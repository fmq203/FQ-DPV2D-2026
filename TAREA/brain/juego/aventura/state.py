# aventura/state.py
from engine.inventory import Inventory


class GameState:
    """Estado persistente de la partida (vive en game.state, no en las escenas)."""

    def __init__(self):
        self.room = "rambla"
        self.inventory = Inventory(capacity=8)
        self.flags = set()  # puzles resueltos, diálogos vistos...
        self.lives = 3      # errores permitidos en la payada
        self.clock = 0      # frames de juego transcurridos (no corre en pausa)
        self.timers = {}    # nombre -> frame en que arrancó (ej. el chorizo en la parrilla)
        self.gone = set()   # hotspots que ya terminaron de irse de la pantalla (gato, perro)
