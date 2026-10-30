---
title: Guion del video (15–40 s)
type: entrega
sources: [raw/tarea-videojuegos-2026-v2.pdf]
updated: 2026-10-30
---

# Guion del video (15–40 s)

0–3 s menú → Comenzar · 3–12 s caminar y Mirar/Agarrar en escenario 1 · 12–20 s inventario/combinar · 20–28 s diálogo con opciones · 28–35 s resolver puzle y cambiar de escenario · 35–40 s Victoria. Grabar con [[recorder]] + FFmpeg o con un grabador de pantalla; verificar duración.

**Hecho (2026-10-30):** `tools/grabar_video.py` juega este guion solo (reloj y mouse virtuales, caminatas a x2, corte en los dos últimos versos de la payada) y exporta `TAREA/video/el-murguista.mp4` (39,8 s, 900×600; incluye el mini-reto de la parrilla con un corte mientras se asa el chorizo; con la música de cada lugar y el jingle de victoria; sin los demás efectos). Requiere `pip install imageio-ffmpeg` en el venv (`juego/requirements-dev.txt`). Si se cambia el juego, volver a correrlo.
