---
title: FSM de interacción con verbos
type: diseno
sources: [raw/tarea-videojuegos-2026-v2.pdf]
updated: 2026-10-25
---

# FSM de interacción con verbos

**Implementado** en `juego/aventura/scenes/game_scene.py` (docstring con el diagrama). Estados reales: `IDLE`, `WALKING`, `SPEAKING`, `DIALOGUE`; el comando se arma con `verb` + `pending` (ítem elegido para *Usar*/*Dar*). Verbos: Mirar, **Agarrar** (no "Coger": en Uruguay es vulgar), Usar, Hablar, Dar; clic en zona vacía = caminar; clic derecho cancela el ítem pendiente; las salidas viajan con cualquier verbo. Resolución en tabla `acts` por hotspot con clave `"Verbo"` o `"Verbo:item"` y respuestas por defecto. Propuesta original: estados `IDLE → VERBO_ELEGIDO → OBJETO1_ELEGIDO → (esperando OBJETO2 si el verbo es Usar/Dar) → EJECUTANDO → IDLE`, más `DIALOGO`, `CAMINANDO`, `CINEMATICA` (bloquean input).
- Verbos (9 como Monkey Island o reducido a 4–6): Mirar, Coger, Usar, Hablar, Abrir, Dar, Empujar…; el verbo por defecto es *Caminar a*.
- Línea de comando "Usar llave con puerta" se arma con los estados; clic derecho = acción por defecto del objeto.
- Resolución en tabla `(verbo, objeto[, objeto2]) → acción` (dict), con respuesta por defecto ("No puedo hacer eso") — análogo al `historia/ACCIONES` de [[clase-6-aventura-grafica]].
- Cada cambio de estado de UI reproduce sonido ([[audio]]).
