---
title: Hot cache
type: estado
sources: [AGENTS.md, MEMORY.md, juego/tests/smoke_test.py]
updated: 2026-10-25
---

# Estado actual (2026-10-25)

**Hecho — "El Murguista" jugable de punta a punta** (avance ~85%)
- 3 escenarios conectados (Rambla de Barrio Sur, Mercado del Puerto, Museo del Carnaval) con zona navegable y click-to-walk ([[walkmask]]).
- FSM de verbos (Mirar/Agarrar/Usar/Hablar/Dar) + comando armado ([[fsm-verbos]]), inventario con combinación ([[inventario-y-combinacion]]), diálogos con opciones por mouse y duelo de payada ([[sistema-dialogos]]), 3 puzles ([[escenarios-y-puzles]]).
- Menú, Game Over (3 errores en la payada) y Victoria (coger el bombo), con volver al menú; sonido en toda interacción.
- Fondos: los 4 son pixel art (Pixellab). Personajes y objetos siguen como placeholders geométricos por código (`aventura/art.py`) por falta de generaciones gratuitas. Los atajos F1/F2 ya fueron eliminados.
- **README público** en `TAREA/README.md` con capturas (`tools/capturas.py`); se actualiza según [[checklist-entrega]] y la regla §8 de `AGENTS.md`.
- `tests/smoke_test.py` juega la partida completa (victoria y derrota) con eventos reales: en verde. `juego/.venv` creado.

**Siguiente** (entrega final 6-nov-2026)
1. Jugar a mano (`cd juego && .venv/bin/python -m aventura.main`) y ajustar ritmo/humor/textos.
2. Arte real opcional (reemplazar `art.py`; registrar en [[assets-lista]]) y música opcional.
3. README, documento de diseño, video 15–40 s, repo GitLab ([[checklist-entrega]]).

**Bloqueos / gaps:** integrantes del grupo; si se envió el mail al docente; estructura del repo GitLab; música.
