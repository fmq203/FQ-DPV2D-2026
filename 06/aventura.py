import os
import re
import sys
import pygame

pygame.init()

ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 26)
fuente_titulo = pygame.font.SysFont("arial", 30, bold=True)

CARPETA_ASSETS = os.path.join(os.path.dirname(__file__), "assets")

# ====== INVENTARIO ======
# Objetos que el jugador puede tener. Algunas opciones solo aparecen
# si el jugador tiene (o no tiene) determinado objeto.
tiene_banana = False

# ====== FONDOS POR ESCENA ======
FONDOS = {
    "inicio": (20, 60, 20),    # selva
    "rio": (15, 45, 75),       # río
    "aldea": (70, 55, 20),     # aldea
    "cueva": (45, 35, 25),     # cueva
    "mono": (45, 35, 25),      # sigue dentro de la cueva
    "cofre": (70, 20, 20),     # susto / peligro
    "tesoro": (90, 75, 10),    # brillo dorado
}
FONDO_POR_DEFECTO = (20, 30, 20)


def cargar_imagen_fondo(nombre_escena):
    # Busca assets/fondos/<escena>.png o .jpg. Si no existe ninguna,
    # devuelve None y el juego usa el color de FONDOS como respaldo.
    for extension in (".png", ".jpg", ".jpeg"):
        ruta = os.path.join(CARPETA_ASSETS, "fondos", nombre_escena + extension)
        if os.path.isfile(ruta):
            try:
                imagen = pygame.image.load(ruta).convert()
                return pygame.transform.scale(imagen, (ANCHO, ALTO))
            except pygame.error as e:
                print(f"No se pudo cargar la imagen '{ruta}': {e}")
                return None
    return None


# Precargamos las imágenes de fondo una sola vez (quedan en caché por escena).
IMAGENES_FONDO = {nombre: cargar_imagen_fondo(nombre) for nombre in FONDOS}

# ====== SPRITES ANIMADOS (objetos) ======
# Cada carpeta en assets/objetos/ tiene los frames sueltos de una animación
# (no una spritesheet). Los cargamos una sola vez y los ciclamos por tiempo.
def _numero_en_nombre(nombre):
    # "chest2.png" -> 2, "chest10.png" -> 10 (para no ordenar como texto,
    # donde "chest10" quedaría antes que "chest2").
    coincidencia = re.search(r"\d+", nombre)
    return int(coincidencia.group()) if coincidencia else 0


def cargar_frames(carpeta, prefijo="", escala=1, tamaño=None):
    ruta = os.path.join(CARPETA_ASSETS, "objetos", carpeta)
    if not os.path.isdir(ruta):
        return []
    nombres = sorted(
        (n for n in os.listdir(ruta)
         if n.startswith(prefijo) and n.lower().endswith((".png", ".jpg", ".jpeg"))),
        key=_numero_en_nombre,
    )
    frames = []
    for nombre in nombres:
        imagen = pygame.image.load(os.path.join(ruta, nombre)).convert_alpha()
        if tamaño:
            imagen = pygame.transform.smoothscale(imagen, tamaño)
        elif escala != 1:
            ancho, alto = imagen.get_size()
            imagen = pygame.transform.scale(imagen, (ancho * escala, alto * escala))
        frames.append(imagen)
    return frames


def frame_actual(frames, intervalo_ms=200):
    # Elige el frame según el tiempo transcurrido, para que la animación
    # se vea igual sin importar los FPS.
    if not frames:
        return None
    indice = (pygame.time.get_ticks() // intervalo_ms) % len(frames)
    return frames[indice]


FRAMES_BANANA = cargar_frames("banana", escala=4)          # para la escena del río
FRAMES_BANANA_ICONO = cargar_frames("banana", escala=2)    # más chico, para el inventario
FRAMES_MONO = cargar_frames("mono", prefijo="Monkey Idle", escala=3)

# chest1..chest15: 1-5 el cofre abriéndose, 6-15 ya abierto con destellos.
FRAMES_COFRE = cargar_frames("cofre", prefijo="chest", tamaño=(140, 140))
FRAMES_COFRE_GRANDE = cargar_frames("cofre", prefijo="chest", tamaño=(220, 220))
COFRE_CERRADO = FRAMES_COFRE[:1] if FRAMES_COFRE else []
COFRE_INTENTANDO_ABRIR = FRAMES_COFRE[3:4] if len(FRAMES_COFRE) > 3 else []
COFRE_ABIERTO_GRANDE = FRAMES_COFRE_GRANDE[5:] if len(FRAMES_COFRE_GRANDE) > 5 else []

# Qué sprites animados mostrar (y dónde) según la escena actual.
# Cada escena puede tener varios sprites a la vez (por eso es una lista).
SPRITES_ESCENA = {
    "rio": [
        {"frames": FRAMES_BANANA, "pos": (760, 160), "visible": lambda: not tiene_banana},
    ],
    "cueva": [
        {"frames": FRAMES_MONO, "pos": (720, 140)},
        {"frames": COFRE_CERRADO, "pos": (660, 320)},
    ],
    "mono": [
        {"frames": FRAMES_MONO, "pos": (720, 140)},
        {"frames": COFRE_CERRADO, "pos": (660, 320)},
    ],
    "cofre": [
        {"frames": COFRE_INTENTANDO_ABRIR, "pos": (660, 320)},
    ],
    "tesoro": [
        {"frames": COFRE_ABIERTO_GRANDE, "pos": (340, 300)},
    ],
}

# ====== SONIDO ======
sonido_click = None
try:
    pygame.mixer.init()
    for extension in (".wav", ".ogg"):
        ruta = os.path.join(CARPETA_ASSETS, "sonidos", "click" + extension)
        if os.path.isfile(ruta):
            sonido_click = pygame.mixer.Sound(ruta)
            break
except pygame.error as e:
    print(f"No se pudo inicializar el sonido: {e}")


# ====== ACCIONES ======
# Funciones que se ejecutan al elegir una opción, antes de cambiar de escena.
# Sirven para modificar el inventario u otras variables globales.
def tomar_banana():
    global tiene_banana
    tiene_banana = True


def dar_banana():
    global tiene_banana
    tiene_banana = False


def reiniciar():
    global tiene_banana
    tiene_banana = False


ACCIONES = {
    "tomar_banana": tomar_banana,
    "dar_banana": dar_banana,
    "reiniciar": reiniciar,
}

# Botón que se muestra en vez de las opciones cuando una escena es un final
# (su lista de "opciones" está vacía).
BOTON_REINICIAR = [{"texto": "Reiniciar aventura", "destino": "inicio", "accion": "reiniciar"}]

# ====== HISTORIA ======
# Cada escena tiene un texto y una lista de opciones.
# Cada opción es un diccionario con:
#   "texto": lo que se muestra en el botón
#   "destino": a qué escena se va al elegirla
#   "requiere" (opcional): función que devuelve True/False; si devuelve
#       False, la opción no se muestra (así se implementa el inventario)
#   "accion" (opcional): nombre de una función en ACCIONES que se ejecuta
#       al elegir la opción (por ejemplo, agarrar un objeto)
historia = {
    "inicio": {
        "texto": "Estás en la selva. Escuchás un ruido entre los árboles.",
        "opciones": [
            {"texto": "Ir a investigar", "destino": "cueva"},
            {"texto": "Seguir el sendero", "destino": "rio"},
        ],
    },
    "cueva": {
        "texto": "Dentro de la cueva hay un cofre dorado. Un mono lo custodia.",
        "opciones": [
            {"texto": "Hablar con el mono", "destino": "mono"},
            {"texto": "Abrir el cofre a escondidas", "destino": "cofre"},
        ],
    },
    "mono": {
        "texto": "El mono habla: '¡Dame una banana y el tesoro será tuyo!'",
        "opciones": [
            {"texto": "Dar la banana", "destino": "tesoro", "accion": "dar_banana",
             "requiere": lambda: tiene_banana},
            {"texto": "No tengo ninguna banana...", "destino": "inicio", "requiere": lambda: not tiene_banana},
            {"texto": "Negarme", "destino": "inicio"},
        ],
    },
    "tesoro": {
        "texto": "¡Ganaste el tesoro legendario de la selva! Fin de la aventura.",
        "opciones": [],
    },
    "cofre": {
        "texto": "Intentás abrir el cofre a escondidas, pero el mono te descubre "
                 "y grita furioso. Escapás corriendo con las manos vacías.",
        "opciones": [
            {"texto": "Volver a la selva", "destino": "inicio"},
        ],
    },
    "rio": {
        "texto": "El sendero termina en la orilla de un río ancho. Hay una banana "
                 "silvestre entre las piedras y una vieja barca amarrada.",
        "opciones": [
            {"texto": "Agarrar la banana", "destino": "rio", "accion": "tomar_banana",
             "requiere": lambda: not tiene_banana},
            {"texto": "Cruzar el río en la barca", "destino": "aldea"},
            {"texto": "Volver a la selva", "destino": "inicio"},
        ],
    },
    "aldea": {
        "texto": "Llegás a una pequeña aldea junto al río. Los aldeanos te "
                 "agradecen la visita y te invitan a quedarte. Fin de la aventura.",
        "opciones": [],
    },
}
# ======================================================

escena = "inicio"


def opciones_visibles(opciones):
    # Filtra las opciones según su condición "requiere" (si tiene una).
    return [op for op in opciones if op.get("requiere", lambda: True)()]


def opciones_mostradas(escena):
    # Si la escena no tiene opciones, es un final: mostramos el botón
    # de reiniciar en su lugar.
    opciones = historia[escena]["opciones"]
    if not opciones:
        return BOTON_REINICIAR
    return opciones_visibles(opciones)


def dibujar_botones(opciones):
    botones = []
    y = ALTO - 44 * len(opciones) - 20
    for op in opciones:
        rect = pygame.Rect(ANCHO // 2 - 220, y, 440, 36)
        pygame.draw.rect(pantalla, (60, 60, 130), rect)
        pygame.draw.rect(pantalla, (120, 120, 200), rect, width=2)
        pantalla.blit(fuente.render(op["texto"], True, (255, 255, 255)), (rect.x + 12, rect.y + 6))
        botones.append((rect, op))
        y += 46
    return botones


def dibujar_texto(texto, limite=48):
    palabras = texto.split()
    lineas, actual = [], ""
    for p in palabras:
        if len(actual) + len(p) + 1 > limite:
            lineas.append(actual)
            actual = p
        else:
            actual = (actual + " " + p).strip()
    lineas.append(actual)
    y = 150
    for linea in lineas:
        pantalla.blit(fuente.render(linea, True, (255, 255, 255)), (80, y))
        y += 34


def elegir_opcion(op):
    global escena
    if sonido_click:
        sonido_click.play()
    nombre_accion = op.get("accion")
    if nombre_accion:
        ACCIONES[nombre_accion]()
    escena = op["destino"]
    if not historia[escena]["opciones"]:
        print("La aventura terminó.")


ejecutando = True
while ejecutando:
    opciones = opciones_mostradas(escena)
    botones = dibujar_botones(opciones)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and opciones:
            mx, my = pygame.mouse.get_pos()
            for rect, op in botones:
                if rect.collidepoint(mx, my):
                    elegir_opcion(op)
                    break

    imagen_fondo = IMAGENES_FONDO.get(escena)
    if imagen_fondo:
        pantalla.blit(imagen_fondo, (0, 0))
    else:
        pantalla.fill(FONDOS.get(escena, FONDO_POR_DEFECTO))
    pantalla.blit(fuente_titulo.render("AVENTURA EN LA SELVA", True, (255, 200, 60)), (80, 60))

    for sprite in SPRITES_ESCENA.get(escena, []):
        if sprite.get("visible", lambda: True)():
            frame = frame_actual(sprite["frames"])
            if frame:
                pantalla.blit(frame, sprite["pos"])

    if tiene_banana:
        icono = frame_actual(FRAMES_BANANA_ICONO)
        if icono:
            pantalla.blit(icono, (80, 96))
            pantalla.blit(fuente.render("Inventario: banana", True, (230, 230, 150)), (118, 100))
        else:
            pantalla.blit(fuente.render("Inventario: 🍌 banana", True, (230, 230, 150)), (80, 100))

    dibujar_texto(historia[escena]["texto"])
    dibujar_botones(opciones_mostradas(escena))
    pygame.display.flip()
    reloj.tick(30)

pygame.quit()
sys.exit()
