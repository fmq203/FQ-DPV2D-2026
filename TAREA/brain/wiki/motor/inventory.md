---
title: engine/inventory.py — Item e Inventory
type: motor
sources: [juego/engine/inventory.py]
updated: 2026-10-25
---

# engine/inventory.py — Item e Inventory

- `Item(name, image, description, usable)`.
- `Inventory(capacity=8)`: `add` (rechaza duplicados/lleno), `remove(name)`, `has`, `get`, `select(name)`, `selected`, `handle_event(event, origin, slot=56)` (clic selecciona), `draw(surface, origin, slot)`.
- `draw`/`handle_event` aceptan `horizontal=True` desde el 2026-10-25 (cambio nuestro, ver [[cambios-al-motor]]); por defecto siguen verticales.
- `combine(a, b, recipes)` (cambio nuestro): `recipes = {frozenset({a, b}): Item}`; quita ambos, agrega el resultado y lo devuelve (o `None`). Ver [[inventario-y-combinacion]].
