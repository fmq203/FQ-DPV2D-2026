# aventura/game.py
import os

from engine.game_loop import Game
from engine.asset_manager import AssetManager
from engine.audio import AudioManager
from aventura import art
from aventura.state import GameState
from aventura.scenes.menu_scene import MenuScene
from aventura.scenes.game_scene import GameScene
from aventura.scenes.end_scenes import GameOverScene, VictoryScene

ANCHO, ALTO = 900, 600


class AventuraGame(Game):
    """Aventura gráfica point-and-click sobre el motor del curso (enfoque escenas)."""

    def __init__(self):
        super().__init__(ANCHO, ALTO, "El Murguista — Aventura en Montevideo", 60)

        self.game_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(self.game_dir, "assets")

        self.assets = AssetManager()
        self.audio = AudioManager()
        self.state = GameState()
        self.load_assets()

        self.add_scene("menu", MenuScene)
        self.add_scene("game", GameScene)
        self.add_scene("game_over", GameOverScene)
        self.add_scene("victory", VictoryScene)
        self.change_scene("menu")

    def load_assets(self):
        # Fondos placeholder generados por código (ver art.py); sonidos .wav reales.
        for room in ("menu", "rambla", "mercado", "tablado"):
            self.assets.images[f"bg_{room}"] = art.make_background(
                room, (ANCHO, ALTO) if room == "menu" else (art.W, art.H))
        for name in ("click", "pickup", "win", "lose", "talk", "combine", "nope", "bombo"):
            self.audio.load_sound(name, os.path.join(self.assets_dir, "audio", f"{name}.wav"))

    def new_game(self):
        """Reinicia el estado y arranca la partida."""
        self.state = GameState()
        self.change_scene("game")
