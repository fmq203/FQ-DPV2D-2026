import math
import random
import sys
import pygame
pygame.init()
ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

GRAVEDAD = 0.25   # se le suma a vy cada cuadro: acelera la caída
POTENCIA = 22     # velocidad inicial de la bala al disparar
VIENTO_MAX = 0.06  # empuje horizontal máximo por cuadro (positivo = hacia la derecha)
CAMBIO_VIENTO_CADA = 300  # cuadros entre cambios de viento (~5 s a 60 FPS)

origen = (90, ALTO - 30)  # posición del cañón
balas = []  # cada bala es un dict: x, y, vx, vy
blancos = [{"x": x, "ancho": 60, "alto": 40} for x in range(350, 850, 90)]
puntos = 0
viento = random.uniform(-VIENTO_MAX, VIENTO_MAX)
cuadros = 0
fuente = pygame.font.SysFont(None, 28)


def disparar(angulo):
	# atan2 en pantalla ya devuelve el ángulo "matemático" (0° = derecha,
	# 90° = arriba), gracias a cómo se calcula más abajo con MOUSEMOTION.
	rad = math.radians(angulo)
	vx = POTENCIA * math.cos(rad)
	# En pantalla el eje Y crece hacia ABAJO, al revés que en el plano
	# cartesiano normal. Por eso "arriba" (sin positivo) hay que restarlo
	# de y, y acá se guarda como vy negativo.
	vy = -POTENCIA * math.sin(rad)
	balas.append({"x": origen[0], "y": origen[1], "vx": vx, "vy": vy})


ejecutando = True
# angulo vive afuera del while para que se mantenga entre cuadros: pygame
# solo manda MOUSEMOTION cuando el mouse se mueve, así que si se reiniciara
# a 0 en cada vuelta, el cañón "saltaría" a 0° apenas el mouse quedara quieto.
angulo = 0

while ejecutando:
	cuadros += 1
	if cuadros % CAMBIO_VIENTO_CADA == 0:
		viento = random.uniform(-VIENTO_MAX, VIENTO_MAX)

	for evento in pygame.event.get():
		if evento.type == pygame.QUIT:
			ejecutando = False
		elif evento.type == pygame.MOUSEMOTION:
			mx, my = pygame.mouse.get_pos()
			# origen[1] - my (no my - origen[1]) compensa el eje Y invertido
			# de la pantalla, para que el ángulo se comporte como en un
			# plano cartesiano normal (0° derecha, 90° arriba).
			angulo = math.degrees(
				math.atan2(origen[1] - my, mx - origen[0])
			)
		elif evento.type == pygame.MOUSEBUTTONDOWN:
			disparar(angulo)

	# Física de cada bala: primero se mueve con la velocidad actual, y
	# recién después esa velocidad cambia (gravedad, viento). Así el efecto
	# de la aceleración de este cuadro se nota a partir del cuadro siguiente.
	for b in balas:
		b["x"] += b["vx"]
		b["y"] += b["vy"]
		b["vy"] += GRAVEDAD
		b["vx"] += viento
		if b["y"] > ALTO - 10:  # rebote en el piso
			b["vy"] *= -0.7  # invierte la velocidad y la amortigua un 30%
			b["y"] = ALTO - 10  # evita que la bala se meta bajo el piso

	# --- Dibujar ---
	pantalla.fill((25, 25, 45))
	pygame.draw.rect(pantalla, (80, 220, 120), (0, ALTO - 10, ANCHO, 10))  # piso

	# Indicador de viento: texto con el valor y una línea que crece hacia
	# el lado al que empuja (escalada x500 para que se note en pantalla).
	texto_viento = fuente.render(f"Viento: {viento:+.3f}", True, (255, 255, 255))
	pantalla.blit(texto_viento, (ANCHO - 190, 10))
	cx, cy = ANCHO - 100, 40
	pygame.draw.line(
		pantalla,
		(120, 200, 240),
		(cx - viento * 500, cy),
		(cx + viento * 500, cy),
		4,
	)

	for blanco in blancos:
		pygame.draw.rect(
			pantalla,
			(220, 80, 80),
			(blanco["x"], ALTO - 90, blanco["ancho"], blanco["alto"]),
		)

	# Línea de puntería: mismo truco de signo que en disparar() para que
	# apunte hacia donde está realmente el mouse.
	rad = math.radians(angulo)
	pygame.draw.line(
		pantalla,
		(240, 200, 60),
		origen,
		(
			origen[0] + 60 * math.cos(rad),
			origen[1] - 60 * math.sin(rad),
		),
		6,
	)

	for b in balas:
		pygame.draw.circle(
			pantalla,
			(240, 240, 240),
			(int(b["x"]), int(b["y"])),
			8,
		)

	# Colisiones bala-blanco: se recorren copias (balas[:], blancos[:])
	# porque adentro se borra de las listas originales mientras se itera.
	for b in balas[:]:
		for blanco in blancos[:]:
			if (
				blanco["x"] <= b["x"] <= blanco["x"] + blanco["ancho"]
				and ALTO - 90 <= b["y"] <= ALTO - 90 + blanco["alto"]
			):
				blancos.remove(blanco)
				balas.remove(b)
				puntos += 10
				break  # esta bala ya impactó, no puede chocar otro blanco

	pygame.display.set_caption(f"Cañones - Puntos: {puntos}")
	pygame.display.flip()
	reloj.tick(60)  # limita el juego a 60 cuadros por segundo

pygame.quit()
sys.exit()
