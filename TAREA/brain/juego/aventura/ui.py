# aventura/ui.py
from engine.ui import Button


class SoundButton(Button):
    """Button del motor + sonido de click (requisito: feedback sonoro en la UI)."""

    def __init__(self, game, *args, sound="click", **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
        self.sound = sound

    def handle_event(self, event):
        if self.rect.collidepoint(getattr(event, "pos", (-1, -1))):
            if getattr(event, "button", None) == 1:
                self.game.audio.play_sound(self.sound)
        super().handle_event(event)
