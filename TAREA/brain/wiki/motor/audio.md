---
title: engine/audio.py — AudioManager
type: motor
sources: [juego/engine/audio.py, juego/engine/shared_assets.py]
updated: 2026-10-25
---

# engine/audio.py — AudioManager

`AudioManager(num_channels=16)`: `load_sound(name, path)`, `play_sound(name)` (ignora si no existe), `load_music(path)`, `play_music(loops=-1, volume=0.5)`, `stop_music()`. Se desactiva solo si no hay audio.
**Gap:** `shared_assets.sfx_path()` apunta a `assets/sonidos/*.wav` de una carpeta "2027" que no está en el zip → no usarlo; cargar sonidos desde `juego/aventura/assets/audio/` y registrarlos en [[assets-lista]]. Requisito: sonido en cada interacción de UI ([[requisitos-comunes]]).
