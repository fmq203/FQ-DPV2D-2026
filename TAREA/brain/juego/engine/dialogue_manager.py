"""
engine/dialogue_manager.py

Muestra mensajes/diálogos en pantalla, con duración opcional.
"""

import pygame


class DialogueManager:
    def __init__(self, screen, font_size=50, color=(255, 255, 255)):
        self.screen = screen
        self.font = pygame.font.Font(None, font_size)
        self.color = color

        self.active_message = None
        self.message_surface = None
        self.message_rect = None
        self.message_timer = 0
        self.message_duration = 0  # 0 => mensaje permanente

    def show_message(self, text, duration_seconds=0, position="center",
                     color=None, center_at=None):
        """Muestra un mensaje. Si la duración es 0, es permanente.

        # [Tarea 2026] `color` (por hablante), `center_at=(x, y)` (texto flotante
        sobre un personaje, se mantiene dentro de la pantalla) y ajuste de línea
        automático para textos largos.
        """
        self.active_message = text
        self.message_surface = self._render(text, color or self.color)

        screen_rect = self.screen.get_rect()
        if center_at is not None:
            self.message_rect = self.message_surface.get_rect(midbottom=center_at)
            self.message_rect.clamp_ip(screen_rect.inflate(-20, -20))
        elif position == "top":
            self.message_rect = self.message_surface.get_rect(
                centerx=screen_rect.centerx, top=20
            )
        else:
            self.message_rect = self.message_surface.get_rect(center=screen_rect.center)

        self.message_duration = duration_seconds * 1000
        self.message_timer = pygame.time.get_ticks()

    def _render(self, text, color):
        # [Tarea 2026] texto con contorno negro y varias líneas (estilo aventura gráfica).
        max_w = self.screen.get_width() - 160
        lines, line = [], ""
        for word in text.split():
            test = (line + " " + word).strip()
            if line and self.font.size(test)[0] > max_w:
                lines.append(line)
                line = word
            else:
                line = test
        lines.append(line)
        h = self.font.get_linesize()
        w = max(self.font.size(l)[0] for l in lines)
        surf = pygame.Surface((w + 4, h * len(lines) + 4), pygame.SRCALPHA)
        for i, l in enumerate(lines):
            for dx, dy in ((0, 0), (4, 0), (0, 4), (4, 4), (2, 0), (2, 4), (0, 2), (4, 2)):
                surf.blit(self.font.render(l, True, (0, 0, 0)), ((w - self.font.size(l)[0]) // 2 + dx, i * h + dy))
            surf.blit(self.font.render(l, True, color), ((w - self.font.size(l)[0]) // 2 + 2, i * h + 2))
        return surf

    def update(self):
        if self.message_duration > 0:
            if pygame.time.get_ticks() - self.message_timer > self.message_duration:
                self.clear_message()

    def draw(self):
        if self.message_surface:
            self.screen.blit(self.message_surface, self.message_rect)

    def clear_message(self):
        self.active_message = None
        self.message_surface = None
        self.message_duration = 0
