---
title: Máscara de caminabilidad y movimiento
type: diseno
sources: [raw/tarea-videojuegos-2026-v2.pdf]
updated: 2026-10-25
---

# Máscara de caminabilidad y movimiento

**Implementado** con [[walkmask]] (unión de rectángulos rasterizada en `pygame.mask`; clic fuera de zona → punto navegable más cercano; deslizamiento por bordes; escala del personaje por Y). Opciones del enunciado: polígonos de navegación o máscaras. Propuesta: una imagen en blanco/negro por escenario (`walk_<room>.png`) → `pygame.mask.from_threshold` / consulta de píxel; el personaje camina en línea recta hacia el clic si el punto es caminable; si no, hacia el punto caminable más cercano. Pathfinding (BFS sobre grilla gruesa de la máscara) como mejora. Escala del personaje por Y (profundidad) opcional.
Extensión nueva al motor: `engine/walkmask.py` ([[cambios-al-motor]]).
