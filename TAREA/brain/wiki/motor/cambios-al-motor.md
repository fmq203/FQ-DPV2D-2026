---
title: Cambios al motor (a documentar en la entrega)
type: motor
sources: [raw/tarea-videojuegos-2026-v2.pdf, juego/engine/]
updated: 2026-10-25
---

# Cambios al motor (a documentar en la entrega)

La tarea permite modificar/extender el motor **documentando los cambios** ([[requisitos-comunes]]). Cada cambio en `juego/engine/` se marca en el código con el comentario `# [Tarea 2026]`, se registra acá y en `decisions.md`. Esta tabla es la base de la sección "Cambios al motor" del README ([[readme-plantilla]]).

| Módulo | Cambio | Estado | Motivo |
|---|---|---|---|
| `engine/inventory.py` | Parámetro `horizontal=False` en `draw`/`handle_event` (+ `_slot_rect`); compatible hacia atrás | **hecho** 2026-10-25 | Barra inferior horizontal, ver [[inventario-y-combinacion]] |
| `engine/inventory.py` | `combine(a, b, recipes)` | **hecho** 2026-10-25 | [[inventario-y-combinacion]] |
| `engine/dialogue.py` | `DialogueBox`: opciones con **mouse** + hooks `on_confirm`/`on_end` | **hecho** 2026-10-25 | Antes solo teclado, ver [[dialogue-manager]] |
| `engine/dialogue_manager.py` | `show_message(color, center_at)`, wrap y contorno | **hecho** 2026-10-25 | Texto flotante sobre el hablante |
| `engine/walkmask.py` (nuevo) | Máscara de caminabilidad + movimiento ([[walkmask]]) | **hecho** 2026-10-25 | [[mascara-caminabilidad]] |
| barra de verbos | Vive en el juego (`game_scene.py`), no en el motor | **hecho** (sin tocar motor) | [[fsm-verbos]] |

Extensiones que **no** tocan el motor (viven en `juego/aventura/`): `SoundButton` (sonido en botones).
