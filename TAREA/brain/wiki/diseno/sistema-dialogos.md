---
title: Sistema de diálogos
type: diseno
sources: [juego/engine/dialogue.py, raw/clase-6-aventura.py]
updated: 2026-10-25
---

# Sistema de diálogos

**Hecho:** `DialogueBox` con mouse y `DialogueNode` (nodos en `juego/aventura/data/dialogs.py`; los textos de verbos/NPC flotan con `DialogueManager` sobre el hablante, con color por personaje). Plan original: usar `DialogueNode` (texto, hablante, opciones → siguiente nodo, `action` al entrar) como árbol por NPC, con opciones condicionadas por inventario/flags (estilo `requiere` de la clase 6). Mostrar el texto **flotante sobre el personaje/NPC** con `DialogueManager` y las opciones en el panel inferior, seleccionables con **mouse**. Cada selección → sonido. Ver [[dialogue-manager]].
