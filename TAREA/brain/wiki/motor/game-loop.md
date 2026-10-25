---
title: engine/game_loop.py — GameLoop y Game
type: motor
sources: [juego/engine/game_loop.py]
updated: 2026-10-25
---

# engine/game_loop.py — GameLoop y Game

- `GameLoop(w,h,title,fps)`: `pygame.init`, mixer (tolerante a fallos), ventana, clock; `run()` = `tick → _handle_events → _update → _draw → flip`. Hooks: `handle_specific_events(event)`, `handle_events(events)`, `update_game_logic()`, `draw_game_elements()`.
- `Game(GameLoop)`: gestor de escenas. `add_scene(nombre, ClaseEscena)` (se registra la **clase**), `change_scene(nombre, **kwargs)` (diferido al próximo `update`), la escena se **reinstancia** en cada entrada; llama `on_exit()`/`on_enter()`.
- Uso en este proyecto: `AventuraGame(Game)` con escenas `menu`, `game`, `game_over`, `victory`. Estado persistente en `game`, no en escenas (ver LEARNINGS.md).
- Base: [[clase-8-reestructuracion-motor]].
