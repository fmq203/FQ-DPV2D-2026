---
title: engine/cursor.py — Cursor
type: motor
sources: [juego/engine/cursor.py]
updated: 2026-10-25
---

# engine/cursor.py — Cursor

`Cursor(normal, hover, size)`: dibuja un cursor propio (flecha / círculo rojo) y oculta el del sistema (`mouse.set_visible(False)`); `draw(surface, hovered=False)`. Usarlo con `hovered = any(h.contains(pos) for h in hotspots)`. Puede aceptar imágenes propias (un cursor por verbo).
