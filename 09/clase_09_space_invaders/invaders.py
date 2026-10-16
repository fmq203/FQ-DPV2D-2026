"""
Clase 09 - Space Invaders (disparos y enemigos).

IDEA GENERAL
------------
Usamos el enfoque "Game Loop" del motor: en vez de escribir nosotros el
`while ejecutando:` de siempre, heredamos de `GameLoop`. El motor se encarga de:
    - crear la ventana (pygame.init, set_mode)
    - controlar los FPS (Clock.tick)
    - repetir en cada frame:  eventos -> lógica -> dibujo
Nosotros solo rellenamos tres métodos:
    handle_specific_events(event)  -> qué pasa cuando se aprieta una tecla
    update_game_logic()            -> mover cosas y detectar colisiones
    draw_game_elements()           -> dibujar todo en pantalla

ESTRUCTURAS DE DATOS
--------------------
Todo lo que aparece y desaparece (balas, enemigos) es una LISTA de pygame.Rect.
Un Rect es un rectángulo con x, y, ancho y alto; sirve a la vez como posición,
tamaño y "caja de colisión".

Controles: flechas = mover, ESPACIO = disparar, R = reiniciar, ESC = salir.
"""

import pygame

# Del motor: GameLoop (bucle principal) y Label (texto en pantalla).
from engine import GameLoop, Label, ParticleSystem
from engine.utils.colors import BLANCO, AMARILLO

# ---------------------------------------------------------------------- #
#  Constantes: números "mágicos" con nombre, para poder ajustarlos fácil.
# ---------------------------------------------------------------------- #
ANCHO, ALTO = 800, 600
VIDAS_INICIALES = 3
PARPADEO_MS = 1000           # cuánto dura la invulnerabilidad tras ser tocada
INTERVALO_PARPADEO_MS = 100  # cada cuánto cambia la nave visible <-> invisible


class SpaceInvaders(GameLoop):
    # ================================================================== #
    #  INICIO Y REINICIO
    # ================================================================== #
    def __init__(self):
        # Le pedimos al motor ventana de 800x600, título y 60 FPS.
        super().__init__(ANCHO, ALTO, "Space Invaders", 60)
        # Fuente grande para el cartel final (se crea una sola vez).
        self.fuente_grande = pygame.font.Font(None, 72)
        self.reiniciar()

    def reiniciar(self):
        """Deja el juego en su estado inicial. Se usa al arrancar y con la tecla R."""
        # La nave: un Rect de 60x30 centrado abajo.
        self.nave = pygame.Rect(ANCHO // 2 - 30, ALTO - 60, 60, 30)

        # Balas de la nave: empieza vacía, se llena al apretar espacio.
        self.balas = []

        # Sistema de partículas del motor: guarda y actualiza las chispas de
        # las explosiones (se vacía solo cuando cada partícula se apaga).
        self.particulas = ParticleSystem()

        # Oleada: una grilla de enemigos creada con una lista por comprensión.
        # x va de 60 en 60 (columnas) e y de 40 en 40 (filas) => 12 x 3 enemigos.
        self.enemigos = [pygame.Rect(x, y, 40, 30)
                         for x in range(40, ANCHO - 40, 60)
                         for y in range(30, 150, 40)]
        self.dir_enemigos = 1   # 1 = la oleada va a la derecha, -1 = a la izquierda

        self.puntos = 0
        self.vidas = VIDAS_INICIALES

        # Instante (en ms desde que arrancó pygame) hasta el cual la nave es
        # invulnerable. Al empezar vale 0, o sea "ya pasó": no es invulnerable.
        self.invulnerable_hasta = 0

        # Estado de la partida. Decide qué se actualiza y qué se dibuja.
        #   "jugando" -> todo funciona
        #   "ganaste" -> se eliminó toda la oleada
        #   "perdiste"-> sin vidas o un enemigo llegó abajo
        self.estado = "jugando"

    # ================================================================== #
    #  EVENTOS  (el motor llama a esto UNA VEZ POR CADA evento)
    # ================================================================== #
    def handle_specific_events(self, event):
        # Solo nos interesan las teclas apretadas (KEYDOWN = un solo disparo
        # por pulsación, no mientras se mantiene presionada).
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            self.running = False            # el motor corta el bucle y cierra
        elif event.key == pygame.K_r:
            self.reiniciar()
        elif event.key == pygame.K_SPACE and self.estado == "jugando":
            # CREAR una bala: nace en la punta de la nave (centrada, 4x12).
            # Su "ciclo de vida" sigue en mover_balas().
            self.balas.append(pygame.Rect(self.nave.centerx - 2, self.nave.y, 4, 12))

    # ================================================================== #
    #  LÓGICA  (el motor llama a esto una vez por frame, 60 veces/seg)
    # ================================================================== #
    def update_game_logic(self):
        # Las partículas se actualizan siempre (también al terminar la partida)
        # para que las explosiones se apaguen solas. dt va en SEGUNDOS.
        self.particulas.update(1 / self.fps)

        # Si la partida terminó, congelamos el resto (solo queda el cartel y R).
        if self.estado != "jugando":
            return

        # El orden importa: primero movemos, después revisamos choques.
        self.mover_nave()
        self.mover_balas()
        self.mover_oleada()
        self.colisiones_bala_enemigo()
        self.colisiones_con_nave()

        # Condición de victoria: la lista de enemigos quedó vacía.
        if not self.enemigos:
            self.estado = "ganaste"

    def mover_nave(self):
        # get_pressed() dice qué teclas están mantenidas AHORA, así la nave
        # se mueve de forma continua (a diferencia de KEYDOWN, que es un pulso).
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.nave.x -= 6
        if teclas[pygame.K_RIGHT]:
            self.nave.x += 6
        # "Clamp": limita x entre 0 y el borde derecho para no salirse de pantalla.
        self.nave.x = max(0, min(ANCHO - self.nave.width, self.nave.x))

    def mover_balas(self):
        # CICLO DE VIDA de una bala: nace al disparar, sube 8 px por frame y
        # se elimina al salir por arriba (así la lista no crece para siempre).
        #
        # Recorremos una COPIA (balas[:]) porque borramos de la lista mientras
        # iteramos; si recorriéramos la original, Python saltearía elementos.
        for b in self.balas[:]:
            b.y -= 8
            if b.bottom < 0:               # todo el Rect quedó sobre el borde superior
                self.balas.remove(b)

    def mover_oleada(self):
        # La flota se mueve EN BLOQUE: si UN solo enemigo toca un borde,
        # cambia la dirección de todos y todos bajan un nivel.
        borde = any(e.right >= ANCHO or e.left <= 0 for e in self.enemigos)
        if borde:
            self.dir_enemigos *= -1        # 1 -> -1 o -1 -> 1
            for e in self.enemigos:
                e.y += 20                  # bajan un nivel
        # Después, todos avanzan 3 px en la dirección actual.
        for e in self.enemigos:
            e.x += 3 * self.dir_enemigos

    def colisiones_bala_enemigo(self):
        # Doble recorrido bala x enemigo, ambos sobre copias porque borramos.
        for b in self.balas[:]:
            for e in self.enemigos[:]:
                if b.colliderect(e):       # ¿se superponen los dos rectángulos?
                    self.balas.remove(b)   # la bala se gasta...
                    self.enemigos.remove(e)  # ...y el enemigo muere
                    self.puntos += 10
                    # Explosión roja/naranja centrada en el enemigo. gravity=0
                    # porque estamos en el espacio: las chispas no caen.
                    self.particulas.emit(e.centerx, e.centery, count=25,
                                         color=(255, 120, 60), speed=(80, 260),
                                         life=(0.3, 0.7), size=(2, 5), gravity=0)
                    # break: esta bala ya no existe, pasamos a la siguiente.
                    # Sin esto intentaríamos borrarla de nuevo y daría error.
                    break

    def colisiones_con_nave(self):
        ahora = pygame.time.get_ticks()    # milisegundos desde que arrancó pygame

        # Derrota inmediata: algún enemigo llegó al fondo de la pantalla.
        if any(e.bottom >= ALTO for e in self.enemigos):
            self.vidas = 0
            self.estado = "perdiste"
            return

        # Mientras dura el parpadeo la nave es invulnerable: salimos sin
        # revisar choques. Esto evita perder todas las vidas de golpe.
        if ahora < self.invulnerable_hasta:
            return

        for e in self.enemigos[:]:
            if e.colliderect(self.nave):
                self.enemigos.remove(e)    # el enemigo que chocó desaparece
                self.vidas -= 1
                # Chispas verdes (color de la nave) más grandes y lentas.
                self.particulas.emit(self.nave.centerx, self.nave.centery,
                                     count=40, color=(0, 255, 120),
                                     speed=(60, 200), life=(0.4, 0.9),
                                     size=(3, 6), gravity=0)
                # Arranca la ventana de invulnerabilidad: termina 1 s más tarde.
                self.invulnerable_hasta = ahora + PARPADEO_MS
                if self.vidas <= 0:
                    self.estado = "perdiste"
                break                      # un solo golpe por frame

    # ================================================================== #
    #  DIBUJO  (el motor llama a esto después de la lógica, cada frame)
    # ================================================================== #
    def nave_visible(self):
        """True si hay que dibujar la nave; durante el parpadeo alterna."""
        ahora = pygame.time.get_ticks()
        if ahora >= self.invulnerable_hasta:
            return True                    # fuera del parpadeo: siempre visible
        # Dentro del parpadeo: dividimos el tiempo en tramos de 100 ms y
        # dibujamos solo los tramos pares => titila ~5 veces por segundo.
        return (ahora // INTERVALO_PARPADEO_MS) % 2 == 0

    def draw_game_elements(self):
        # Se pinta de atrás hacia adelante: lo último dibujado queda encima.
        self.screen.fill((10, 10, 20))     # 1) fondo (borra el frame anterior)

        if self.nave_visible():            # 2) nave (puede estar "apagada")
            pygame.draw.rect(self.screen, (0, 255, 120), self.nave)
        for b in self.balas:               # 3) balas
            pygame.draw.rect(self.screen, (255, 255, 100), b)
        for e in self.enemigos:            # 4) enemigos
            pygame.draw.rect(self.screen, (255, 80, 80), e)

        # 5) Partículas (encima de los enemigos, debajo del HUD).
        self.particulas.draw(self.screen)

        # 6) HUD (puntos arriba a la izquierda, vidas arriba a la derecha),
        # con el componente Label del motor.
        Label(f"Puntos: {self.puntos}", (10, 8), 30, BLANCO).draw(self.screen)
        Label(f"Vidas: {self.vidas}", (ANCHO - 10, 8), 30, BLANCO,
              align="topright").draw(self.screen)
        pygame.display.set_caption(f"Space Invaders - Puntos: {self.puntos}")

        # 7) Si la partida terminó, el cartel va encima de todo lo demás.
        if self.estado != "jugando":
            self.dibujar_final()
        # (El motor hace pygame.display.flip() solo, después de este método.)

    def dibujar_final(self):
        # Velo negro semitransparente: SRCALPHA permite el canal alfa (150/255).
        velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        velo.fill((0, 0, 0, 150))
        self.screen.blit(velo, (0, 0))

        if self.estado == "ganaste":
            texto, color = "¡Ganaste!", (120, 255, 140)
        else:
            texto, color = "Game Over", (255, 90, 90)

        # align="center" centra el texto en el punto indicado.
        Label(texto, (ANCHO // 2, ALTO // 2 - 30), font=self.fuente_grande,
              color=color, align="center").draw(self.screen)
        Label(f"Puntos: {self.puntos}  -  R para reiniciar",
              (ANCHO // 2, ALTO // 2 + 30), 32, AMARILLO,
              align="center").draw(self.screen)


# Este bloque solo corre si ejecutás `python invaders.py` directamente
# (no si otro archivo hace `import invaders`).
if __name__ == "__main__":
    SpaceInvaders().run()
