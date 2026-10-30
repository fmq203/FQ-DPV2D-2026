# aventura/game.py
import os

import pygame

from engine.game_loop import Game
from engine.inventory import Item
from engine.asset_manager import AssetManager
from engine.audio import AudioManager
from aventura import art
from aventura.data.items import ITEMS
from aventura.state import GameState
from aventura.scenes.menu_scene import MenuScene
from aventura.scenes.game_scene import GameScene
from aventura.scenes.end_scenes import GameOverScene, VictoryScene
from aventura.scenes.credits_scene import CreditsScene

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
        self.checkpoint = None  # estado al empezar la payada (para "Reintentar payada")
        self.music_on = True
        self.music_track = self.music_playing = None  # tema pedido / tema sonando
        self.load_assets()

        self.add_scene("menu", MenuScene)
        self.add_scene("game", GameScene)
        self.add_scene("game_over", GameOverScene)
        self.add_scene("victory", VictoryScene)
        self.add_scene("credits", CreditsScene)
        self.change_scene("menu")

    def load_assets(self):
        # Fondos PNG (o placeholder por código si faltan, ver art.py); sonidos y música .wav.
        for room in ("menu", "rambla", "mercado", "tablado"):
            self.assets.images[f"bg_{room}"] = art.make_background(
                room, (ANCHO, ALTO) if room == "menu" else (art.W, art.H))
        for name in ("click", "pickup", "win", "lose", "talk", "combine", "nope", "bombo"):
            self.audio.load_sound(name, os.path.join(self.assets_dir, "audio", f"{name}.wav"))

    # ---------------------------------------------------------------- música
    def play_music(self, track):
        """Música de fondo por lugar (assets/audio/musica_<track>.wav, ver tools/gen_musica.py).
        Si ya suena ese tema no la reinicia; si cambia, entra con un fundido."""
        self.music_track = track
        if not (self.audio.enabled and self.music_on):
            return
        if self.music_playing == track and pygame.mixer.music.get_busy():
            return
        path = os.path.join(self.assets_dir, "audio", f"musica_{track}.wav")
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.35)
            pygame.mixer.music.play(-1, fade_ms=900)
            self.music_playing = track
        except pygame.error as e:
            print(f"No se pudo reproducir la música '{path}': {e}")

    def stop_music(self):
        self.music_playing = None
        self.audio.stop_music()

    def toggle_music(self):
        self.music_on = not self.music_on
        if self.music_on:
            self.play_music(self.music_track)
        else:
            self.stop_music()

    # --------------------------------------------------------------- partida
    def new_game(self):
        """Reinicia el estado y arranca la partida."""
        self.state = GameState()
        self.checkpoint = None
        self.change_scene("game")

    def save_checkpoint(self):
        """Se guarda al aceptar la payada: si se pierde, se puede reintentar desde ahí."""
        s = self.state
        self.checkpoint = (s.room, [i.name for i in s.inventory.items], set(s.flags))

    def retry_payada(self):
        room, items, flags = self.checkpoint
        self.state = GameState()
        self.state.room, self.state.flags = room, set(flags)
        for key in items:
            self.state.inventory.add(Item(key, art.make_icon(key), ITEMS[key][1]))
        self.change_scene("game", retry=True)
