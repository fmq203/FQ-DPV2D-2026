# aventura/scenes/credits_scene.py
import pygame

from engine.ui import Scene
from aventura.data.creditos import CREDITOS
from aventura.scenes.menu_scene import MenuScene
from aventura.ui import SoundButton


class CreditsScene(Scene):
    """Créditos sobre el fondo del menú; la lista sale de data/creditos.py."""

    def __init__(self, game):
        super().__init__(game)
        self.title = MenuScene._outlined(pygame.font.Font(None, 72), "CRÉDITOS", (255, 200, 60))
        sec_font, line_font = pygame.font.Font(None, 30), pygame.font.Font(None, 28)
        self.lines = []  # (superficie, espacio_antes)
        for section, names in CREDITOS:
            self.lines.append((MenuScene._outlined(sec_font, section, (120, 220, 255)), 12))
            for name in names:
                self.lines.append((MenuScene._outlined(line_font, name, (245, 245, 250)), 0))
        w = game.screen.get_width()
        self.button = SoundButton(game, w // 2 - 130, 530, 260, 50, "Volver al menú",
                                  lambda: game.change_scene("menu"), font_size=34)

    def handle_events(self, events):
        for event in events:
            self.button.handle_event(event)

    def draw(self, surface):
        surface.blit(self.game.assets.get_image("bg_menu"), (0, 0))
        veil = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        veil.fill((10, 10, 25, 170))
        surface.blit(veil, (0, 0))
        cx = surface.get_width() // 2
        surface.blit(self.title, self.title.get_rect(centerx=cx, y=24))
        y = 100
        for img, gap in self.lines:
            y += gap
            surface.blit(img, img.get_rect(centerx=cx, y=y))
            y += img.get_height() - 6
        self.button.draw(surface)
