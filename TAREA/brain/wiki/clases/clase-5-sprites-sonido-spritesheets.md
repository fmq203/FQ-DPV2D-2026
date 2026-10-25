---
title: "Clase 5: sprites, sonido y spritesheets"
type: clase
sources: [raw/clase-5.ipynb]
updated: 2026-10-25
---

# Clase 5: sprites, sonido y spritesheets

## Parte 1 — De rectángulos a sprites
- Separar **`self.image`** (lo que se ve) de **`self.rect`** (caja invisible para lógica y colisiones). Las colisiones siguen funcionando igual porque dependen del `rect`.
- `pygame.image.load(...).convert_alpha()` para PNG con transparencia (`.convert()` sin transparencia); `image.get_rect()` da el tamaño; dibujar con `blit(self.image, self.rect)`.
- Guardar los recursos en una carpeta `assets/`.

## Parte 2 y 3 — Sonido y música
- `pygame.mixer.init()` una vez al inicio.
- **Efectos cortos:** `pygame.mixer.Sound(path)` cargados antes del bucle, `.play()` en el momento del evento; pueden sonar varios a la vez.
- **Música:** `pygame.mixer.music` es un único canal en streaming para pistas largas (una a la vez). En el motor esto está encapsulado en [[audio]].
- El ejemplo usa un estado de juego por string (`estado_juego = 'jugando' | 'game_over'`): forma mínima de máquina de estados, antecedente de las escenas del motor ([[game-loop]]).

## Extras — Spritesheets
- Una imagen grande con muchos sprites; se recorta con `spritesheet.subsurface(Rect)`. En grilla regular se calcula `x = col * ancho`, `y = fila * alto`.
- Herramientas: TexturePacker / free-tex-packer, ShoeBox, LibreSprite, Piskel, ezgif, spritefusion (tiles).
- **Editor del curso:** `https://github.com/apastorini/sprites_label/blob/main/editor.py` (versión tkinter también en el notebook de la clase 8). Clic izquierdo marca, clic derecho guarda nombre/descripción, se agrupan sprites en animaciones (`idle`, `walk`…) y se guarda un **JSON** `{spritesheet_path, animations:{nombre:[{name,x,y,width,height}]}}`. **El JSON y la imagen deben estar en la misma carpeta.** Lo lee `Spritesheet` del motor ([[asset-manager]]).
- **Animación por acción:** el `Player` cambia de animación según lo que hace (`walk` si se mueve, `idle` si no) y reinicia el frame al cambiar. En la aventura: `idle` / `walk_left` / `walk_right` / `talk` del personaje. El `GameObject` del motor ([[game-object]]) maneja una sola lista de frames, así que el cambio de animación lo hace la entidad reasignando `frames`.

## Fuentes de assets que recomienda la clase
craftpix.net, itch.io/game-assets, gameart2d.com/freebies, laredgames.itch.io; sonido: pixabay.com/sound-effects, freesound.org, bfxr.net; música: fesliyanstudios.com (8-bit), opengameart.org. Registrar origen y licencia en [[assets-lista]].

Nota: el notebook de la clase 6 repite este contenido casi sin cambios; lo propio de la clase 6 es `aventura.py` ([[clase-6-aventura-grafica]]).
