# aventura/art.py
"""
Arte del juego. Si existe el PNG en `assets/` se usa; si no, se dibuja un
placeholder geométrico con pygame.draw. Así se reemplaza pieza por pieza.
Nombres y tamaños esperados: ver assets/README.md.
"""
import math
import os

import pygame

W, H = 900, 450  # área de escena (la barra de comandos ocupa y >= 450)
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
TANO_ALTO = 110  # alto en px de Tano con escala 1.0 (la escala real va de 0.7 a 1.1)
_cache = {}


def load_png(subdir, name):
    """Devuelve la imagen assets/<subdir>/<name>.png o None si no existe (con caché)."""
    key = (subdir, name)
    if key not in _cache:
        path = os.path.join(ASSETS_DIR, subdir, f"{name}.png")
        img = None
        if os.path.isfile(path):
            try:
                img = pygame.image.load(path).convert_alpha()
            except pygame.error as e:
                print(f"No se pudo cargar {path}: {e}")
        _cache[key] = img
    return _cache[key]


def _scaled(img, size):
    """Pixel art chico (se agranda ≥ 1.5x): sin suavizar para conservar píxeles nítidos."""
    big = size[0] >= img.get_width() * 1.5 or size[1] >= img.get_height() * 1.5
    return (pygame.transform.scale if big else pygame.transform.smoothscale)(img, size)


def _fit_height(img, height):
    w = max(1, round(img.get_width() * height / img.get_height()))
    return _scaled(img, (w, max(1, round(height))))


def make_background(room, target=(W, H)):
    """Fondo de `room` del tamaño `target` (por defecto el área de escena; el menú usa pantalla completa)."""
    tw, th = target
    img = load_png("fondos", room)
    if img:
        if img.get_size() == target:
            return img
        # otra proporción: escalar para cubrir y recortar, alineado abajo (conserva horizonte y piso)
        k = max(tw / img.get_width(), th / img.get_height())
        size = (round(img.get_width() * k), round(img.get_height() * k))
        # pixel art chico: escalado sin suavizar para conservar los píxeles nítidos
        scale = pygame.transform.scale if img.get_width() * 2 <= tw else pygame.transform.smoothscale
        big = scale(img, size)
        return big.subsurface(((big.get_width() - tw) // 2, big.get_height() - th, tw, th)).copy()
    bg = _placeholder_background(room)
    return bg if target == (W, H) else pygame.transform.scale(bg, target)


def draw_prop(surf, kind, rect, color, sprite_id=None, flip=False):
    """Dibuja un hotspot: sprites/<sprite_id>.png (alto = alto del rect, apoyado abajo) o placeholder.
    flip=True lo espeja (p. ej. un animal que se va caminando hacia el otro lado)."""
    img = load_png("sprites", sprite_id) if sprite_id and kind not in ("zone", "item") else None
    if kind == "marker" and not img:
        return _marker(surf, rect, color, sprite_id)
    if img:
        img = _fit_height(img, pygame.Rect(rect).height)
        if flip:
            img = pygame.transform.flip(img, True, False)
        surf.blit(img, img.get_rect(midbottom=pygame.Rect(rect).midbottom))
    else:
        _placeholder_prop(surf, kind, rect, color)


def _marker(surf, rect, color, label):
    """Recordatorio visible de un sprite pendiente: rectángulo de color con el id del hotspot.
    Desaparece solo cuando se agrega assets/sprites/<id>.png."""
    r = pygame.Rect(rect)
    box = pygame.Surface(r.size, pygame.SRCALPHA)
    box.fill((*color, 150))
    surf.blit(box, r)
    pygame.draw.rect(surf, color, r, 3)
    txt = pygame.font.Font(None, 22).render(f"FALTA: {label}", True, (255, 255, 255))
    surf.blit(txt, txt.get_rect(center=r.center))


def make_icon(key, size=48):
    img = load_png("objetos", key)
    if img:
        return _scaled(img, (size, size))
    return _placeholder_icon(key, size)


def _walk_frames():
    frames, i = [], 0
    while True:
        f = load_png("sprites", f"tano_walk_{i}")
        if f is None:
            return frames
        frames.append(f)
        i += 1


def draw_tano(surf, feet, scale=1.0, facing=1, t=0, walking=False, speaking=False):
    """Tano: sprites/tano_idle.png (+ tano_walk_0..N.png) mirando a la derecha, o placeholder."""
    idle = load_png("sprites", "tano_idle")
    if idle is None:
        return _placeholder_tano(surf, feet, scale, facing, t, walking, speaking)
    frames = _walk_frames() if walking else []
    img = frames[(t // 6) % len(frames)] if frames else idle
    img = _fit_height(img, TANO_ALTO * scale)
    if facing < 0:
        img = pygame.transform.flip(img, True, False)
    surf.blit(img, img.get_rect(midbottom=(int(feet[0]), int(feet[1]))))


def _gradient(surf, rect, top, bottom):
    r = pygame.Rect(rect)
    for y in range(r.height):
        t = y / max(1, r.height - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        pygame.draw.line(surf, c, (r.x, r.y + y), (r.right, r.y + y))


def _skyline(surf, base_y, color, seed=0):
    x = 0
    while x < W:
        w = 40 + (x * 7 + seed * 13) % 50
        h = 50 + (x * 13 + seed * 29) % 90
        pygame.draw.rect(surf, color, (x, base_y - h, w, h))
        x += w + 4


def _salvo(surf, x, base_y, color):
    """Silueta estilizada del Palacio Salvo."""
    pygame.draw.rect(surf, color, (x - 40, base_y - 150, 80, 150))
    pygame.draw.rect(surf, color, (x - 28, base_y - 200, 56, 50))
    pygame.draw.rect(surf, color, (x - 16, base_y - 245, 32, 45))
    pygame.draw.polygon(surf, color, [(x - 12, base_y - 245), (x + 12, base_y - 245), (x, base_y - 275)])
    pygame.draw.line(surf, color, (x, base_y - 275), (x, base_y - 310), 3)


def _placeholder_background(room):
    s = pygame.Surface((W, H))
    if room == "menu":
        _gradient(s, (0, 0, W, H), (15, 15, 45), (70, 40, 90))
        pygame.draw.circle(s, (240, 235, 200), (730, 90), 38)
        _skyline(s, 400, (25, 20, 50), 1)
        _salvo(s, 200, 400, (18, 14, 38))
        pygame.draw.rect(s, (12, 10, 28), (0, 400, W, 50))
    elif room == "rambla":
        _gradient(s, (0, 0, W, 190), (250, 170, 90), (255, 220, 150))
        pygame.draw.circle(s, (255, 245, 200), (620, 170), 46)
        _skyline(s, 215, (150, 110, 120), 3)
        _gradient(s, (0, 190, W, 70), (170, 130, 95), (140, 105, 75))   # Río de la Plata
        pygame.draw.rect(s, (200, 195, 185), (0, 255, W, 40))             # muro de la rambla
        pygame.draw.rect(s, (160, 155, 145), (0, 290, W, 6))
        pygame.draw.rect(s, (205, 180, 150), (0, 296, W, H - 296))         # vereda
        for x in range(0, W, 90):
            pygame.draw.line(s, (185, 160, 130), (x, 296), (x - 40, H), 2)
        for x in (60, 420, 780):                                           # faroles
            pygame.draw.rect(s, (60, 60, 70), (x, 150, 6, 145))
            pygame.draw.circle(s, (255, 235, 150), (x + 3, 148), 11)
    elif room == "mercado":
        _gradient(s, (0, 0, W, 300), (120, 70, 50), (170, 110, 70))
        for x in range(0, W, 60):                                          # ladrillos
            for y in range(0, 300, 30):
                off = 30 if (y // 30) % 2 else 0
                pygame.draw.rect(s, (105, 58, 42), (x + off, y, 58, 28), 1)
        for x in (150, 450, 750):                                          # arcos de hierro
            pygame.draw.rect(s, (35, 40, 45), (x - 8, 40, 16, 260))
            pygame.draw.arc(s, (35, 40, 45), (x - 150, 20, 300, 120), 0, math.pi, 8)
        pygame.draw.rect(s, (60, 50, 45), (0, 40, W, 12))
        pygame.draw.rect(s, (150, 135, 120), (0, 300, W, H - 300))          # piso
        for x in range(0, W, 80):
            pygame.draw.line(s, (125, 110, 98), (x, 300), (x - 30, H), 2)
    elif room == "tablado":
        _gradient(s, (0, 0, W, 300), (10, 12, 35), (45, 30, 70))
        pygame.draw.circle(s, (235, 235, 210), (140, 70), 28)
        _skyline(s, 300, (22, 20, 45), 5)
        pygame.draw.rect(s, (80, 55, 40), (480, 200, 400, 110))            # escenario de madera
        pygame.draw.rect(s, (110, 78, 55), (480, 200, 400, 14))
        for x in (500, 860):
            pygame.draw.rect(s, (60, 40, 30), (x - 6, 90, 12, 120))
        for i in range(24):                                                  # guirnalda de luces
            x = 20 + i * 38
            y = 60 + int(math.sin(i * 0.5) * 12)
            pygame.draw.circle(s, [(255, 90, 90), (255, 220, 80), (90, 200, 255)][i % 3], (x, y), 6)
        pygame.draw.rect(s, (55, 50, 60), (0, 300, W, H - 300))             # adoquines
        for x in range(0, W, 60):
            pygame.draw.line(s, (40, 36, 46), (x, 300), (x - 20, H), 2)
    return s


# --------------------------------------------------------------------------- #
#  Props (hotspots) y personajes
# --------------------------------------------------------------------------- #
def _placeholder_prop(surf, kind, rect, color):
    r = pygame.Rect(rect)
    if kind == "person":
        pygame.draw.ellipse(surf, color, (r.x + r.w * 0.15, r.y + r.h * 0.3, r.w * 0.7, r.h * 0.7))
        pygame.draw.circle(surf, (235, 190, 150), (r.centerx, r.y + r.h * 0.2), min(r.w, r.h) * 0.22)
        pygame.draw.rect(surf, (40, 30, 30), (r.centerx - r.w * 0.2, r.y + r.h * 0.0, r.w * 0.4, r.h * 0.08))
    elif kind == "stall":
        pygame.draw.rect(surf, color, r)
        pygame.draw.rect(surf, (240, 240, 235), (r.x - 6, r.y - 12, r.w + 12, 18))
        pygame.draw.rect(surf, (30, 30, 30), r, 2)
    elif kind == "grill":
        pygame.draw.rect(surf, (45, 45, 50), (r.x, r.y + r.h * 0.45, r.w, r.h * 0.55))
        pygame.draw.rect(surf, color, (r.x + 8, r.y + r.h * 0.4, r.w - 16, r.h * 0.12))
    elif kind == "bench":
        pygame.draw.rect(surf, color, (r.x, r.y + r.h * 0.35, r.w, r.h * 0.2))
        pygame.draw.rect(surf, color, (r.x, r.y, r.w, r.h * 0.18))
        for x in (r.x + 10, r.right - 14):
            pygame.draw.rect(surf, (60, 40, 30), (x, r.y + r.h * 0.5, 6, r.h * 0.5))
    elif kind == "bin":
        pygame.draw.rect(surf, color, (r.x + 6, r.y + 18, r.w - 12, r.h - 18))
        pygame.draw.rect(surf, (70, 80, 70), (r.x, r.y + 10, r.w, 10))
        pygame.draw.rect(surf, (225, 220, 205), (r.x + 14, r.y + 2, 26, 14))  # diario asomando
    elif kind == "dog":
        pygame.draw.ellipse(surf, color, (r.x, r.y + r.h * 0.25, r.w * 0.8, r.h * 0.6))
        pygame.draw.circle(surf, color, (int(r.right - r.w * 0.15), int(r.y + r.h * 0.3)), int(r.h * 0.28))
        for x in (r.x + 8, r.x + r.w * 0.55):
            pygame.draw.rect(surf, color, (x, r.y + r.h * 0.7, 8, r.h * 0.3))
    elif kind == "cat":
        pygame.draw.ellipse(surf, color, (r.x, r.y + r.h * 0.3, r.w * 0.8, r.h * 0.6))
        pygame.draw.circle(surf, color, (int(r.right - r.w * 0.22), int(r.y + r.h * 0.35)), int(r.h * 0.28))
        pygame.draw.polygon(surf, color, [(r.right - 30, r.y + 8), (r.right - 24, r.y - 2), (r.right - 18, r.y + 8)])
    elif kind == "poster":
        pygame.draw.rect(surf, color, r)
        pygame.draw.rect(surf, (255, 255, 255), r, 3)
        for i in range(3):
            pygame.draw.line(surf, (255, 255, 255), (r.x + 12, r.y + 22 + i * 18), (r.right - 12, r.y + 22 + i * 18), 3)
    elif kind == "drum":
        pygame.draw.ellipse(surf, color, (r.x, r.y + r.h * 0.5, r.w, r.h * 0.5))
        pygame.draw.rect(surf, color, (r.x, r.y + r.h * 0.25, r.w, r.h * 0.5))
        pygame.draw.ellipse(surf, (240, 230, 200), (r.x, r.y, r.w, r.h * 0.5))
        pygame.draw.ellipse(surf, (0, 0, 0), (r.x, r.y, r.w, r.h * 0.5), 2)
    elif kind == "item":  # objeto suelto: su ícono de inventario, cuadrado y apoyado abajo
        side = min(r.w, r.h)
        img = load_png("objetos", color)
        icon = _scaled(img, (side, side)) if img else make_icon(color, side)
        surf.blit(icon, icon.get_rect(midbottom=r.midbottom))
    elif kind == "clothes":  # tendedero con ropa goteando
        pygame.draw.line(surf, (60, 60, 60), (r.x, r.y + 10), (r.right, r.y + 20), 2)
        for i, c in enumerate(((220, 80, 80), (80, 140, 220), (240, 220, 90), (150, 200, 120))):
            x = r.x + 20 + i * 55
            pygame.draw.rect(surf, c, (x, r.y + 14 + i * 2, 34, 42))
            pygame.draw.circle(surf, (110, 170, 230), (x + 17, r.y + 64 + i * 2), 3)  # gota
    elif kind == "zone":  # zona sin dibujo (el fondo ya la muestra)
        pass


def _placeholder_icon(key, size=48):
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    if key == "termo":
        pygame.draw.rect(s, (60, 110, 190), (14, 10, 20, 34), border_radius=5)
        pygame.draw.rect(s, (200, 200, 205), (14, 6, 20, 8), border_radius=3)
    elif key == "mate" or key in ("mate_cargado", "mate_listo"):
        pygame.draw.ellipse(s, (120, 80, 40), (10, 14, 28, 30))
        pygame.draw.ellipse(s, (60, 140, 50) if key != "mate" else (40, 25, 15), (14, 12, 20, 9))
        pygame.draw.line(s, (200, 200, 200), (26, 16), (36, 4), 3)
        if key == "mate_listo":
            for dx in (-6, 0, 6):
                pygame.draw.arc(s, (230, 230, 240), (20 + dx, 0, 8, 12), 0, math.pi, 2)
    elif key == "yerba":
        pygame.draw.polygon(s, (60, 140, 60), [(10, 12), (38, 12), (42, 44), (6, 44)])
        pygame.draw.rect(s, (240, 240, 200), (14, 24, 20, 10))
    elif key == "diario":
        pygame.draw.rect(s, (225, 220, 205), (8, 8, 32, 34))
        for y in (14, 22, 30, 36):
            pygame.draw.line(s, (90, 90, 90), (12, y), (36, y), 2)
    elif key == "choripan":
        pygame.draw.ellipse(s, (225, 170, 90), (4, 16, 40, 20))        # pan
        pygame.draw.ellipse(s, (160, 60, 45), (1, 20, 46, 11))          # chorizo asomando
        pygame.draw.line(s, (110, 35, 30), (8, 25), (40, 25), 2)
        pygame.draw.ellipse(s, (225, 170, 90), (4, 26, 40, 12))
    else:
        pygame.draw.rect(s, (200, 50, 200), (8, 8, 32, 32), 2)
    return s


def _placeholder_tano(surf, feet, scale=1.0, facing=1, t=0, walking=False, speaking=False):
    """Tano, aspirante a murguista: cuerpo-cápsula con galera y bufanda."""
    x, y = feet
    bob = abs(math.sin(t * 0.25)) * 4 * scale if walking else 0
    y = y - bob
    sw = int(14 * scale)
    leg = math.sin(t * 0.25) * 5 * scale if walking else 0
    pygame.draw.line(surf, (30, 30, 60), (x - 5 * scale, y - 24 * scale), (x - 5 * scale + leg, y), int(5 * scale))
    pygame.draw.line(surf, (30, 30, 60), (x + 5 * scale, y - 24 * scale), (x + 5 * scale - leg, y), int(5 * scale))
    pygame.draw.rect(surf, (200, 40, 70), (x - sw, y - 66 * scale, sw * 2, 44 * scale), border_radius=int(8 * scale))
    pygame.draw.rect(surf, (255, 220, 0), (x - sw, y - 52 * scale, sw * 2, 5 * scale))
    head = (int(x), int(y - 76 * scale))
    pygame.draw.circle(surf, (235, 190, 150), head, int(11 * scale))
    pygame.draw.rect(surf, (25, 25, 30), (x - 13 * scale, head[1] - 17 * scale, 26 * scale, 7 * scale))
    pygame.draw.rect(surf, (25, 25, 30), (x - 8 * scale, head[1] - 30 * scale, 16 * scale, 15 * scale))
    pygame.draw.circle(surf, (20, 20, 20), (int(x + 4 * scale * facing), head[1] - 1), max(1, int(2 * scale)))
    if speaking:
        pygame.draw.line(surf, (60, 20, 20), (x + 2 * scale * facing, head[1] + 6 * scale),
                         (x + 8 * scale * facing, head[1] + 6 * scale), 2)
