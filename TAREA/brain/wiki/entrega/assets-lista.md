---
title: Lista de assets y origen
type: entrega
sources: [juego/aventura/art.py, tools/gen_sonidos.py, tools/gen_sprites.py, tools/gen_musica.py]
updated: 2026-10-30
---

# Lista de assets y origen

| Asset | Ubicación | Origen / licencia |
|---|---|---|
| Respaldo de todo el arte | `juego/aventura/art.py` | Placeholder dibujado por código con `pygame.draw` (solo se usa si falta el PNG): sin licencia externa. Cada PNG externo nuevo debe agregarse a esta tabla con origen y licencia |
| Sprites: Tano (quieto + 4 frames de caminata), pescador, parrillero, contramaestre, perro, gato, bombo, banco, tacho (+ vacío), puesto de yerbas, parrilla (+ prendida) | `juego/aventura/assets/sprites/*.png` | Pixel art **generado por código** el 2026-10-30 con `tools/gen_sprites.py` (pygame): sin licencia externa. Editables a mano (p. ej. LibreSprite); el script los sobrescribe si se vuelve a correr |
| Íconos de inventario (termo, mate, mate cargado, mate listo, yerba, diario, chori al pan) | `juego/aventura/assets/objetos/*.png` | Ídem, generados por `tools/gen_sprites.py` |
| Fondo de la Rambla de Barrio Sur | `juego/aventura/assets/fondos/rambla.png` | Pixel art 344×192 creado por el usuario con **Pixellab** (herramienta de IA para pixel art; archivo `pixellab-rambla-de-montevideo--uruguay--…png`). **A confirmar:** términos de uso/licencia de Pixellab para el plan usado y declarar el uso de IA en el README/defensa si el curso lo pide |
| Fondo del Mercado del Puerto | `juego/aventura/assets/fondos/mercado.png` | Pixel art 344×192 creado por el usuario con **Pixellab** (igual que la Rambla: confirmar términos/licencia). Los puestos de yerba y de ropa y la parrilla son zonas sobre el dibujo |
| Fondo del Museo del Carnaval (tablado) | `juego/aventura/assets/fondos/tablado.png` | Pixel art 344×192 creado por el usuario con **Pixellab** (confirmar términos/licencia). El cartel es una zona sobre la pancarta del dibujo |
| Fondo del menú (Palacio Salvo) | `juego/aventura/assets/fondos/menu.png` | Pixel art 344×192 creado por el usuario con **Pixellab** (confirmar términos/licencia) |
| click/pickup/win/lose .wav | `juego/aventura/assets/audio/` | Generados por código (ondas senoidales, `wave`) el 2026-10-25: sin licencia externa |
| talk/combine/nope/bombo .wav | `juego/aventura/assets/audio/` | Generados por `tools/gen_sonidos.py` (ondas por código): sin licencia externa |
| musica_menu / musica_rambla / musica_mercado / musica_tablado .wav (loops de 7–13 s: retirada de murga, rambla lluviosa, candombe, marcha camión) | `juego/aventura/assets/audio/` | Sintetizadas por `tools/gen_musica.py` (tambores, platillo, lluvia y melodías por código) el 2026-10-30: sin licencia externa |
| Video de entrega | `TAREA/video/el-murguista.mp4` | Grabado por `tools/grabar_video.py` con las imágenes del juego, la música de cada lugar y `win.wav` |
| Asistencia de IA en código y diseño | — | Claude Sonnet 5.5 y Claude Opus 5.5 (Anthropic); declarado en los Créditos del juego, el README y `DISENO.md` |
Completar con URL y licencia de cada uno antes de entregar.
