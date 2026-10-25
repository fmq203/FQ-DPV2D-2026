"""Genera los .wav placeholder nuevos (ondas por código, sin licencias externas).
Uso: python3 tools/gen_sonidos.py   (desde brain/)"""
import math
import os
import struct
import wave

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "juego", "aventura", "assets", "audio")
RATE = 22050


def tono(nombre, notas, vol=0.4):
    """notas: lista de (frecuencia_hz, duracion_s, forma) con forma 'sin' o 'cuad'."""
    datos = bytearray()
    for f, d, forma in notas:
        n = int(RATE * d)
        for i in range(n):
            env = min(1, i / 200) * min(1, (n - i) / 400)
            v = math.sin(2 * math.pi * f * i / RATE)
            if forma == "cuad":
                v = 1 if v >= 0 else -1
            datos += struct.pack("<h", int(v * env * vol * 32767))
    with wave.open(os.path.join(OUT, nombre), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(bytes(datos))


tono("talk.wav", [(330, 0.04, "cuad"), (392, 0.04, "cuad")], 0.25)
tono("combine.wav", [(440, 0.08, "sin"), (554, 0.08, "sin"), (659, 0.14, "sin")])
tono("nope.wav", [(180, 0.12, "cuad"), (140, 0.18, "cuad")], 0.3)
tono("bombo.wav", [(70, 0.25, "sin"), (55, 0.2, "sin")], 0.7)
print("OK ->", OUT)
