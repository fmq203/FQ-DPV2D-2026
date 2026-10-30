"""Genera los sprites y los íconos en pixel art por código (PNG chicos con contorno oscuro).
El juego los agranda sin suavizar (~2.6x, igual que los fondos de Pixellab).
Son PNG comunes: se pueden retocar a mano con cualquier editor (Aseprite, Piskel, GIMP...)
o reemplazar por arte nuevo con el mismo nombre. Si se borra uno, vuelve el placeholder.
Uso: juego/.venv/bin/python tools/gen_sprites.py   (desde brain/)
Ojo: sobrescribe los PNG que genera (lista en SPRITES e ICONOS)."""
import os

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "juego", "aventura", "assets")

# Paleta
NEGRO, BLANCO, CONTORNO = (20, 18, 24), (240, 238, 230), (24, 18, 28)
PIEL, PIEL_D = (235, 188, 145), (200, 150, 110)
ROJO, ROJO_D = (205, 45, 70), (150, 30, 50)
AMARILLO, AMARILLO_D = (245, 205, 45), (200, 155, 25)
AZUL, AZUL_D = (45, 90, 170), (30, 60, 125)
VERDE, VERDE_D = (65, 155, 70), (40, 105, 50)
MADERA, MADERA_D, MADERA_L = (150, 100, 60), (105, 68, 40), (180, 130, 80)
HIERRO, HIERRO_D = (70, 72, 80), (45, 46, 52)
GRIS, PLATA = (165, 165, 170), (205, 208, 215)
PAPEL, CREMA = (225, 220, 200), (240, 225, 185)
CHORIZO, PAN = (150, 50, 40), (220, 165, 90)
LADRILLO, LADRILLO_D = (160, 75, 50), (115, 50, 35)


def lienzo(w, h):
    return pygame.Surface((w, h), pygame.SRCALPHA)


def R(s, c, x, y, w=1, h=1):
    s.fill(c, (x, y, w, h))


def linea(s, c, a, b, ancho=1):
    pygame.draw.line(s, c, a, b, ancho)


def contorno(s, color=CONTORNO):
    """Agrega 1 px de contorno alrededor de todo lo opaco (estilo pixel art); lo semitransparente (humo) no."""
    w, h = s.get_size()
    out = lienzo(w + 2, h + 2)
    for x in range(w):
        for y in range(h):
            if s.get_at((x, y)).a == 255:
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    out.set_at((x + 1 + dx, y + 1 + dy), color)
    out.blit(s, (1, 1))
    return out


# ------------------------------------------------------------------ personajes
def tano(frame=None):
    """Tano, aspirante a murguista: galera, traje de murga con retazos. Mira a la derecha.
    frame None = quieto; 0..3 = caminata."""
    s = lienzo(16, 40)
    bob = 1 if frame in (1, 3) else 0
    # galera
    R(s, NEGRO, 4, 0 + bob, 8, 7); R(s, AMARILLO, 4, 5 + bob, 8, 1); R(s, NEGRO, 2, 7 + bob, 12, 1)
    # cara
    R(s, (70, 45, 30), 4, 8 + bob, 2, 5)
    R(s, PIEL, 6, 8 + bob, 6, 8); R(s, PIEL, 12, 11 + bob, 1, 2)
    R(s, NEGRO, 9, 10 + bob); R(s, (150, 60, 60), 9, 14 + bob, 2, 1)
    R(s, PIEL_D, 7, 16 + bob, 3, 1)
    # traje de retazos
    R(s, ROJO, 3, 17 + bob, 10, 12)
    R(s, AZUL, 3, 18 + bob, 3, 3); R(s, VERDE, 9, 22 + bob, 3, 3); R(s, AZUL, 5, 25 + bob, 3, 3)
    R(s, AMARILLO, 3, 21 + bob, 10, 1); R(s, AMARILLO, 3, 28 + bob, 10, 1)
    R(s, BLANCO, 6, 17 + bob, 5, 1); R(s, BLANCO, 8, 18 + bob)            # moña
    R(s, ROJO_D, 10, 18 + bob, 2, 9); R(s, BLANCO, 10, 27 + bob, 3, 2)   # brazo y guante
    R(s, ROJO_D, 3, 29 + bob, 9, 1)
    # piernas
    pant = (40, 40, 80)
    if frame in (0, 2):  # piernas abiertas
        for r in range(8 - bob):
            R(s, pant, 5 - r // 3, 30 + bob + r, 3, 1)
            R(s, pant, 8 + r // 3, 30 + bob + r, 3, 1)
        R(s, NEGRO, 1, 38, 4, 2); R(s, NEGRO, 10, 38, 5, 2)
    elif frame in (1, 3):  # piernas juntas (paso)
        R(s, pant, 6, 31, 4, 7); R(s, NEGRO, 5, 38, 6, 2)
    else:
        R(s, pant, 4, 30, 3, 8); R(s, pant, 9, 30, 3, 8)
        R(s, NEGRO, 3, 38, 4, 2); R(s, NEGRO, 9, 38, 5, 2)
    return s


def pescador():
    """Impermeable amarillo (El Niño), barba gris y caña hacia el río."""
    s = lienzo(24, 42)
    linea(s, MADERA_D, (16, 21), (23, 0))            # caña
    R(s, AMARILLO, 5, 2, 9, 4); R(s, AMARILLO_D, 3, 6, 13, 2)
    R(s, PIEL, 6, 8, 7, 7); R(s, PIEL, 13, 11)
    R(s, (200, 200, 205), 6, 12, 8, 5); R(s, NEGRO, 10, 10)
    R(s, AMARILLO, 4, 17, 12, 16); R(s, AMARILLO_D, 4, 17, 2, 16)
    for y in (20, 24, 28):
        R(s, NEGRO, 11, y)
    R(s, AMARILLO_D, 11, 19, 5, 3); R(s, PIEL, 16, 20, 1, 2)
    botas = (40, 70, 55)
    R(s, botas, 5, 33, 4, 7); R(s, botas, 11, 33, 4, 7)
    R(s, (25, 45, 35), 4, 39, 6, 3); R(s, (25, 45, 35), 10, 39, 6, 3)
    return s


def asador():
    """Boina, bigote, panza y delantal; pinza en la mano."""
    s = lienzo(22, 36)
    R(s, NEGRO, 5, 1, 10, 3); R(s, NEGRO, 9, 0)
    R(s, PIEL, 6, 4, 8, 7); R(s, PIEL, 14, 7, 1, 2); R(s, NEGRO, 11, 6)
    R(s, (60, 40, 30), 9, 9, 6, 1)
    R(s, BLANCO, 3, 11, 15, 15); R(s, BLANCO, 2, 15, 17, 9)
    R(s, ROJO_D, 5, 14, 11, 14); R(s, ROJO_D, 7, 11, 1, 3); R(s, ROJO_D, 13, 11, 1, 3)
    R(s, (230, 230, 225), 15, 13, 3, 7); R(s, PIEL, 15, 20, 3, 2)
    linea(s, PLATA, (17, 22), (21, 28)); linea(s, PLATA, (18, 22), (21, 26))
    R(s, (50, 50, 60), 6, 28, 4, 6); R(s, (50, 50, 60), 12, 28, 4, 6)
    R(s, NEGRO, 5, 34, 5, 2); R(s, NEGRO, 12, 34, 6, 2)
    return s


def contramaestre():
    """Director de murga: galera con cinta de colores, levita con galones y bigotazo."""
    s = lienzo(20, 35)
    R(s, NEGRO, 5, 0, 9, 6)
    for i, c in enumerate((ROJO, AMARILLO, VERDE, AZUL, ROJO, AMARILLO, VERDE, AZUL, ROJO)):
        R(s, c, 5 + i, 4)
    R(s, NEGRO, 3, 6, 13, 1)
    R(s, PIEL, 6, 7, 7, 7); R(s, PIEL, 13, 10, 1, 2); R(s, NEGRO, 10, 9)
    bigote = (40, 30, 25)
    R(s, bigote, 8, 12, 7, 1); R(s, bigote, 7, 13, 2, 1); R(s, bigote, 14, 13, 2, 1)
    R(s, AZUL, 3, 14, 13, 13); R(s, AMARILLO, 9, 14, 1, 13); R(s, AMARILLO, 3, 14, 3, 1)
    R(s, AZUL_D, 12, 15, 3, 8); R(s, BLANCO, 12, 23, 3, 2)
    R(s, AZUL_D, 3, 27, 12, 1)
    R(s, (30, 30, 40), 5, 28, 3, 5); R(s, (30, 30, 40), 11, 28, 3, 5)
    R(s, NEGRO, 4, 33, 4, 2); R(s, NEGRO, 11, 33, 5, 2)
    return s


def perro():
    """Perro grandote mirando a la izquierda (hacia donde llega Tano)."""
    s = lienzo(38, 21)
    pelo, pelo_d = (130, 90, 55), (95, 62, 38)
    linea(s, pelo_d, (32, 9), (36, 3), 2)                    # cola
    for x, c in ((11, pelo), (15, pelo), (26, pelo_d), (30, pelo_d)):
        R(s, c, x, 15, 3, 6)
    R(s, pelo, 10, 7, 22, 9); R(s, pelo_d, 10, 7, 22, 2)
    R(s, pelo, 2, 3, 10, 8); R(s, pelo, 0, 7, 4, 3)
    R(s, NEGRO, 0, 7); R(s, NEGRO, 5, 5); R(s, BLANCO, 2, 10)
    R(s, pelo_d, 8, 2, 3, 5)
    R(s, (200, 40, 40), 10, 8, 2, 5)                         # collar
    return s


def gato():
    """Gato naranja atigrado del Mercado, echado."""
    s = lienzo(24, 15)
    nar, nar_d = (215, 135, 60), (170, 95, 40)
    linea(s, nar, (20, 10), (23, 3), 2)
    R(s, nar, 7, 6, 14, 7)
    for x in (10, 13, 16):
        R(s, nar_d, x, 6, 1, 4)
    R(s, nar, 1, 3, 7, 6); R(s, nar, 1, 1, 2, 2); R(s, nar, 5, 1, 2, 2)
    R(s, (80, 200, 80), 3, 5); R(s, (230, 130, 140), 1, 6)
    R(s, nar, 7, 13, 2, 2); R(s, nar, 17, 13, 2, 2)
    return s


# ------------------------------------------------------------------ objetos de escena
def bombo():
    """Bombo de murga: casco rojo, un solo parche, cuerdas de tensión y mazo."""
    s = lienzo(21, 19)
    R(s, ROJO, 1, 6, 19, 9)
    pygame.draw.ellipse(s, ROJO_D, (1, 11, 19, 8))
    for x in range(3, 18, 4):
        linea(s, CREMA, (x, 9), (x + 2, 15))
    pygame.draw.ellipse(s, CREMA, (1, 2, 19, 8))
    pygame.draw.ellipse(s, (170, 150, 110), (1, 2, 19, 8), 1)
    linea(s, MADERA_D, (14, 1), (19, 5), 2)                   # mazo
    R(s, BLANCO, 12, 0, 3, 2)
    return s


def banco():
    s = lienzo(65, 27)
    for x in (6, 56):
        R(s, HIERRO, x, 0, 3, 27)
    for y in (2, 7):
        R(s, MADERA, 2, y, 61, 3); R(s, MADERA_L, 2, y, 61, 1)
    R(s, MADERA, 0, 13, 65, 4); R(s, MADERA_L, 0, 13, 65, 1); R(s, MADERA_D, 0, 16, 65, 1)
    return s


def tacho(con_diario=True):
    s = lienzo(22, 31)
    if con_diario:
        R(s, PAPEL, 5, 0, 10, 7)
        for y in (2, 4):
            R(s, GRIS, 6, y, 8, 1)
    R(s, (75, 120, 80), 2, 8, 18, 23)
    for x in (6, 11, 16):
        R(s, (55, 95, 60), x, 9, 1, 21)
    R(s, (55, 95, 60), 0, 5, 22, 4)
    return s


def yerbas():
    """Puesto de yerba: toldo a rayas, estantes con paquetes y mostrador con cartel."""
    s = lienzo(46, 31)
    for x in range(0, 46, 6):
        R(s, VERDE if (x // 6) % 2 == 0 else BLANCO, x, 0, 6, 5)
    R(s, MADERA_D, 1, 5, 2, 26); R(s, MADERA_D, 43, 5, 2, 26)
    R(s, (90, 60, 40), 3, 5, 40, 15)
    paquetes = (VERDE, AMARILLO, ROJO, (60, 110, 200))
    for fila, y in enumerate((7, 13)):
        for i, x in enumerate(range(4, 41, 5)):
            c = paquetes[(i + fila) % 4]
            R(s, c, x, y, 4, 5); R(s, CREMA, x + 1, y + 2, 2, 1)
    R(s, MADERA, 0, 20, 46, 11); R(s, MADERA_L, 0, 19, 46, 2)
    R(s, CREMA, 13, 23, 20, 6)
    for i in range(5):                                      # "YERBA" en verde, a lo pixel
        R(s, VERDE_D, 15 + i * 4, 25, 2, 2)
    return s


# Colores del chorizo según la cocción (sprite de la parrilla e íconos)
COCCION = {"crudo": ((225, 125, 135), (245, 165, 170)), "a_punto": (CHORIZO, (195, 85, 60)),
           "quemado": ((45, 35, 35), (75, 60, 55))}


def parrilla(prendida=False, chorizo=None):
    """Parrilla de ladrillo. Apagada: carbón gris. Prendida: brasas y humo.
    chorizo: None | "crudo" | "a_punto" | "quemado" (uno grande en el medio de la parrilla)."""
    s = lienzo(62, 27)
    if prendida:
        humo = (90, 85, 85, 190) if chorizo == "quemado" else (215, 215, 220, 150)
        for x0 in (14, 31, 47):                              # humo ondulado, semitransparente
            for y, dx in ((4, 0), (3, 1), (2, 2), (1, 1), (0, 0)):
                R(s, humo, x0 + dx, y, 3, 1)
    R(s, LADRILLO, 0, 12, 62, 15)
    for y in range(12, 27, 4):
        R(s, LADRILLO_D, 0, y, 62, 1)
        for x in range((y // 4 % 2) * 4, 62, 8):
            R(s, LADRILLO_D, x, y, 1, 4)
    brasa = (240, 110, 40) if prendida else (90, 90, 95)
    for x in range(4, 58, 3):
        R(s, brasa, x, 10, 2, 2)
    R(s, HIERRO_D, 2, 8, 58, 2)
    for x in range(3, 60, 4):
        R(s, HIERRO, x, 7, 1, 2)
    if chorizo:
        base, brillo = COCCION[chorizo]
        R(s, base, 17, 1, 28, 7); R(s, base, 15, 2, 2, 5); R(s, base, 45, 2, 2, 5)   # chorizo grande, bien visible
        R(s, brillo, 18, 2, 25, 1)
        if chorizo == "a_punto":
            for x in (22, 28, 34, 40):                       # marcas de la parrilla
                R(s, (100, 30, 25), x, 2, 1, 6)
        elif chorizo == "quemado":
            for x in (19, 26, 33, 41):                       # brasas en el carbón
                R(s, (240, 110, 40), x, 4, 2, 1)
    return s


def lena():
    """Pila de leña (troncos con la punta clara)."""
    s = lienzo(32, 11)
    for x, y in ((0, 6), (8, 6), (16, 6), (24, 6), (4, 2), (12, 2), (20, 2)):
        R(s, MADERA, x, y, 8, 5); R(s, MADERA_D, x, y + 4, 8, 1)
        R(s, (215, 175, 120), x, y + 1, 2, 3)               # corte del tronco
    return s


# ------------------------------------------------------------------ íconos de inventario
def _mate(s, carga=False, humo=False):
    pygame.draw.ellipse(s, (130, 85, 45), (4, 6, 12, 13))
    R(s, (95, 60, 30), 5, 6, 10, 2)
    if carga:
        R(s, VERDE, 6, 6, 8, 2)
    linea(s, PLATA, (12, 7), (15, 1))
    if humo:
        for x, y in ((6, 3), (7, 1), (9, 4), (10, 2), (8, 0)):
            R(s, BLANCO, x, y)
    return s


ICONOS = {
    "termo": lambda s: (R(s, AZUL, 7, 4, 7, 15), R(s, AZUL_D, 7, 4, 2, 15),
                        R(s, PLATA, 7, 1, 7, 3), R(s, PLATA, 14, 2, 1, 1)),
    "mate": lambda s: _mate(s),
    "mate_cargado": lambda s: _mate(s, carga=True),
    "mate_listo": lambda s: _mate(s, carga=True, humo=True),
    "yerba": lambda s: (R(s, VERDE, 4, 2, 12, 17), R(s, VERDE_D, 4, 2, 12, 2),
                        R(s, CREMA, 5, 8, 10, 6), R(s, ROJO, 6, 10, 8, 1), R(s, ROJO, 6, 12, 6, 1)),
    "diario": lambda s: (R(s, PAPEL, 3, 4, 14, 13), R(s, NEGRO, 4, 5, 12, 2),
                         [R(s, GRIS, 4, y, 12, 1) for y in (9, 11, 13, 15)],
                         R(s, (190, 185, 170), 10, 8, 1, 9)),
    "choripan": lambda s: (pygame.draw.ellipse(s, PAN, (1, 7, 18, 8)),
                           R(s, CHORIZO, 0, 9, 20, 3), R(s, (190, 80, 60), 1, 9, 18, 1),
                           pygame.draw.ellipse(s, (235, 185, 110), (2, 11, 16, 5)),
                           [R(s, VERDE, x, 8) for x in (5, 9, 13)]),
    "lena": lambda s: [(R(s, MADERA, 2, y, 16, 4), R(s, MADERA_D, 2, y + 3, 16, 1),
                        R(s, (215, 175, 120), 2, y + 1, 2, 2)) for y in (5, 10, 15)],
    "lena_papel": lambda s: ([(R(s, MADERA, 2, y, 16, 4), R(s, MADERA_D, 2, y + 3, 16, 1)) for y in (10, 15)],
                             R(s, PAPEL, 4, 4, 12, 6), R(s, GRIS, 5, 6, 10, 1), R(s, GRIS, 5, 8, 8, 1)),
    "chorizo": lambda s: _chorizo(s, "crudo"),
    "chorizo_asado": lambda s: _chorizo(s, "a_punto"),
    "pan": lambda s: (pygame.draw.ellipse(s, PAN, (1, 6, 18, 9)), R(s, (240, 200, 130), 4, 8, 12, 1),
                      [R(s, (180, 125, 60), x, 7, 2, 1) for x in (5, 9, 13)]),
}


def _chorizo(s, coccion):
    base, brillo = COCCION[coccion]
    R(s, base, 2, 8, 16, 5); R(s, base, 1, 9, 1, 3); R(s, base, 18, 9, 1, 3)
    R(s, brillo, 3, 8, 13, 1)
    R(s, (230, 220, 210), 0, 10); R(s, (230, 220, 210), 19, 10)    # puntas atadas
    if coccion == "a_punto":
        for x in (6, 10, 14):
            R(s, (100, 30, 25), x, 9, 1, 4)

SPRITES = {
    "tano_idle": tano(),
    **{f"tano_walk_{i}": tano(i) for i in range(4)},
    "pescador": pescador(), "asador": asador(), "contramaestre": contramaestre(),
    "perro": perro(), "gato": gato(), "bombo": bombo(), "banco": banco(),
    "tacho": tacho(), "tacho_vacio": tacho(False),
    "yerbas": yerbas(), "parrilla": parrilla(), "parrilla_prendida": parrilla(True), "lena": lena(),
    **{f"parrilla_chorizo_{c}": parrilla(True, c) for c in COCCION},
}


def main():
    for sub in ("sprites", "objetos"):
        os.makedirs(os.path.join(ASSETS, sub), exist_ok=True)
    for name, surf in SPRITES.items():
        pygame.image.save(contorno(surf), os.path.join(ASSETS, "sprites", f"{name}.png"))
    for name, dibujar in ICONOS.items():
        s = lienzo(20, 20)
        dibujar(s)
        pygame.image.save(contorno(s), os.path.join(ASSETS, "objetos", f"{name}.png"))
    print(f"OK {len(SPRITES)} sprites + {len(ICONOS)} íconos -> {ASSETS}")


if __name__ == "__main__":
    main()
