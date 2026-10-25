# LEARNINGS — lecciones aprendidas

- (2026-10-25) El `Game` del motor instancia la escena **de nuevo** en cada `change_scene` → el estado persistente (inventario, flags de puzles) NO debe vivir en la escena sino en el objeto `game` (ej. `game.state`). Fuente: `juego/engine/game_loop.py`.
- (2026-10-25) `change_scene` es diferido: se aplica al inicio del siguiente `update`; no asumir cambio inmediato.
- (2026-10-25) `AudioManager.play_sound` ignora en silencio nombres no cargados → un sonido faltante no da error pero incumple el requisito de feedback sonoro.
- (2026-10-25) `Inventory` del motor era solo vertical: con 8 slots el panel se salía de la pantalla debajo de la barra. Se agregó `horizontal=True` ([[cambios-al-motor]]).
- (2026-10-25) `Cursor.draw` oculta el puntero del sistema y nunca lo restaura: al salir de la escena con cursor hay que llamar `pygame.mouse.set_visible(True)` (en `on_exit`); si no, el menú queda sin puntero.
- (2026-10-25) Al ingerir una fuente, leerla **completa**: un resumen hecho sobre los primeros párrafos dejó afuera contenido útil de la clase 5.
- (2026-10-25) `DialogueBox._go_to` ejecuta `node.action` **antes** de envolver el texto: permite nodos dinámicos (texto/opciones calculados en la acción, ej. la payada con vidas). Fuente: `juego/engine/dialogue.py`.
- (2026-10-25) Un test de humo que juega con eventos reales de mouse (postear `MOUSEBUTTONDOWN` y avanzar frames) detecta errores de flujo (ej. diálogo que no cierra) que un test de funciones no ve.
