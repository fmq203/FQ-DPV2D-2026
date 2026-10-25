---
title: engine/walkmask.py — WalkMask
type: motor
sources: [juego/engine/walkmask.py]
updated: 2026-10-25
---

# engine/walkmask.py — WalkMask (módulo nuevo, nuestro)

`WalkMask(size, rects)`: zona navegable = unión de rectángulos, rasterizada en una `pygame.mask.Mask`.
- `contains(pos)`: ¿es caminable el píxel?
- `nearest(pos)`: punto navegable más cercano (clamp contra cada rect).
- `step(pos, target, dist)`: avanza en línea recta; si choca, se desliza por un eje; devuelve `(pos, llegó)`.
Usado por `GameScene` para el click-to-walk. Ver [[mascara-caminabilidad]], [[cambios-al-motor]].
