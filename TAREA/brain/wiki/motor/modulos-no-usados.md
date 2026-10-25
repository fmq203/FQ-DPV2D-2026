---
title: Módulos del motor no necesarios para la aventura
type: motor
sources: [juego/engine/]
updated: 2026-10-25
---

# Módulos del motor no necesarios para la aventura

`tilemap.py` (TilemapLoader, Tile), `camera.py`, `iso_tools.py` (opción 2), `physics.py`/`physics_object.py` (Pymunk, opción 3), `particle.py` (útil como efecto opcional al abrir el cofre), `background.py` (Parallax/Frame/Video; opcional), `challenge.py` (reto con tiempo; opcional como minipuzle), `dialogue.py` ya cubierto en [[dialogue-manager]]. No eliminarlos del motor (`engine/__init__.py` los importa).
