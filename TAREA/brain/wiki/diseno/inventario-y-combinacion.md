---
title: Inventario y combinación de ítems
type: diseno
sources: [juego/engine/inventory.py]
updated: 2026-10-30
---

# Inventario y combinación de ítems

Barra inferior horizontal (estilo Monkey Island). Extender `Inventory`: panel horizontal + scroll si hay más ítems que slots; tabla de recetas `{frozenset({a,b}): resultado}`; el verbo *Usar* con ítem seleccionado sobre otro ítem o hotspot dispara la combinación. **Hecho:** panel horizontal y `Inventory.combine(a, b, recipes)`; recetas en `juego/aventura/data/items.py`; *Usar* ítem → clic en otro ítem combina ([[inventory]]). Registrar el cambio en [[cambios-al-motor]]. Una receta puede **conservar** ítems (`(resultado, mensaje, ("termo",))`): el termo sigue en el inventario después de cebar. Recetas: yerba+mate, mate cargado+termo, diario+leña (fuego), chorizo asado+pan (chori al pan).
