import sys
import pygame

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

GRAVEDAD = 0.5
VEL_MOV = 6
FUERZA_SALTO = -13
POS_INICIAL = (100, 300)

mono = pygame.Rect(*POS_INICIAL, 40, 40)
vel_x, vel_y = 0, 0
en_piso = False
vidas = 3

plataformas = [
    pygame.Rect(0, ALTO - 40, ANCHO, 40),  # piso
    pygame.Rect(200, 450, 180, 25),
    pygame.Rect(450, 360, 180, 25),
    pygame.Rect(600, 250, 180, 25),
]

BANANAS_INICIALES = [
    pygame.Rect(250, 420, 20, 20),
    pygame.Rect(500, 330, 20, 20),
    pygame.Rect(650, 220, 20, 20),
]
bananas = [pygame.Rect(b) for b in BANANAS_INICIALES]
juntas = 0

# Enemigos: cada uno patrulla entre un x mínimo y máximo sobre su plataforma
enemigos = [
    {"rect": pygame.Rect(220, 430, 30, 20), "min_x": 200, "max_x": 350, "vel": 2},
    {"rect": pygame.Rect(470, 340, 30, 20), "min_x": 450, "max_x": 600, "vel": 3},
]

inicio_ticks = pygame.time.get_ticks()
segundos_finales = None

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and en_piso:
                vel_y = FUERZA_SALTO

    # Movimiento horizontal con teclado
    teclas = pygame.key.get_pressed()
    vel_x = (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * VEL_MOV

    # Gravedad y movimiento
    vel_y += GRAVEDAD
    mono.x += vel_x
    mono.y += vel_y

    # Colisión con plataformas
    en_piso = False
    for p in plataformas:
        if mono.colliderect(p) and vel_y > 0 and mono.bottom <= p.top + 15:
            mono.bottom = p.top
            vel_y = 0
            en_piso = True

    # Juntar bananas
    for b in bananas[:]:
        if mono.colliderect(b):
            bananas.remove(b)
            juntas += 1

    # Mover enemigos (patrulla izquierda-derecha)
    for e in enemigos:
        e["rect"].x += e["vel"]
        if e["rect"].left <= e["min_x"] or e["rect"].right >= e["max_x"]:
            e["vel"] *= -1

    # Tocar un enemigo: perder una vida y reaparecer
    for e in enemigos:
        if mono.colliderect(e["rect"]):
            vidas -= 1
            mono.topleft = POS_INICIAL
            vel_y = 0
            if vidas <= 0:
                ejecutando = False

    # Si el mono se cae de la pantalla, reiniciar el juego
    if mono.top > ALTO:
        mono.topleft = POS_INICIAL
        vel_y = 0
        bananas = [pygame.Rect(b) for b in BANANAS_INICIALES]
        juntas = 0

    # Dibujar
    pantalla.fill((150, 210, 255))
    for p in plataformas:
        pygame.draw.rect(pantalla, (90, 60, 30), p)
    pygame.draw.rect(pantalla, (160, 110, 50), mono)
    for b in bananas:
        pygame.draw.circle(pantalla, (255, 220, 60), b.center, 10)
    for e in enemigos:
        pygame.draw.rect(pantalla, (200, 40, 40), e["rect"])

    if len(bananas) == 0 and segundos_finales is None:
        segundos_finales = (pygame.time.get_ticks() - inicio_ticks) // 1000

    segundos = segundos_finales if segundos_finales is not None else (pygame.time.get_ticks() - inicio_ticks) // 1000
    pygame.display.set_caption(f"El Mono - Bananas: {juntas} - Vidas: {vidas} - Tiempo: {segundos}s")
    pygame.display.flip()
    reloj.tick(60)

    if len(bananas) == 0:
        pygame.time.wait(1500)
        ejecutando = False

pygame.quit()
sys.exit()
