---
title: Clases 1-4: diseño, ventana, GameObject, colisiones
type: clase
sources: [raw/clase-1-4.ipynb]
updated: 2026-10-25
---

# Clases 1-4: diseño, ventana, GameObject, colisiones

- **Clase 1 — Diseñar:** 4 pilares: (1) objetivo claro, (2) reglas y limitaciones, (3) conflicto y desafío, (4) interacción y retroalimentación (*feedback*: "sin feedback el juego se siente muerto"). *Gameplay loop* acción → reacción/feedback → nuevo desafío. Géneros 2D: arcade, plataformas, **aventura gráfica**, objetos ocultos.
- **Género "Aventura gráfica" según la clase 1** (Monkey Island, Broken Sword): objetivo = resolver puzles para avanzar una historia; reglas = sin acción en tiempo real, se usan objetos del inventario en el escenario o con personajes; desafío = puzles lógicos; el motor necesita **gestión de estado** (qué puzles se resolvieron), **inventario** y **diálogos**. El género "objetos ocultos" aporta los **hotspots** (clic en áreas). → [[arquitectura-juego]], [[hotspot]].
- Loop de nuestra aventura: explorar → examinar → recoger → combinar/usar → hablar → desbloquear → nuevo escenario.
- **Clase 2 — Ventana y bucle:** `pygame.init`, `set_mode`, bucle INPUT → UPDATE → RENDER, `fill` + `flip`, coordenadas con (0,0) arriba-izquierda, colores RGB.
- **Clase 3 — Movimiento y clases:** `key.get_pressed`, agrupar estado en clases (`Player`) → base del `GameObject` del motor ([[game-object]]).
- **Clase 4 — Colisiones y puntaje:** segundo tipo de objeto (coleccionable), colisión por rects (`colliderect`), puntaje con `pygame.font.Font(...).render` + `blit`. Reusar `rect.collidepoint` para clics sobre [[hotspot]].

Lección de diseño que usamos: mantener `INPUT/UPDATE/RENDER` separados (ver [[game-loop]]).
