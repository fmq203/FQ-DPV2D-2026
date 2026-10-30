"""Genera la música de fondo por código (sin licencias externas): un loop por lugar.
  musica_menu.wav    retirada de murga (bombo, platillo, redoblante + melodía en la menor)
  musica_rambla.wav  lento y melancólico, con lluvia de fondo (El Niño)
  musica_mercado.wav candombe: madera, chico, repique y piano + melodía alegre
  musica_tablado.wav marcha camión de murga, más rápida, con fanfarria
Cada loop dura un número exacto de compases, así empalma sin saltos.
Uso: python3 tools/gen_musica.py   (desde brain/) -> juego/aventura/assets/audio/"""
import math
import os
import random
import struct
import wave

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "juego", "aventura", "assets", "audio")
RATE = 22050

# Notas (Hz)
G3, A3, C4, D4, E4, FS4, G4, A4, B4 = 196.0, 220.0, 261.63, 293.66, 329.63, 369.99, 392.0, 440.0, 493.88
C5, D5, E5, F5, G5 = 523.25, 587.33, 659.25, 698.46, 783.99


class Tema:
    """Buffer mono de `tiempos` negras a `bpm`; se mezclan sonidos con add(tiempo_en_negras, muestras)."""

    def __init__(self, bpm, tiempos, semilla=7):
        self.negra = 60 / bpm
        self.largo = int(RATE * self.negra * tiempos)
        self.buf = [0.0] * self.largo
        random.seed(semilla)  # ruido reproducible

    def add(self, t, muestras):
        i0 = int(t * self.negra * RATE)
        for k, v in enumerate(muestras):
            self.buf[(i0 + k) % self.largo] += v  # lo que sobra al final entra por el principio: loop sin cortes

    def melodia(self, notas, forma="cuad", vol=0.12, octava=1.0):
        t = 0
        for f, dur in notas:
            self.add(t, nota(f * octava, dur * self.negra * 0.95, forma, vol))
            t += dur
        assert abs(t * self.negra * RATE - self.largo) < 2, f"la melodía dura {t} negras"

    def guardar(self, nombre, pico_final=0.8):
        pico = max(abs(v) for v in self.buf) or 1
        with wave.open(os.path.join(OUT, nombre), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(RATE)
            w.writeframes(b"".join(struct.pack("<h", int(v / pico * pico_final * 32767)) for v in self.buf))
        print(f"OK {nombre} ({self.largo / RATE:.1f} s)")


# ------------------------------------------------------------------ instrumentos
def nota(freq, dur, forma="cuad", vol=0.12):
    n = int(RATE * dur)
    out = []
    for i in range(n):
        env = min(1, i / 300) * math.exp(-i / (RATE * dur * 0.8))
        v = math.sin(2 * math.pi * freq * i / RATE)
        if forma == "cuad":
            v = 1 if v >= 0 else -1  # onda cuadrada "chiptune"
        out.append(vol * env * v)
    return out


def bombo(vol=0.9):
    n = int(RATE * 0.28)
    return [vol * math.sin(2 * math.pi * (95 - 50 * i / n) * i / RATE) * math.exp(-i / (RATE * 0.09))
            for i in range(n)]


def tambor(freq, vol=0.5, decay=0.08, ruido=0.3):
    """Tambor de candombe: tono que cae + golpe de ruido (piano: grave, repique: medio, chico: agudo)."""
    n = int(RATE * decay * 4)
    return [vol * math.exp(-i / (RATE * decay)) *
            ((1 - ruido) * math.sin(2 * math.pi * freq * (1 - 0.3 * i / n) * i / RATE) + ruido * random.uniform(-1, 1))
            for i in range(n)]


def madera(vol=0.25):
    """Palo contra la madera del tambor (la "clave" del candombe)."""
    n = int(RATE * 0.04)
    return [vol * math.sin(2 * math.pi * 1900 * i / RATE) * math.exp(-i / (RATE * 0.008)) for i in range(n)]


def platillo(vol=0.25, largo=0.18):
    n = int(RATE * largo)
    return [vol * random.uniform(-1, 1) * math.exp(-i / (RATE * largo / 4)) for i in range(n)]


def redoble(vol=0.15):
    n = int(RATE * 0.06)
    return [vol * random.uniform(-1, 1) * math.exp(-i / (RATE * 0.015)) for i in range(n)]


def murga(tema, compases, platillo_en_cada_tiempo=False):
    """Base de murga en 2/4 ("marcha camión"): bombo en 1 y en el "y" del 2, platillo, redoblante."""
    for c in range(compases):
        t = c * 2
        tema.add(t, bombo())
        tema.add(t + 1.5, bombo(0.6))
        tema.add(t + 1, platillo())
        if platillo_en_cada_tiempo:
            tema.add(t, platillo(0.15, 0.12))
        elif c % 2 == 1:
            tema.add(t + 1.5, platillo(0.18, 0.1))
        for s in range(8):
            tema.add(t + s / 4, redoble(0.2 if s in (0, 4) else 0.08))


# ------------------------------------------------------------------ temas
def menu():
    t = Tema(112, 16)
    murga(t, 8)
    t.melodia([(E5, 1), (E5, .5), (D5, .5), (C5, 1), (A4, 1),
               (C5, .5), (D5, .5), (E5, 1), (D5, 2),
               (E5, 1), (F5, .5), (E5, .5), (D5, 1), (C5, 1),
               (G5, .5), (F5, .5), (E5, .5), (D5, .5), (A4, 2)], octava=0.5)
    t.guardar("musica_menu.wav")


def rambla():
    """4/4 lento: bajo suave (la menor - fa - do - sol), melodía senoidal, escobilla y lluvia."""
    t = Tema(72, 16, semilla=3)
    for c, bajo in enumerate((110.0, 87.31, 130.81, 98.0)):
        for b in (0, 2):
            t.add(c * 4 + b, nota(bajo, t.negra * 1.9, "sin", 0.35))
        for b in (1, 3):
            t.add(c * 4 + b, platillo(0.05, 0.25))  # escobilla
    t.melodia([(E4, 2), (D4, 1), (C4, 1), (C4, 3), (A3, 1),
               (G3, 2), (C4, 1), (D4, 1), (D4, 4)], forma="sin", vol=0.22)
    # lluvia: ruido suavizado continuo + gotas sueltas
    suave = 0.0
    lluvia = []
    for _ in range(t.largo):
        suave = suave * 0.92 + random.uniform(-1, 1) * 0.08
        lluvia.append(suave * 0.35)
    t.add(0, lluvia)
    for _ in range(40):
        t.add(random.uniform(0, 16), madera(random.uniform(0.03, 0.07)))
    t.guardar("musica_rambla.wav", pico_final=0.6)


def mercado():
    """Candombe en 4/4: madera (clave), chico, repique y piano, + melodía alegre en sol."""
    t = Tema(116, 16, semilla=11)
    for c in range(4):
        base = c * 4
        for p in ((0, .5, 1.5, 2, 3) if c % 2 == 0 else (0, 1, 1.5, 2.5, 3)):  # clave
            t.add(base + p, madera())
        for b in range(4):                                                    # chico: "ta-ki" en cada tiempo
            t.add(base + b + .5, tambor(520, 0.22, 0.03, 0.5))
            t.add(base + b + .75, tambor(520, 0.16, 0.03, 0.5))
        for p in (0, 1.5, 2, 3.5):                                            # piano (grave)
            t.add(base + p, tambor(110, 0.6, 0.09, 0.2))
        for p in ((2.75, 3.25) if c % 2 else (1.25, 3.75)):                   # repique
            t.add(base + p, tambor(260, 0.35, 0.05, 0.4))
    t.melodia([(G4, 1), (B4, .5), (D5, .5), (E5, 1), (D5, 1),
               (B4, 1), (A4, .5), (G4, .5), (A4, 2),
               (G4, 1), (B4, .5), (D5, .5), (E5, .5), (D5, .5), (B4, 1),
               (A4, 1), (B4, .5), (A4, .5), (G4, 2)], vol=0.1)
    t.guardar("musica_mercado.wav")


def tablado():
    """Marcha camión más rápida, platillo en cada tiempo y fanfarria en re mayor."""
    t = Tema(128, 16, semilla=5)
    murga(t, 8, platillo_en_cada_tiempo=True)
    t.melodia([(D4, 1), (FS4, .5), (A4, .5), (A4, 1), (FS4, 1),
               (G4, .5), (A4, .5), (B4, 1), (A4, 2),
               (G4, 1), (FS4, .5), (E4, .5), (D4, 1), (E4, 1),
               (FS4, .5), (E4, .5), (D4, 1), (D4, 2)], vol=0.13)
    t.guardar("musica_tablado.wav")


if __name__ == "__main__":
    menu()
    rambla()
    mercado()
    tablado()
