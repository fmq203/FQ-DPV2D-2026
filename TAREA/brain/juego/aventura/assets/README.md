# Assets del juego

Si el PNG existe se usa; si falta, el juego dibuja el placeholder geométrico (`aventura/art.py`).
Se puede reemplazar pieza por pieza. **Todo asset externo se registra en
`wiki/entrega/assets-lista.md` con origen y licencia.**

| Carpeta | Archivo | Tamaño / convención |
|---|---|---|
| `fondos/` | `menu.png`, `rambla.png`, `mercado.png`, `tablado.png` | 900×450 px ideal. Otra proporción: se escala para cubrir y se recorta **alineada abajo** (el piso/horizonte queda abajo, el cielo se recorta) |
| `sprites/` | `tano_idle.png` | Mirando a la **derecha**, fondo transparente; se dibuja a ~110 px de alto (escala 0.7–1.1 según la profundidad), apoyado en los pies |
| `sprites/` | `tano_walk_0.png`, `tano_walk_1.png`, … | Frames de caminata consecutivos (opcional; cambia cada 6 ticks) |
| `sprites/` | `<id del hotspot>.png` | Se ajusta al **alto** del rect del hotspot, apoyado abajo. Ids: `banco`, `tacho`, `pescador`, `yerbas` (hoy: rectángulo verde «FALTA»), `parrilla` (hoy: rectángulo rojo «FALTA»), `parrillero`, `tendedero`, `gato`, `cartel`, `perro`, `contramaestre`, `bombo` |
| `objetos/` | `termo.png`, `mate.png`, `yerba.png`, `mate_cargado.png`, `mate_listo.png`, `diario.png`, `choripan.png` | Cuadrados (se escalan a 48×48 en el inventario; el mismo PNG se usa para el objeto suelto en la escena) |
| `audio/` | `click, pickup, win, lose, talk, combine, nope, bombo` `.wav` | Ya incluidos (generados por código) |

**Tamaño nativo recomendado (pixel art):** los fondos se agrandan ~2.6× (344×192 → 900×450), así que para que todo tenga el mismo "grosor de píxel" los sprites deben tener ~1/2.6 del tamaño en pantalla: Tano ≈ 42 px de alto, pescador ≈ 43, parrillero ≈ 36, contramaestre ≈ 35, perro ≈ 21 de alto, gato ≈ 15, bombo ≈ 19, banco ≈ 65×27, tacho ≈ 21×31, íconos de objetos 18–24 px cuadrados. Los sprites se agrandan sin suavizar.

Los hotspots (rects, puntos de parada, zona caminable) están en `aventura/data/rooms.py`:
si tu fondo tiene otra distribución, ajustá ahí las coordenadas.

Los cuatro fondos (**menú**, Rambla, Mercado y Tablado) ya son pixel art (Pixellab). El del menú se escala a pantalla completa (900×600); los de escena a 900×450.

`fondos/originales/` guarda fuentes sin usar (no se cargan en el juego). Los fondos de pixel art chico (≤450 px de ancho) se escalan sin suavizar.
