# decisions — log de decisiones (append-only)

| Fecha | Decisión | Motivo |
|---|---|---|
| 2026-10-25 | Elegir **Opción 1: Aventura gráfica** | Elección del usuario; el motor ya trae `hotspot`, `inventory`, `cursor`, `dialogue`, `audio` y la Clase 6 es una aventura |
| 2026-10-25 | Brain ubicado en `Videojuegos/TAREA/brain/` | Elección del usuario |
| 2026-10-25 | Usar `AGENTS.md` en lugar de `CLAUDE.md` | Pedido del usuario; Claude Code solo autocarga CLAUDE.md → si se quiere, agregar `CLAUDE.md` con `@AGENTS.md` (creado 2026-10-25) |
| 2026-10-25 | Patrón del PDF: `raw/` inmutable + `wiki/` del agente + MEMORY/LEARNINGS/decisions | Guía `raw/guia-second-brain.pdf` §3.1–3.4 |
| 2026-10-25 | `juego/engine/` = copia de `engine/` del zip, sin `.venv`/`.idea`/`__pycache__` | Evitar ~miles de archivos de venv; el original queda en `raw/motor-2026-con-ejemplos.zip` |
| 2026-10-25 | Escenas = clases registradas con `Game.add_scene` (patrón Clase 8 / `platformer`) | Es el enfoque que el motor recomienda para juegos con menú/game over |
| 2026-10-25 | `aventura/ui.py::SoundButton` envuelve `engine.ui.Button` en vez de modificar el motor | Cumplir sonido en UI sin tocar `engine/` |
| 2026-10-25 | Sonidos placeholder generados por código | No hay sonidos en el zip; evitar problemas de licencia |
| 2026-10-25 | Primer cambio al motor: `Inventory` con `horizontal=True`, marcado `# [Tarea 2026]` | El panel vertical se salía de pantalla; ver `wiki/motor/cambios-al-motor.md` |
| 2026-10-25 | `SoundButton` reescrito: sobrescribe `handle_event` en vez de parsear argumentos | La versión anterior dependía de la posición del callback y era frágil |
| 2026-10-25 | Agregados `juego/tests/smoke_test.py` y `tools/lint.py` | Verificación repetible de juego y brain |
| 2026-10-25 | Ambientación: **"El Murguista"** en Montevideo (Rambla de Pocitos, Mercado del Puerto, Tablado de Barrio Sur) reemplaza selva/mono/banana | Pedido del usuario; premisa "aspirante a murguista busca el bombo" |
| 2026-10-25 | Arte **placeholder geométrico por código** (`aventura/art.py`); se borraron los fondos PNG de la clase 6 | Pedido del usuario; sin problemas de licencia. Reemplazable por arte real |
| 2026-10-25 | Nuevo `engine/walkmask.py` (máscara de caminabilidad) | Requisito de zonas navegables; ver `wiki/motor/walkmask.md` |
| 2026-10-25 | `Inventory.combine`, `DialogueBox` con mouse + hooks, `DialogueManager` con color/center_at/wrap, todo marcado `# [Tarea 2026]` | Requisitos de combinación y diálogos con mouse |
| 2026-10-25 | Datos del juego en `aventura/data/` (rooms/dialogs/items) y una sola `GameScene` | Escenarios y puzles como datos; ver `wiki/diseno/escenarios-y-puzles.md` |
| 2026-10-25 | Game Over = perder la payada (3 errores); Victoria = coger el bombo | Define la condición de derrota pendiente |
| 2026-10-25 | Sonidos nuevos generados por `tools/gen_sonidos.py` (talk, combine, nope, bombo) | Feedback sonoro en toda interacción |
| 2026-10-25 | Chivito → **chori al pan** (el chivito va a la plancha; el chori a la parrilla) | Corrección del usuario |
| 2026-10-25 | Chiste del clima: "El Niño", primavera húmeda y lluviosa (hotspot Cielo, Pescador, diario, cartel, intro de Tano) | Pedido del usuario |
| 2026-10-25 | Chiste de la ropa que no se seca: hotspot Tendedero (Mercado) + opción del Pescador | Pedido del usuario |
| 2026-10-25 | Bombo con **un solo parche** (no tres), correa y mazo | Verificado contra murgas-del-uruguay.blogspot.com/2012/03/la-batea.html |
| 2026-10-25 | Verbo **Coger → Agarrar** | En Uruguay "coger" es vulgar; pedido del usuario |
| 2026-10-25 | Dichos populares incorporados a hotspots, diálogos y payada | Pedido del usuario; fuentes en `wiki/diseno/escenarios-y-puzles.md` |
| 2026-10-25 | `art.py` carga PNG de `assets/{fondos,sprites,objetos}/` si existen y cae al placeholder si faltan (`load_png`) | Reemplazar arte pieza por pieza sin tocar la lógica |
| 2026-10-25 | Skyline de `rambla.jpeg` convertido en silueta transparente (`tools/preparar_skyline.py`) y usado en el fondo de la Rambla | Pedido del usuario; fondo mantiene cielo/río/vereda dibujados por código |
| 2026-10-25 | `fondos/rambla.png` (aportado por el usuario) es el fondo completo de la Rambla; se eliminó el skyline anterior (`rambla.jpeg`, `skyline_rambla.png`, `tools/preparar_skyline.py` y su rama en `art.py`). `make_background` escala para cubrir y recorta alineado abajo en vez de estirar | Pedido del usuario; evita deformar imágenes de otra proporción |
| 2026-10-25 | Fondo de la Rambla "más tranquilo": `tools/simplificar_rambla.py` suaviza y tiñe la foto del usuario y la apoya en muro/vereda dibujados; el original queda en `fondos/originales/` | Pedido del usuario (la foto tenía demasiado detalle y competía con personajes y objetos) |
| 2026-10-25 | Fondo de la Rambla = pixel art creado con Pixellab (reemplaza la foto simplificada y `tools/simplificar_rambla.py`); zona navegable y hotspots de la Rambla reubicados sobre la vereda en perspectiva; la salida al Mercado pasa al fondo de la vereda; `make_background` escala sin suavizar el pixel art chico | Pedido del usuario |
| 2026-10-25 | Fondo del Mercado = pixel art Pixellab (`fondos/mercado.png`); zona caminable = pasillo central de piedra; puesto de yerba, parrilla y tendedero pasan a ser zonas sobre el dibujo (sin placeholder); salidas en las esquinas inferiores; puntos de aparición ajustados | Pedido del usuario |
| 2026-10-25 | Fondo del Tablado = pixel art Pixellab (`fondos/tablado.png`); sin piso libre, Tano camina por la franja inferior delante del público (+ calles laterales); Contramaestre y bombo quedan sobre el escenario, accesibles desde la franja; cartel = zona sobre la pancarta | Pedido del usuario |
| 2026-10-25 | Fondo del menú = pixel art Pixellab (`fondos/menu.png`) a pantalla completa (`make_background(room, target)`); título/subtítulo con contorno negro | Pedido del usuario; el menú mide 900×600 y la imagen era 900×450 (quedaba una franja negra) |
| 2026-10-25 | README público en `TAREA/README.md` + `capturas/` generadas por `tools/capturas.py`; regla en `AGENTS.md` §8 de mantenerlo siempre al día; correo del docente omitido | Pedido del usuario; el repo es público |
