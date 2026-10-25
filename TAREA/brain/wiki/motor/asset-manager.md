---
title: engine/asset_manager.py y sprite_sheet.py
type: motor
sources: [juego/engine/asset_manager.py, juego/engine/sprite_sheet.py]
updated: 2026-10-25
---

# engine/asset_manager.py y sprite_sheet.py

- `AssetManager`: `load_spritesheet(name, json_path)`, `get_sprite(sheet, sprite)`, `get_animation(sheet, anim)`, `load_image(name, path)` (usa `convert_alpha`; **requiere ventana creada**), `get_image(name)`. Dicts `spritesheets`, `images`, `sounds` (este último sin uso).
- `Spritesheet(json_path)`: lee el JSON del editor del curso; busca la imagen **junto al JSON** usando solo el nombre de archivo; `get_sprite`, `get_animation_frames`, `sprite_names`.
- Los fondos y objetos de la clase 6 son **imágenes sueltas** (`load_image`), no spritesheets.
