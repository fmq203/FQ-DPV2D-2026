---
title: Clase 8: reestructuración del motor
type: clase
sources: [raw/clase-8.ipynb]
updated: 2026-10-25
---

# Clase 8: reestructuración del motor

Principio: el `engine/` guarda lo genérico; la carpeta del juego guarda lógica, arte y reglas propias.

Estructura de un juego (ejemplo Arkanoid, y `platformer/` del zip): `main.py` mínimo → `game.py` (clase del juego, crea `AssetManager`, carga assets, registra escenas) → `entities.py` (heredan de `GameObject`) → `scenes/*` (heredan de `Scene`, usan `self.game.assets`).

Módulos del motor documentados: `game_loop`, `asset_manager`, `spritesheet`, `game_object`, `ui`, `dialogue`. Ver [[game-loop]], [[asset-manager]], [[game-object]], [[scene-ui]], [[dialogue-manager]].

Convenciones: llamar `super().update()` en entidades para que corra la animación; assets se cargan con apodo y se piden por apodo; `main.py` solo instancia y ejecuta.
Herramienta: editor de spritesheets (tkinter + PIL) incluido en el notebook.
