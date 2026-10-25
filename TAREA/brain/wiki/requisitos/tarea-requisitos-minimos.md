---
title: Requisitos mínimos — Opción 1 Aventura gráfica
type: requisito
sources: [raw/tarea-videojuegos-2026-v2.pdf]
updated: 2026-10-25
---

# Requisitos mínimos — Opción 1 Aventura gráfica

Juego point-and-click estilo Monkey Island 1: exploración, recolección de objetos y acertijos. Complejidad **Alta**.

**Objetivo:** guiar al personaje por escenarios con el ratón, interactuar con el entorno, resolver puzles y avanzar la historia.

## Mínimos obligatorios
1. Interfaz point-and-click con **verbos de acción** (Mirar, Usar, Hablar, Coger…). → [[fsm-verbos]]
2. **Inventario** para guardar y **combinar** ítems. → [[inventario-y-combinacion]]
3. **≥ 3 escenarios interconectados** con zonas navegables por el personaje. → [[escenarios-y-puzles]], [[mascara-caminabilidad]]
4. **Diálogos con opciones múltiples** con NPCs. → [[sistema-dialogos]]
5. **≥ 2 puzles** para avanzar. → [[escenarios-y-puzles]]

## Orientación técnica (del enunciado)
- **Mecánicas:** máquina de estados finitos para acciones/interacciones; polígonos de navegación o máscaras de caminabilidad.
- **Colisiones:** clics sobre **hotspots** (rectángulos o máscaras). → [[hotspot]]
- **UI:** un `DialogueManager` para los textos flotantes + barra de comandos e inventario abajo. → [[dialogue-manager]]

Ver también [[requisitos-comunes]].
