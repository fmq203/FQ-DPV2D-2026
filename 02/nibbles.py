import random
import sys
from pathlib import Path
import pygame

pygame.init()

ANCHO, ALTO = 600, 600
CELDA = 30
COLUMNAS = ANCHO // CELDA
FILAS = ALTO // CELDA

pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

# El cuerpo: lista de (columna, fila). La cabeza es el primer elemento.
serpiente = [(5, 5)]
direccion = (1, 0)  # (dx, dy) -> derecha


def manzana_nueva(ocupadas):
    while True:
        m = (random.randint(0, COLUMNAS - 1), random.randint(0, FILAS - 1))
        if m not in ocupadas:
            return m


manzana = manzana_nueva(serpiente)
puntos = 0

RECORD_PATH = Path(__file__).parent / "record.txt"
try:
    with open(RECORD_PATH) as f:
        record = int(f.read())
except FileNotFoundError:
    record = 0

manzana_dorada = None
temporizador_dorada = 0
PROBABILIDAD_DORADA = 0.01  # chance por frame de que aparezca (poco frecuente)
DURACION_DORADA = 50  # frames que dura visible antes de desaparecer


def dibujar_celda(pos, color):
    pygame.draw.rect(pantalla, color,
                      (pos[0] * CELDA, pos[1] * CELDA, CELDA - 2, CELDA - 2))


ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            # No dejar que gire 180 grados (no puede ir para atrás)
            if evento.key == pygame.K_UP and direccion != (0, 1):
                direccion = (0, -1)
            elif evento.key == pygame.K_DOWN and direccion != (0, -1):
                direccion = (0, 1)
            elif evento.key == pygame.K_LEFT and direccion != (1, 0):
                direccion = (-1, 0)
            elif evento.key == pygame.K_RIGHT and direccion != (-1, 0):
                direccion = (1, 0)

    # 1) Nueva cabeza
    cabeza = (serpiente[0][0] + direccion[0], serpiente[0][1] + direccion[1])
    serpiente.insert(0, cabeza)

    # 2) ¿Comió?
    if cabeza == manzana:
        puntos += 1
        manzana = manzana_nueva(serpiente)
    elif manzana_dorada is not None and cabeza == manzana_dorada:
        puntos += 5
        manzana_dorada = None
    else:
        serpiente.pop()  # no comió -> se achica por el final

    # 2b) Manzana dorada: aparece poco frecuente y dura un tiempo limitado
    if manzana_dorada is None:
        if random.random() < PROBABILIDAD_DORADA:
            manzana_dorada = manzana_nueva(serpiente + [manzana])
            temporizador_dorada = DURACION_DORADA
    else:
        temporizador_dorada -= 1
        if temporizador_dorada <= 0:
            manzana_dorada = None

    # 3) ¿Chocó con el borde o consigo misma?
    if (cabeza[0] < 0 or cabeza[0] >= COLUMNAS or
            cabeza[1] < 0 or cabeza[1] >= FILAS or
            cabeza in serpiente[1:]):
        ejecutando = False

    # 4) Dibujar
    pantalla.fill((10, 10, 15))
    for segmento in serpiente:
        dibujar_celda(segmento, (0, 220, 60))
    dibujar_celda(manzana, (230, 40, 40))
    if manzana_dorada is not None:
        dibujar_celda(manzana_dorada, (255, 215, 0))
    pygame.display.set_caption(f"Puntos: {puntos} | Récord: {record}")
    pygame.display.flip()

    reloj.tick(10)  # 10 FPS: velocidad clásica

if puntos > record:
    record = puntos
    with open(RECORD_PATH, "w") as f:
        f.write(str(record))

pygame.quit()
print(f"Fin del juego. Puntos: {puntos} | Récord: {record}")
sys.exit()
