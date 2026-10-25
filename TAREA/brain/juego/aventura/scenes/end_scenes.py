# aventura/scenes/end_scenes.py
import pygame

from engine.ui import Scene
from aventura.ui import SoundButton


class _EndScene(Scene):
    TEXT, SUB, COLOR, SOUND = "", "", (255, 255, 255), "click"

    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 90)
        self.sub_font = pygame.font.Font(None, 34)
        w = game.screen.get_width()
        self.button = SoundButton(game, w // 2 - 130, 380, 260, 56, "Volver al menú",
                                  lambda: game.change_scene("menu"))

    def on_enter(self):
        self.game.audio.play_sound(self.SOUND)

    def handle_events(self, events):
        for event in events:
            self.button.handle_event(event)

    def draw(self, surface):
        surface.fill((10, 10, 20))
        img = self.font.render(self.TEXT, True, self.COLOR)
        surface.blit(img, img.get_rect(center=(surface.get_width() // 2, 220)))
        sub = self.sub_font.render(self.SUB, True, (220, 220, 235))
        surface.blit(sub, sub.get_rect(center=(surface.get_width() // 2, 300)))
        self.button.draw(surface)


class GameOverScene(_EndScene):
    TEXT, COLOR, SOUND = "GAME OVER", (230, 60, 60), "lose"
    SUB = "¡Vayan pelando las chauchas! El Contramaestre te sacó del tablado."


class VictoryScene(_EndScene):
    TEXT, COLOR, SOUND = "¡VICTORIA!", (255, 215, 0), "win"
    SUB = "¡Uruguay nomá! Recuperaste el bombo: que empiece el Carnaval."
