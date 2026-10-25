---
title: Clase 6: aventura gráfica (aventura.py)
type: clase
sources: [raw/clase-6.ipynb, raw/clase-6-aventura.py]
updated: 2026-10-25
---

# Clase 6: aventura gráfica (aventura.py)

`aventura.py` es una aventura **de texto con botones** (no point-and-click): script único, 900×600, 30 FPS.

Ideas reutilizables:
- **Diccionario `historia`**: escena → `{texto, opciones:[{texto, destino, requiere, accion}]}`; `requiere` es un lambda que filtra opciones según inventario; `accion` ejecuta efectos (tomar/dar banana). → modelo de datos para diálogos ([[sistema-dialogos]]) y puzles.
- **Fondos por escena** `assets/fondos/<escena>.png` con color de respaldo y alias (cueva reusada por mono/cofre/tesoro).
- **Animación por frames sueltos** (`cargar_frames`, orden natural por número, `frame_actual` por tiempo `get_ticks()//intervalo`) para banana, mono, cofre (chest1-5 abriendo, 6-15 destellos).
- **Sonido click** opcional: si no existe el archivo, sigue en silencio.
- Historia: selva → cueva (mono + cofre) / río (banana) → aldea; puzle banana→mono→tesoro.

Limitaciones frente a la tarea: sin verbos, sin personaje caminando, sin inventario visual combinable, estado en variables globales. Assets disponibles en `Videojuegos/06/assets/` (fondos aldea/cueva/inicio/rio, banana, cofre, mono).
