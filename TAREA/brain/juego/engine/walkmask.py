"""
engine/walkmask.py

# [Tarea 2026] Módulo nuevo: zona navegable de un escenario (máscara de caminabilidad).

La zona se define como unión de rectángulos y se rasteriza en una
`pygame.mask.Mask` (un bit por píxel de la pantalla). El personaje se mueve
en línea recta hacia el destino, deslizándose por los bordes si hay pared.
"""

import math

import pygame


class WalkMask:
    def __init__(self, size, rects):
        self.rects = [pygame.Rect(r) for r in rects]
        surf = pygame.Surface(size)
        surf.fill((0, 0, 0))
        for r in self.rects:
            surf.fill((255, 255, 255), r)
        self.mask = pygame.mask.from_threshold(surf, (255, 255, 255), (1, 1, 1, 255))
        self.size = size

    def contains(self, pos):
        x, y = int(pos[0]), int(pos[1])
        if not (0 <= x < self.size[0] and 0 <= y < self.size[1]):
            return False
        return bool(self.mask.get_at((x, y)))

    def nearest(self, pos):
        """Punto caminable más cercano a `pos` (el mismo si ya es caminable)."""
        if self.contains(pos):
            return (pos[0], pos[1])
        best, best_d = None, None
        for r in self.rects:
            p = (min(max(pos[0], r.left), r.right - 1), min(max(pos[1], r.top), r.bottom - 1))
            d = (p[0] - pos[0]) ** 2 + (p[1] - pos[1]) ** 2
            if best_d is None or d < best_d:
                best, best_d = p, d
        return best

    def step(self, pos, target, dist):
        """Avanza `dist` píxeles de `pos` hacia `target`. Devuelve (nueva_pos, llegó)."""
        dx, dy = target[0] - pos[0], target[1] - pos[1]
        d = math.hypot(dx, dy)
        if d <= dist:
            return (target[0], target[1]), True
        nx, ny = pos[0] + dx / d * dist, pos[1] + dy / d * dist
        if self.contains((nx, ny)):
            return (nx, ny), False
        for cand in ((nx, pos[1]), (pos[0], ny)):  # deslizar por el borde
            if self.contains(cand) and cand != tuple(pos):
                return cand, False
        return (pos[0], pos[1]), True  # trabado: se corta el movimiento
