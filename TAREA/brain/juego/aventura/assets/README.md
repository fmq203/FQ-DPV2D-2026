# Assets del juego

Si el PNG existe se usa; si falta, el juego dibuja el placeholder geométrico (`aventura/art.py`).
Se puede reemplazar pieza por pieza. **Todo asset externo se registra en
`wiki/entrega/assets-lista.md` con origen y licencia.**

| Carpeta | Archivo | Tamaño / convención |
|---|---|---|
| `fondos/` | `menu.png`, `rambla.png`, `mercado.png`, `tablado.png` | 900×450 px ideal. Otra proporción: se escala para cubrir y se recorta **alineada abajo** (el piso/horizonte queda abajo, el cielo se recorta) |
| `sprites/` | `tano_idle.png` | Mirando a la **derecha**, fondo transparente; se dibuja a ~110 px de alto (escala 0.7–1.1 según la profundidad), apoyado en los pies |
| `sprites/` | `tano_walk_0.png` … `tano_walk_3.png` | Frames de caminata consecutivos (cambia cada 6 ticks) |
| `sprites/` | `<id del hotspot>.png` | Se ajusta al **alto** del rect del hotspot, apoyado abajo. Ids: `banco`, `tacho`, `pescador`, `yerbas`, `parrilla`, `parrillero`, `gato`, `perro`, `contramaestre`, `bombo`. Sin `yerbas.png`/`parrilla.png` aparece un rectángulo «FALTA» |
| `sprites/` | `tacho_vacio.png`, `parrilla_prendida.png` | Variantes por estado (`sprite_if` en `data/rooms.py`): tacho sin diario, parrilla con fuego |
| `objetos/` | `termo.png`, `mate.png`, `yerba.png`, `mate_cargado.png`, `mate_listo.png`, `diario.png`, `choripan.png` | Cuadrados (se escalan a 48×48 en el inventario; el mismo PNG se usa para el objeto suelto en la escena) |
| `audio/` | `click, pickup, win, lose, talk, combine, nope, bombo` `.wav` + `musica_menu/rambla/mercado/tablado.wav` (un tema por lugar; el juego elige `musica_<room>.wav`) | Generados por código (`tools/gen_sonidos.py`, `tools/gen_musica.py`) |

**Hoy** todos los sprites e íconos son pixel art generado por `tools/gen_sprites.py`. Ojo: si se vuelve a correr ese script, **sobrescribe** los PNG que genera; si retocaste alguno a mano, no lo vuelvas a correr (o comentá ese sprite en `SPRITES`/`ICONOS`).

## Editar los sprites a mano (LibreSprite)
[LibreSprite](https://github.com/libresprite/libresprite) (gratis, derivado de Aseprite) abre los PNG directo:
1. Abrir el PNG (ej. `sprites/pescador.png`). Son chicos (≈ 20–60 px): hacer zoom ×8 o más.
2. Lápiz de 1 px, sin antialias. Mantener el fondo transparente y el contorno oscuro de 1 px.
3. Guardar como PNG con el **mismo nombre**. El juego lo agranda sin suavizar (~2,6×).
4. Se puede cambiar el tamaño del lienzo: el juego escala al alto del hotspot y conserva la proporción.

**Tamaño nativo recomendado (pixel art):** los fondos se agrandan ~2.6× (344×192 → 900×450), así que para que todo tenga el mismo "grosor de píxel" los sprites deben tener ~1/2.6 del tamaño en pantalla: Tano ≈ 42 px de alto, pescador ≈ 43, parrillero ≈ 36, contramaestre ≈ 35, perro ≈ 21 de alto, gato ≈ 15, bombo ≈ 19, banco ≈ 65×27, tacho ≈ 21×31, íconos de objetos 18–24 px cuadrados. Los sprites se agrandan sin suavizar.

Los hotspots (rects, puntos de parada, zona caminable) están en `aventura/data/rooms.py`:
si tu fondo tiene otra distribución, ajustá ahí las coordenadas.

Los cuatro fondos (**menú**, Rambla, Mercado y Tablado) son pixel art (Pixellab). El del menú se escala a pantalla completa (900×600); los de escena a 900×450.

`fondos/originales/` guarda fuentes sin usar (no se cargan en el juego). Los fondos de pixel art chico (≤450 px de ancho) se escalan sin suavizar.
