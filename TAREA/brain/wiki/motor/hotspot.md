---
title: engine/hotspot.py — Hotspot
type: motor
sources: [juego/engine/hotspot.py]
updated: 2026-10-25
---

# engine/hotspot.py — Hotspot

`Hotspot(rect, name, callback, cursor="hand", visible=False, color)`: `contains(pos)`, `activate()` (llama `callback(self)`), `handle_event(event)` (solo clic izquierdo; devuelve True si cayó dentro), `draw` (contorno solo si `visible`, útil para depurar).
**Limitación:** solo rectángulos y el callback no recibe el verbo activo → para la tarea la escena debe consultar el verbo/ítem seleccionado ([[fsm-verbos]]) y/o extender con máscaras (`pygame.mask`). Ver [[escenarios-y-puzles]].
