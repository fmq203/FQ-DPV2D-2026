import sys
import pygame

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

pala = pygame.Rect(ANCHO // 2 - 60, ALTO - 40, 120, 15)
pelota = pygame.Rect(ANCHO // 2 - 8, ALTO // 2, 16, 16)
vel_x, vel_y = 5, -5

# Ladrillos: una fila de rectángulos
FILAS, COLS = 4, 10
ladrillos = []
for fila in range(FILAS):
    for col in range(COLS):
        ladrillos.append(pygame.Rect(col * 80 + 5, fila * 30 + 40, 70, 20))

vidas = 3
puntos = 0
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Paleta sigue al mouse
    pala.x = pygame.mouse.get_pos()[0] - pala.width // 2
    pala.x = max(0, min(ANCHO - pala.width, pala.x))

    # Mover la pelota
    pelota.x += vel_x
    pelota.y += vel_y

    # Rebotes con paredes
    if pelota.left <= 0 or pelota.right >= ANCHO:
        vel_x *= -1
    if pelota.top <= 0:
        vel_y *= -1
    if pelota.colliderect(pala) and vel_y > 0:
        vel_y *= -1

    # COMPLETÁ: destruir ladrillos
    for ladrillo in ladrillos[:]:
         if pelota.colliderect(ladrillo):
             ladrillos.remove(ladrillo)
             puntos += 10
             vel_y *= -1
             if puntos % 50 == 0:
                 vel_x *= 1.1
                 vel_y *= 1.1
             break

    # Perder vida
    if pelota.bottom >= ALTO:
        vidas -= 1
        pelota.center = (ANCHO // 2, ALTO // 2)
        if vidas == 0:
            ejecutando = False

    # Dibujar
    pantalla.fill((15, 15, 30))
    pygame.draw.rect(pantalla, (90, 180, 255), pala)
    pygame.draw.rect(pantalla, (255, 255, 255), pelota)
    for ladrillo in ladrillos:
        pygame.draw.rect(pantalla, (255, 120, 120), ladrillo)
    
    # Ganar el juego : mensaje de victoria
    if len(ladrillos) == 0:
        fuente = pygame.font.Font(None, 74)
        texto = fuente.render("¡Ganaste!", True, (255, 255, 0))
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))

    pygame.display.set_caption(f"Arkanoid - Vidas: {vidas} - Ladrillos: {len(ladrillos)} - Puntos: {puntos}")
    pygame.display.flip()
    reloj.tick(60)

    # Ganar el juego : salir
    if len(ladrillos) == 0:
        pygame.time.wait(2000)   # pausa 2 segundos con el mensaje ya visible
        ejecutando = False

pygame.quit()
sys.exit()
