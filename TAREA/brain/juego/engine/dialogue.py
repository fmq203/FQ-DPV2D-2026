"""
engine/dialogue.py

Diálogos con ramificaciones (árbol de conversación) y, opcionalmente, la
posibilidad de generar respuestas con IA. Si no hay IA disponible, el juego
funciona igual con los nodos escritos a mano.

Ejemplo de uso:

    nodes = {
        "start": DialogueNode("¡Hola! ¿Qué quieres?", speaker="NPC",
                              choices=[("Comprar", "comprar"), ("Adiós", None)]),
        "comprar": DialogueNode("Aquí tienes.", speaker="NPC"),
    }
    box.start(nodes, "start")
"""

import textwrap

import pygame


class DialogueNode:
    def __init__(self, text, speaker="", choices=None, action=None, portrait=None):
        self.text = text
        self.speaker = speaker
        self.choices = choices or []   # lista de (etiqueta, siguiente_nodo_o_None)
        self.action = action           # callback opcional al entrar
        self.portrait = portrait


class DialogueBox:
    def __init__(self, screen, font_size=26, height=170, width_ratio=0.9):
        self.screen = screen
        self.width = int(screen.get_width() * width_ratio)
        self.height = height
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = (screen.get_width() // 2, screen.get_height() - 10)
        self.font = pygame.font.Font(None, font_size)
        self.small = pygame.font.Font(None, font_size - 4)
        self.nodes = {}
        self.current = None
        self.lines = []
        self.choice_index = 0
        self.active = False
        # [Tarea 2026] soporte de mouse + hooks (sonido al elegir, fin del diálogo)
        self.choice_rects = []
        self.on_confirm = None   # callback() al elegir una opción
        self.on_end = None       # callback() al cerrarse el diálogo

    def start(self, nodes, start="start"):
        self.nodes = nodes
        self.active = True
        self._go_to(start)

    def _go_to(self, name):
        self.current = self.nodes.get(name)
        self.choice_index = 0
        if self.current:
            if self.current.action:
                self.current.action(self.current)
            self.lines = textwrap.wrap(self.current.text, 52)

    def _close(self):
        self.active = False
        if self.on_end:
            self.on_end()

    def handle_event(self, event):
        if not self.active or not self.current:
            return
        # [Tarea 2026] elegir opciones con el mouse
        if event.type == pygame.MOUSEMOTION:
            for i, r in enumerate(self.choice_rects):
                if r.collidepoint(event.pos):
                    self.choice_index = i
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, r in enumerate(self.choice_rects):
                if r.collidepoint(event.pos):
                    self.choice_index = i
                    self._confirm()
                    return
            if not self.current.choices:
                self._confirm()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._confirm()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                if self.current.choices:
                    self.choice_index = (self.choice_index + 1) % len(self.current.choices)
            elif event.key in (pygame.K_UP, pygame.K_w):
                if self.current.choices:
                    self.choice_index = (self.choice_index - 1) % len(self.current.choices)

    def _confirm(self):
        if self.on_confirm:
            self.on_confirm()
        if self.current and self.current.choices:
            _, nxt = self.current.choices[self.choice_index]
            if nxt is None:
                self._close()
            else:
                self._go_to(nxt)
        else:
            self._close()

    def draw(self):
        if not self.active or not self.current:
            return
        panel = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        panel.fill((0, 0, 0, 200))
        self.screen.blit(panel, self.rect.topleft)
        pygame.draw.rect(self.screen, (240, 240, 240), self.rect, 3, border_radius=8)

        x = self.rect.x + 16
        y = self.rect.y + 12
        if self.current.speaker:
            name = self.font.render(self.current.speaker, True, (255, 220, 90))
            self.screen.blit(name, (x, y))
            y += name.get_height() + 4
        for line in self.lines:
            text = self.font.render(line, True, (240, 240, 240))
            self.screen.blit(text, (x, y))
            y += text.get_height() + 2

        self.choice_rects = []
        for index, (label, _) in enumerate(self.current.choices):
            color = (255, 255, 120) if index == self.choice_index else (200, 200, 200)
            text = self.small.render(("> " if index == self.choice_index else "  ") + label,
                                     True, color)
            pos = (x + 20, y + index * (self.small.get_height() + 2))
            self.screen.blit(text, pos)
            self.choice_rects.append(pygame.Rect(pos, text.get_size()).inflate(8, 2))
