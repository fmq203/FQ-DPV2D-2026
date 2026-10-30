---
title: Hot cache
type: estado
sources: [AGENTS.md, MEMORY.md, juego/tests/smoke_test.py]
updated: 2026-10-30
---

# Estado actual (2026-10-30)

**Hecho — "El Murguista" completo y jugable** (avance ~95%)
- 3 escenarios conectados (Rambla de Barrio Sur, Mercado del Puerto, Museo del Carnaval) con zona navegable ([[walkmask]]); verbos + FSM ([[fsm-verbos]]); inventario con combinación ([[inventario-y-combinacion]]); diálogos con opciones y payada ([[sistema-dialogos]]); 3 puzles ([[escenarios-y-puzles]]), incluido el **mini-reto de la parrilla** en el Mercado (gato → leña → fogata → asar el chorizo a tiempo).
- Menú (Comenzar / **Créditos** / Salir), **pausa con ESC** (Continuar / Música / Menú), Game Over con **Reintentar payada**, Victoria.
- Arte: fondos Pixellab; **personajes, objetos e íconos en pixel art generado por código** (`tools/gen_sprites.py`, PNG editables con LibreSprite). **Música por lugar** generada por código (`tools/gen_musica.py`: menú, Rambla, Mercado, Museo).
- Entregables: `TAREA/README.md`, **`TAREA/DISENO.md`** (documento de diseño), **`TAREA/video/el-murguista.mp4`** (39,8 s, `tools/grabar_video.py`), [[assets-lista]], [[cambios-al-motor]].
- `tests/smoke_test.py` en verde: victoria, Game Over → reintentar → victoria, créditos, pausa, límites de la zona caminable.

**Siguiente** (entrega final 6-nov-2026)
1. El usuario va a revisar y personalizar a mano (sprites en LibreSprite, textos, créditos en `aventura/data/creditos.py`). Si retoca sprites, **no** volver a correr `gen_sprites.py`.
2. Tras cambios visibles: `tools/capturas.py` y `tools/grabar_video.py`.
3. Jugar una partida a mano; preparar la defensa ([[checklist-entrega]]).

**Idea abierta:** el docente recomienda mini-retos en **cada** pantalla; la Rambla todavía solo tiene recolección + diálogo.

**Bloqueos / gaps:** GitHub vs GitLab para la entrega; integrantes del grupo y mail al docente; términos de uso de Pixellab.
