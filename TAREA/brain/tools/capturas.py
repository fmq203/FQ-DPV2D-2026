"""Regenera las capturas del README (TAREA/capturas/*.png) jugando el juego sin ventana.
Uso (desde brain/): juego/.venv/bin/python tools/capturas.py"""
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
BRAIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JUEGO = os.path.join(BRAIN, "juego")
sys.path.insert(0, JUEGO)
sys.path.insert(0, os.path.join(JUEGO, "tests"))
OUT = os.path.join(os.path.dirname(BRAIN), "capturas")
os.makedirs(OUT, exist_ok=True)

import pygame
import smoke_test as t
from aventura.scenes import game_scene as gs


def guardar(g, nombre):
    pygame.image.save(g.screen, os.path.join(OUT, nombre))
    print("OK", nombre)


g = t.AventuraGame()
t.step(g, n=3)
guardar(g, "menu.png")

# Rambla: Tano hablando (intro) y una línea del cielo
t.step(g, [t.click((g.screen.get_width() // 2, 320))], n=3)
t.step(g, n=2)
guardar(g, "rambla.png")
t.settle(g)

s = g.current_scene
for k in ("termo", "mate", "yerba"):
    s.give(k)
s.load_room("mercado", 230)
t.step(g, n=2)
guardar(g, "mercado.png")

s.load_room("tablado", 70)
s.give("diario")
t.step(g, n=2)
guardar(g, "tablado.png")

s.flag("perro_comido")
s.start_dialog("payada_intro")
t.choose(g, "Acepto")
t.step(g, n=2)
guardar(g, "payada.png")
pygame.quit()
