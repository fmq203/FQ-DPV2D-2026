---
title: Arquitectura del juego
type: diseno
sources: [juego/engine/game_loop.py, raw/clase-8.ipynb]
updated: 2026-10-30
---

# Arquitectura del juego

```
juego/
├── engine/                  # motor del curso (+ extensiones documentadas)
└── aventura/
    ├── main.py              # instancia AventuraGame y run()
    ├── game.py              # AventuraGame(Game): assets, audio, estado global, registro de escenas
    ├── state.py             # GameState: inventario, flags de puzles, escena actual, diálogos vistos
    ├── art.py               # carga PNG de assets/ o dibuja el placeholder geométrico
    ├── data/                # rooms.py (escenarios/hotspots), dialogs.py (árboles + payada), items.py (ítems/recetas), creditos.py
    ├── scenes/              # menu, game (room + pausa ESC), game_over (+ reintentar payada), victory, credits
    └── assets/              # fondos/ (Pixellab), sprites/ y objetos/ (tools/gen_sprites.py), audio/ (+ musica_<lugar>.wav)
```
Una sola `GameScene` parametrizada por **room** (datos) en vez de una clase por escenario. El estado vive en `game.state` (ver LEARNINGS.md). `game.checkpoint` guarda el estado al aceptar la payada (para "Reintentar payada"); `game.play_music(track)` pone el tema de cada lugar (`load_room` lo llama; el menú usa `menu`) con fundido, `stop_music()` y `toggle_music()` lo controlan. Documento de diseño de la entrega: `TAREA/DISENO.md`. Ver [[fsm-verbos]], [[mascara-caminabilidad]], [[escenarios-y-puzles]], [[sistema-dialogos]], [[inventario-y-combinacion]].
