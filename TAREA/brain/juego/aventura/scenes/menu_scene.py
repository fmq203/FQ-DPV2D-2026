# aventura/scenes/menu_scene.py
import pygame

from engine.ui import Scene
from aventura.ui import SoundButton


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.title = self._outlined(pygame.font.Font(None, 96), "EL MURGUISTA", (255, 200, 60))
        self.subtitle = self._outlined(pygame.font.Font(None, 36),
                                       "Una aventura gráfica en Montevideo", (240, 240, 255))
        w = game.screen.get_width()
        self.buttons = [
            SoundButton(game, w // 2 - 130, 300, 260, 56, "Comenzar Juego", game.new_game),
            SoundButton(game, w // 2 - 130, 380, 260, 56, "Salir", self.quit),
        ]

    @staticmethod
    def _outlined(font, text, color):
        """Texto con contorno negro: se lee sobre el fondo detallado."""
        base = font.render(text, True, color)
        out = pygame.Surface((base.get_width() + 8, base.get_height() + 8), pygame.SRCALPHA)
        shadow = font.render(text, True, (0, 0, 0))
        for dx in range(0, 9, 2):
            for dy in range(0, 9, 2):
                out.blit(shadow, (dx, dy))
        out.blit(base, (4, 4))
        return out

    def quit(self):
        self.game.running = False

    def handle_events(self, events):
        for event in events:
            for b in self.buttons:
                b.handle_event(event)

    def draw(self, surface):
        surface.blit(self.game.assets.get_image("bg_menu"), (0, 0))
        surface.blit(self.title, self.title.get_rect(centerx=surface.get_width() // 2, y=130))
        surface.blit(self.subtitle, self.subtitle.get_rect(centerx=surface.get_width() // 2, y=215))
        for b in self.buttons:
            b.draw(surface)
