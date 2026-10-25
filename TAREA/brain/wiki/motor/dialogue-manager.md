---
title: engine/dialogue_manager.py y dialogue.py
type: motor
sources: [juego/engine/dialogue_manager.py, juego/engine/dialogue.py]
updated: 2026-10-25
---

# engine/dialogue_manager.py y dialogue.py

- `DialogueManager(screen, font_size, color)`: `show_message(text, duration_seconds=0, position="center"|"top")`, `update`, `draw`, `clear_message`. Es el texto flotante que pide la tarea ("textos flotantes de los diálogos"); desde el 2026-10-25 acepta `color`, `center_at=(x, y)` (flota sobre el hablante) y hace wrap con contorno negro (cambio nuestro).
- `DialogueBox(screen)` + `DialogueNode(text, speaker, choices=[(etiqueta, siguiente|None)], action, portrait)`: árbol de conversación con **opciones múltiples**; se navega con teclado (↑↓/W S + Enter/Espacio). Desde el 2026-10-25 soporta **mouse** (hover + clic en opción) y hooks `on_confirm` / `on_end` (cambio nuestro). Ver [[sistema-dialogos]].
