---
title: engine/ui.py y ui_elements.py — Scene, Button, Label, Panel, barras
type: motor
sources: [juego/engine/ui.py, juego/engine/ui_elements.py]
updated: 2026-10-25
---

# engine/ui.py y ui_elements.py — Scene, Button, Label, Panel, barras

- `Scene(game)`: `on_enter`, `on_exit`, `handle_events(events)`, `update()`, `draw(surface)`.
- `Button(x,y,w,h,text,callback,font_size,color,hover_color,text_color)`: `handle_event(event)` (clic izq. dentro del rect → callback), `draw`. **No reproduce sonido**: hay que llamar `game.audio.play_sound("click")` dentro del callback o extender `Button` (cambio a documentar, [[cambios-al-motor]]).
- `Label(text,pos,size,color,align)`, `Panel(rect,color RGBA,border)`, `ProgressBar`, `HealthBar` (ver `ui_elements.py`).
- Sirve para: [[requisitos-comunes]] (menú/game over/victoria).
