---
title: engine/game_object.py — GameObject
type: motor
sources: [juego/engine/game_object.py]
updated: 2026-10-25
---

# engine/game_object.py — GameObject

`GameObject(x, y, frames, anim_speed=0.1)` hereda de `pygame.sprite.Sprite`. `frames` = `Surface` (estático) o lista (animado); `rect` centrado en (x,y); `update()` → `update_animation()` (acumula `anim_speed` por tick); `draw(surface)`. Las entidades hijas deben llamar `super().update()`.
En la aventura: personaje, NPCs, objetos animados (mono, cofre).
