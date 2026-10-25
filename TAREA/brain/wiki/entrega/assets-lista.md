---
title: Lista de assets y origen
type: entrega
sources: [juego/aventura/art.py, tools/gen_sonidos.py]
updated: 2026-10-25
---

# Lista de assets y origen

| Asset | Ubicación | Origen / licencia |
|---|---|---|
| Fondos, props, íconos, personaje (Tano) y NPCs | `juego/aventura/art.py` | Placeholder dibujado por código con `pygame.draw`: sin licencia externa. Se reemplaza con PNG en `juego/aventura/assets/{fondos,sprites,objetos}/` (nombres y tamaños en `assets/README.md`); cada PNG externo debe agregarse a esta tabla con origen y licencia |
| Fondo de la Rambla | `juego/aventura/assets/fondos/rambla.png` | Pixel art 344×192 creado por el usuario con **Pixellab** (herramienta de IA para pixel art; archivo `pixellab-rambla-de-montevideo--uruguay--…png`). **A confirmar:** términos de uso/licencia de Pixellab para el plan usado y declarar el uso de IA en el README/defensa si el curso lo pide |
| Fondo del Mercado del Puerto | `juego/aventura/assets/fondos/mercado.png` | Pixel art 344×192 creado por el usuario con **Pixellab** (igual que la Rambla: confirmar términos/licencia). Los puestos de yerba y de ropa y la parrilla son zonas sobre el dibujo |
| Fondo del Tablado de Carnaval | `juego/aventura/assets/fondos/tablado.png` | Pixel art 344×192 creado por el usuario con **Pixellab** (confirmar términos/licencia). El cartel es una zona sobre la pancarta del dibujo |
| Fondo del menú (Palacio Salvo) | `juego/aventura/assets/fondos/menu.png` | Pixel art 344×192 creado por el usuario con **Pixellab** (confirmar términos/licencia) |
| click/pickup/win/lose .wav | `juego/aventura/assets/audio/` | Generados por código (ondas senoidales, `wave`) el 2026-10-25: sin licencia externa |
| talk/combine/nope/bombo .wav | `juego/aventura/assets/audio/` | Generados por `tools/gen_sonidos.py` (ondas por código): sin licencia externa |
| música | — | **gap — pendiente** (opcional) |
Completar con URL y licencia de cada uno antes de entregar.
