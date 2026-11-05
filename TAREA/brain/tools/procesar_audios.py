"""Convierte las grabaciones propias (assets/audio/originales/*.m4a) en efectos .wav para el juego:
recorta el silencio del principio y del final, normaliza el volumen y la pasa a mono 44,1 kHz.
Uso (desde brain/): juego/.venv/bin/python tools/procesar_audios.py
Para sumar un sonido: guardar el audio en originales/ con el nombre que debe tener (ej. "hablar perro.m4a")."""
import array
import math
import os
import subprocess
import unicodedata
import wave

import imageio_ffmpeg

BRAIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO = os.path.join(BRAIN, "juego", "aventura", "assets", "audio")
ORIG = os.path.join(AUDIO, "originales")
RATE = 44100
# sonidos largos: segundos que se cortan del principio (ya sin el silencio inicial)
CORTAR_INICIO = {"poner_chorizo": 0.5, "agarrar_chorizo_asado": 0.5, "gato_mojado": 1.5, "hablar_gato": 0.5,
                 "perro_come_chori": 0.5}
# archivo original -> nombre del sonido, solo si debe ser distinto del nombre del archivo
# (por defecto "hablar perro.m4a" -> hablar_perro.wav: minúsculas, sin tildes y con _ en vez de espacios)
RENOMBRAR = {
    "agarrar mate.m4a": "agarrar_mate",
    "agarrar termo.m4a": "agarrar_termo",
    "agarrar yerba.m4a": "agarrar_yerba",
    "agarrar papel.m4a": "agarrar_diario",   # el ítem se llama diario
    "agarrar troncos.m4a": "agarrar_lena",   # el ítem se llama lena
    "chori 1.m4a": "poner_chorizo",
    "chori 2.m4a": "agarrar_chorizo_asado",
    "hablar yerba.m4a": "hablar_yerbas",     # el hotspot se llama yerbas
    "voz 1 1.m4a": "voz_pescador_1", "voz 1 2.m4a": "voz_pescador_2", "voz 1 3.m4a": "voz_pescador_3",
    "voz 3 1.m4a": "voz_asador_1", "voz 3 2.m4a": "voz_asador_2", "voz 3 3.m4a": "voz_asador_3",
    "voz 2 1.m4a": "voz_contramaestre_1", "voz 2 2.m4a": "voz_contramaestre_2", "voz 2 3.m4a": "voz_contramaestre_3",
    "apoyar mate.m4a": "apoyar_mate",
    "apoyar termo .m4a": "apoyar_termo",
    "tirar papel.m4a": "tirar_papel",
}


def leer(path):
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    raw = subprocess.run([ff, "-v", "0", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(RATE), "-"],
                         capture_output=True, check=True).stdout
    a = array.array("h")
    a.frombytes(raw)
    return a


def recortar(a):
    w = RATE // 50  # ventanas de 20 ms
    env = [math.sqrt(sum(x * x for x in a[i:i + w]) / w) / 32768 for i in range(0, len(a) - w, w)]
    umbral = max(max(env) * 0.12, 0.004)
    act = [i for i, e in enumerate(env) if e > umbral]
    ini = max(0, (act[0] - 4) * w)
    fin = min(len(a), (act[-1] + 14) * w)
    return a[ini:fin]


def guardar(a, path):
    pico = max(abs(x) for x in a) or 1
    k = 0.9 * 32767 / pico
    out = array.array("h", (int(x * k) for x in a))
    caida = min(len(out), RATE // 12)  # fundido de salida para que no corte seco
    for i in range(caida):
        out[len(out) - 1 - i] = int(out[len(out) - 1 - i] * i / caida)
    with wave.open(path, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(RATE)
        f.writeframes(out.tobytes())


def nombre_de(archivo):
    base = unicodedata.normalize("NFKD", os.path.splitext(archivo)[0]).encode("ascii", "ignore").decode()
    return RENOMBRAR.get(archivo) or "_".join(base.lower().split())


for origen in sorted(os.listdir(ORIG)):
    if not origen.lower().endswith((".m4a", ".mp3", ".wav", ".ogg")):
        continue
    nombre = nombre_de(origen)
    a = recortar(leer(os.path.join(ORIG, origen)))
    a = a[int(CORTAR_INICIO.get(nombre, 0) * RATE):]
    guardar(a, os.path.join(AUDIO, f"{nombre}.wav"))
    print(f"OK {nombre}.wav  {len(a) / RATE:.2f} s")
