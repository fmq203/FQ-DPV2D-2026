---
title: Arquitectura del juego
type: diseno
sources: [juego/engine/game_loop.py, raw/clase-8.ipynb]
updated: 2026-10-25
---

# Arquitectura del juego

```
juego/
├── engine/                  # motor del curso (+ extensiones documentadas)
└── aventura/
    ├── main.py              # instancia AventuraGame y run()
    ├── game.py              # AventuraGame(Game): assets, audio, estado global, registro de escenas
    ├── state.py             # GameState: inventario, flags de puzles, escena actual, diálogos vistos
    ├── art.py               # arte placeholder geométrico (fondos, props, íconos, Tano)
    ├── data/                # rooms.py (escenarios/hotspots), dialogs.py (árboles + payada), items.py (ítems/recetas)
    ├── scenes/              # menu, game (room), game_over, victory
    └── assets/audio  (los fondos y sprites se generan por código en art.py)/
```
Una sola `GameScene` parametrizada por **room** (datos) en vez de una clase por escenario. El estado vive en `game.state` (ver LEARNINGS.md). Ver [[fsm-verbos]], [[mascara-caminabilidad]], [[escenarios-y-puzles]], [[sistema-dialogos]], [[inventario-y-combinacion]].
