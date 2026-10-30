"""Graba el video de entrega (15–40 s) jugando una partida guionada, sin ventana.
Sigue wiki/entrega/video-guion.md: menú -> Rambla (agarrar, diálogo) -> Mercado (combinar, dar)
(gato, fuego y chorizo a punto) -> Museo del Carnaval (payada) -> Victoria. Las caminatas van al doble de velocidad y hay cortes
en las partes lentas. De fondo va la música de cada lugar y el jingle de victoria (los demás efectos no se graban).
Requiere imageio-ffmpeg en el venv:  juego/.venv/bin/pip install imageio-ffmpeg
Uso (desde brain/): juego/.venv/bin/python tools/grabar_video.py  -> TAREA/video/el-murguista.mp4"""
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import wave

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
BRAIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JUEGO = os.path.join(BRAIN, "juego")
sys.path[:0] = [JUEGO, os.path.join(JUEGO, "tests")]
SALIDA = os.path.join(os.path.dirname(BRAIN), "video", "el-murguista.mp4")
FPS = 30  # el juego corre a 60: se guarda 1 de cada 2 frames (o 1 de 4 al caminar = x2)
AUDIO = os.path.join(JUEGO, "aventura", "assets", "audio")
RATE = 22050  # frecuencia de los .wav generados

import imageio_ffmpeg
import pygame

# Reloj y mouse virtuales: el juego cree que pasa 1/60 s por frame y que el mouse está en MOUSE.
_ticks = [0]
MOUSE = [450, 300]
pygame.time.get_ticks = lambda: _ticks[0]
pygame.mouse.get_pos = lambda: tuple(MOUSE)

import smoke_test as t  # noqa: E402  (después de los parches)
from aventura.scenes import game_scene as gs  # noqa: E402

frames_dir = tempfile.mkdtemp(prefix="murguista_")
n_frame, n_tick = [0], [0]
pistas = []
g = t.AventuraGame()


def tick(events=(), n=1, grabar=True, cada=2):
    for e in events:
        pygame.event.post(e)
    for _ in range(n):
        _ticks[0] += 1000 // 60
        g._handle_events()
        g._update()
        g._draw()
        n_tick[0] += 1
        if grabar and n_tick[0] % cada == 0:
            pygame.image.save(g.screen, os.path.join(frames_dir, f"f{n_frame[0]:05d}.png"))
            pistas.append(g.music_playing)  # qué tema suena en este frame (None = silencio)
            n_frame[0] += 1


def mover(pos, frames=16):
    x0, y0 = MOUSE
    for i in range(1, frames + 1):
        k = i / frames
        k = k * k * (3 - 2 * k)  # suavizado
        MOUSE[:] = [x0 + (pos[0] - x0) * k, y0 + (pos[1] - y0) * k]
        tick()


def clic(pos, frames=16):
    mover(pos, frames)
    tick([t.click(tuple(int(v) for v in pos))])


def esperar(leer=45, grabar=True):
    """Hasta que Tano quede libre: graba cada línea `leer` frames y la salta; caminatas a x2."""
    desde = n_tick[0]
    for _ in range(4000):
        s = g.current_scene
        if s.fsm in (gs.IDLE, gs.DIALOGUE):
            return
        if s.fsm == gs.SPEAKING and n_tick[0] - desde >= leer:
            tick([t.click((450, 100))], grabar=grabar)
            desde = n_tick[0]
        else:
            if s.fsm == gs.WALKING:
                desde = n_tick[0]
            tick(grabar=grabar, cada=4 if s.fsm == gs.WALKING else 2)


def hotspot(hid):
    return next(h for h in g.current_scene.hotspots if h.data["id"] == hid).rect.center


def verbo(v):
    clic(g.current_scene.verb_rects[v].center, 12)


def item(key):
    s = g.current_scene
    i = [it.name for it in s.inventory.items].index(key)
    clic(s.inventory._slot_rect(gs.INV_ORIGIN, i, gs.INV_SLOT, True).center, 12)


def accion(v, hid, con=None, leer=55):
    verbo(v)
    if con:
        item(con)
    clic(hotspot(hid))
    esperar(leer)


def opcion(texto, pausa=30):
    box = g.current_scene.box
    tick(n=pausa)
    for (label, _), rect in zip(box.current.choices, box.choice_rects):
        if label.startswith(texto):
            return clic(rect.center, 12)
    raise AssertionError(texto)


# ------------------------------------------------------------------ guion
tick(n=70)                                              # menú
clic((450, 328), 20)
tick(n=2)
esperar(leer=55)                                        # intro de Tano (3 líneas)
accion("Agarrar", "termo", leer=0)
accion("Agarrar", "mate", leer=0)
accion("Agarrar", "tacho", leer=45)
accion("Hablar", "pescador")
opcion("Me robaron", 25); opcion("¿Y cómo", 25); opcion("Mate y chori", 45)
esperar()
accion("Mirar", "a_mercado", leer=0)                    # -> Mercado del Puerto
accion("Agarrar", "yerbas", leer=0)
verbo("Usar"); item("yerba"); item("mate"); esperar(30)            # combinar
verbo("Usar"); item("mate_cargado"); item("termo"); esperar(30)
accion("Usar", "gato", con="termo", leer=40)               # mini-reto: espantar al gato
accion("Agarrar", "lena", leer=0)
verbo("Usar"); item("diario"); item("lena"); esperar(30)  # fuego armado
accion("Usar", "parrilla", con="lena_papel", leer=33)
accion("Usar", "parrilla", con="chorizo", leer=45)
while not g.current_scene.has_flag("chorizo_a_punto"):   # corte: el chorizo se asa sin grabar
    tick(grabar=False)
tick(n=2, grabar=False)
esperar(45)                                               # "¡Huele a gloria!"
accion("Agarrar", "parrilla", leer=40)
verbo("Usar"); item("chorizo_asado"); item("pan"); esperar(35)
accion("Mirar", "a_tablado", leer=0)                    # -> Museo del Carnaval
accion("Dar", "perro", con="choripan", leer=38)
accion("Dar", "contramaestre", con="mate_listo", leer=35)
opcion("Acepto", 20)
from aventura.data.dialogs import PAYADA  # noqa: E402
for i, (_, opciones) in enumerate(PAYADA):
    correcta = [o for o, ok in opciones if ok][0]
    if i < 1:
        opcion(correcta, 45)
        opcion("(Seguir)", 35)
    else:  # corte: los últimos versos se resuelven sin grabar
        t.choose(g, correcta)
        t.choose(g, "(Seguir)")
opcion("¡Gracias", 45)
esperar()
accion("Agarrar", "bombo", leer=40)
tick(n=75)                                              # pantalla de Victoria

# ------------------------------------------------------------------ exportar
def leer_wav(nombre):
    with wave.open(os.path.join(AUDIO, nombre)) as w:
        assert w.getframerate() == RATE and w.getnchannels() == 1 and w.getsampwidth() == 2, nombre
        datos = w.readframes(w.getnframes())
    return [v / 32768 for v in struct.unpack(f"<{len(datos) // 2}h", datos)]


def banda_sonora(ruta):
    """Arma el audio siguiendo el tema que sonaba en cada frame (como en el juego: al cambiar de
    lugar el tema nuevo arranca de cero con fundido de entrada); al terminar la música, el jingle de victoria."""
    temas, out = {}, []
    por_frame = RATE // FPS
    anterior, pos, jingle = None, 0, None
    for pista in pistas:
        if pista != anterior:
            if pista is None and anterior is not None:
                jingle = len(out)
            pos = 0
        if pista:
            temas.setdefault(pista, leer_wav(f"musica_{pista}.wav"))
            muestras = temas[pista]
            for _ in range(por_frame):
                fade = min(1, pos / (RATE * 0.9))
                out.append(muestras[pos % len(muestras)] * 0.6 * fade)
                pos += 1
        else:
            out.extend([0.0] * por_frame)
        anterior = pista
    if jingle is not None:
        for k, v in enumerate(leer_wav("win.wav")):
            if jingle + k < len(out):
                out[jingle + k] += v * 0.8
    with wave.open(ruta, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, v)) * 32767)) for v in out))


os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
audio = os.path.join(frames_dir, "banda.wav")
banda_sonora(audio)
duracion = n_frame[0] / FPS
cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
       "-framerate", str(FPS), "-i", os.path.join(frames_dir, "f%05d.png"),
       "-i", audio,
       "-map", "0:v", "-map", "1:a", "-shortest",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
       "-c:a", "aac", "-b:a", "128k", "-af", f"afade=t=out:st={max(0, duracion - 1.5):.2f}:d=1.5", SALIDA]
subprocess.run(cmd, check=True)
shutil.rmtree(frames_dir)
pygame.quit()
print(f"OK {SALIDA}  ({duracion:.1f} s, {n_frame[0]} frames)")
