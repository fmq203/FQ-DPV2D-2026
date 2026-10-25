# aventura/scenes/game_scene.py
"""
Escena de juego: aventura point-and-click.

Máquina de estados (FSM) de la interacción:
    IDLE ──click──▶ WALKING ──llega──▶ (ejecuta acción) ──▶ IDLE | SPEAKING | DIALOGUE
    SPEAKING (Tano/NPC hablan; click salta la línea) ──▶ IDLE o acción encadenada
    DIALOGUE (opciones múltiples con mouse)           ──▶ IDLE
Dentro de IDLE/WALKING se arma el comando: verbo → [ítem] → objetivo ("Usar termo con mate").
"""
import pygame

from engine.ui import Scene
from engine.cursor import Cursor
from engine.hotspot import Hotspot
from engine.inventory import Item
from engine.dialogue import DialogueBox
from engine.dialogue_manager import DialogueManager
from engine.walkmask import WalkMask
from aventura import art
from aventura.data import dialogs
from aventura.data.items import ITEMS, RECIPES
from aventura.data.rooms import ROOMS, TANO

BAR_Y = 450  # la barra de verbos/inventario ocupa y >= 450
VERBS = ["Mirar", "Agarrar", "Usar", "Hablar", "Dar"]
INV_ORIGIN, INV_SLOT = (360, BAR_Y + 42), 64  # 8 slots x 64 = 512 px de ancho
SPEED = 3.2

IDLE, WALKING, SPEAKING, DIALOGUE = "IDLE", "WALKING", "SPEAKING", "DIALOGUE"

SPEAKER_COLORS = {
    "Tano": TANO, "Pescador": (120, 220, 170), "Parrillero": (255, 170, 120),
    "Contramaestre": (130, 190, 255), "Narrador": (200, 200, 200),
}
DEFAULTS = {
    "Mirar": "No veo nada especial en {n}.",
    "Agarrar": "No puedo llevarme eso. Difícil que el chancho chifle.",
    "Usar": "No se me ocurre cómo usar eso. Despacito y por las piedras.",
    "Hablar": "No creo que me conteste. En boca cerrada no entran moscas.",
    "Dar": "Primero tengo que elegir qué dar, en el inventario.",
}


class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.state = game.state
        self.fsm = IDLE
        self.verb, self.pending = "Mirar", None
        self.font = pygame.font.Font(None, 28)
        self.small = pygame.font.Font(None, 24)
        self.cursor = Cursor()
        self.dialogue = DialogueManager(game.screen, font_size=30)
        self.box = DialogueBox(game.screen, font_size=26, height=200)
        self.box.on_confirm = lambda: self.play("click")
        self.box.on_end = self._dialog_ended
        self.verb_rects = {
            v: pygame.Rect(10 + (i % 3) * 112, BAR_Y + 42 + (i // 3) * 48, 104, 40)
            for i, v in enumerate(VERBS)
        }
        self.icons = {k: art.make_icon(k) for k in ITEMS}
        self.recipes = {k: Item(v[0], self.icons[v[0]], ITEMS[v[0]][1]) for k, v in RECIPES.items()}
        self.queue, self.after, self.pending_end = [], None, None
        self.t, self.facing = 0, 1
        self.target, self.on_arrive = None, None
        self.hovered_name, self.hovered = "", False
        self.title_until = 0
        self.load_room(self.state.room)

    def on_enter(self):
        self.say([("Tano", "Mañana arranca el Carnaval y me robaron el bombo de la murga..."),
                  ("Tano", "¡Tengo que recuperarlo antes de la prueba de admisión!"),
                  ("Tano", "Y encima llueve desde que empezó la primavera... gracias, Niño.")])

    def on_exit(self):
        # Cursor.draw oculta el puntero del sistema: lo restauramos para menú/finales.
        pygame.mouse.set_visible(True)

    # ------------------------------------------------- API para los diálogos
    @property
    def inventory(self):
        return self.state.inventory

    def has_flag(self, f):
        return f in self.state.flags

    def flag(self, f):
        self.state.flags.add(f)

    def play(self, sound):
        self.game.audio.play_sound(sound)

    def trade(self, take, give, flag=None):
        self.inventory.remove(take)
        self.give(give)
        if flag:
            self.flag(flag)

    def finish_after(self, end):
        self.pending_end = end

    # ------------------------------------------------------------- escenarios
    def load_room(self, room, spawn_x=None):
        self.state.room = room
        self.room = ROOMS[room]
        self.walk = WalkMask((art.W, art.H), self.room["walk"])
        self.hotspots = []
        for d in self.room["hotspots"]:
            h = Hotspot(d["rect"], d["name"])
            h.data = d
            self.hotspots.append(h)
        sx, sy = self.room["start"]
        self.pos = (spawn_x if spawn_x is not None else sx, sy)
        self.target = self.on_arrive = None
        self.title_until = pygame.time.get_ticks() + 2500

    def _visible(self, h):
        d = h.data
        if d.get("show_if") and not self.has_flag(d["show_if"]):
            return False
        return not (d.get("hide_if") and self.has_flag(d["hide_if"]))

    def _hotspot_at(self, pos):
        for h in reversed(self.hotspots):
            if self._visible(h) and h.contains(pos):
                return h
        return None

    def _inv_slot_at(self, pos):
        for i, item in enumerate(self.inventory.items):
            if self.inventory._slot_rect(INV_ORIGIN, i, INV_SLOT, True).collidepoint(pos):
                return item
        return None

    # --------------------------------------------------------------- hablar
    def say(self, lines, after=None):
        if isinstance(lines, (str, tuple)):
            lines = [lines]
        self.queue = [("Tano", l) if isinstance(l, str) else l for l in lines]
        self.after = after
        self.fsm = SPEAKING
        self.target = self.on_arrive = None
        self._next_line()

    def _anchor(self, speaker):
        if speaker == "Tano":
            return (self.pos[0], self.pos[1] - 100 * self._scale())
        for h in self.hotspots:
            if h.name == speaker:
                return (h.rect.centerx, h.rect.top - 6)
        return (art.W // 2, 90)

    def _next_line(self):
        if self.queue:
            speaker, text = self.queue.pop(0)
            self.dialogue.show_message(text, max(1.8, 0.06 * len(text)),
                                       color=SPEAKER_COLORS.get(speaker, (255, 255, 255)),
                                       center_at=self._anchor(speaker))
            self.speaker = speaker
            self.play("talk")
            return
        self.fsm = IDLE
        after, self.after = self.after, None
        if after:
            after()

    # ------------------------------------------------------ dialogo (opciones)
    def start_dialog(self, name):
        self.box.start(dialogs.build(name, self), "start")
        self.fsm = DIALOGUE
        self.dialogue.clear_message()

    def _dialog_ended(self):
        self.fsm = IDLE
        if self.pending_end:
            self._end(self.pending_end)
        elif self.has_flag("payada_ganada") and not self.has_flag("bombo_avisado"):
            self.flag("bombo_avisado")
            self.say("¡Uruguay nomá! Ahí está el bombo, voy a buscarlo.")

    def _end(self, which):
        self.game.change_scene(which)

    # -------------------------------------------------------- resultados
    def give(self, key):
        label, desc = ITEMS[key]
        self.inventory.add(Item(key, self.icons[key], desc))

    def apply(self, res):
        if isinstance(res, (str, list)):
            return self.say(res)
        if "if_flag" in res and not self.has_flag(res["if_flag"]):
            return self.apply(res.get("else", "No pasa nada."))
        if "if_flag_not" in res and self.has_flag(res["if_flag_not"]):
            return self.apply(res.get("else", "No pasa nada."))
        for k in ([res["take"]] if isinstance(res.get("take"), str) else res.get("take", [])):
            self.inventory.remove(k)
        if res.get("give"):
            self.give(res["give"])
        if res.get("flag"):
            self.flag(res["flag"])
        sound = res.get("sound") or ("pickup" if res.get("give") else None)
        if sound:
            self.play(sound)

        def finish():
            if res.get("talk"):
                self.start_dialog(res["talk"])
            elif res.get("end"):
                self._end(res["end"])

        if res.get("say"):
            self.say(res["say"], after=finish)
        else:
            finish()

    # ----------------------------------------------------------- interacción
    def walk_to(self, point, on_arrive=None):
        self.target = self.walk.nearest(point)
        self.on_arrive = on_arrive
        self.fsm = WALKING

    def interact(self, h, verb, item=None):
        d = h.data
        self.play("click")
        if "exit" in d:
            room, x = d["exit"]
            return self.walk_to(d["stand"], lambda: self._go(room, x))
        if verb != "Mirar" and d.get("needs") and not self.has_flag(d["needs"]):
            return self.say(d.get("blocked", "No puedo hacer eso todavía."))
        if verb == "Dar" and not item:
            return self.say(DEFAULTS["Dar"])
        self.walk_to(d["stand"], lambda: self._do(h, verb, item))

    def _go(self, room, x):
        self.play("click")
        self.load_room(room, x)
        self.fsm = IDLE

    def _do(self, h, verb, item):
        d = h.data
        self.fsm = IDLE
        res = d["acts"].get(f"{verb}:{item}" if item else verb)
        if res is None:
            if item:
                res = "Eso no sirve con {n}.".format(n=d["name"]) if verb == "Usar" \
                    else f"No creo que {d['name']} quiera eso."
                self.play("nope")
            else:
                res = DEFAULTS[verb].format(n=d["name"])
        self.apply(res)

    def _inventory_click(self, item):
        key = item.name
        if self.pending:
            first, self.pending = self.pending, None
            if first == key:
                return
            if self.verb == "Usar":
                result = self.inventory.combine(first, key, self.recipes)
                if result:
                    self.play("combine")
                    return self.say(RECIPES[frozenset((first, key))][1])
            self.play("nope")
            return self.say("No creo que eso funcione... ni atado con alambre.")
        if self.verb in ("Usar", "Dar"):
            self.pending = key
        elif self.verb == "Mirar":
            self.say(item.description)
        elif self.verb == "Agarrar":
            self.say("Ya lo tengo.")
        else:
            self.say("Hablarle a un objeto es de locos.")

    # -------------------------------------------------------------- eventos
    def handle_events(self, events):
        for event in events:
            if self.fsm == DIALOGUE:
                self.box.handle_event(event)
                continue
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.pending = None
            if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                continue
            if self.fsm == SPEAKING:
                self.dialogue.clear_message()  # click = saltar la línea
                continue
            self._click(event.pos)

    def _click(self, pos):
        for v, r in self.verb_rects.items():
            if r.collidepoint(pos):
                self.verb, self.pending = v, None
                return self.play("click")
        item = self._inv_slot_at(pos)
        if item:
            self.play("click")
            return self._inventory_click(item)
        if pos[1] >= BAR_Y:
            return
        h = self._hotspot_at(pos)
        if h:
            item, self.pending = self.pending, None
            return self.interact(h, self.verb, item)
        self.pending = None
        self.walk_to(pos)

    # ------------------------------------------------------------ actualizar
    def _scale(self):
        return 0.7 + 0.4 * min(1, max(0, (self.pos[1] - 300) / 150))

    def update(self):
        self.t += 1
        self.dialogue.update()
        if self.fsm == SPEAKING and self.dialogue.active_message is None:
            self._next_line()
        if self.fsm == WALKING and self.target:
            old = self.pos
            self.pos, arrived = self.walk.step(self.pos, self.target, SPEED * self._scale())
            if self.pos[0] != old[0]:
                self.facing = 1 if self.pos[0] > old[0] else -1
            if arrived:
                self.target, cb, self.on_arrive = None, self.on_arrive, None
                self.fsm = IDLE
                if cb:
                    cb()
        pos = pygame.mouse.get_pos()
        item = self._inv_slot_at(pos)
        h = self._hotspot_at(pos) if pos[1] < BAR_Y else None
        self.hovered = bool(h)
        self.hovered_name = (h.name if h else "") or (ITEMS[item.name][0] if item else "")

    # ---------------------------------------------------------------- dibujo
    def _command_line(self):
        v = self.verb
        if self.pending:
            link = "con" if v == "Usar" else "a"
            return f"{v} {ITEMS[self.pending][0]} {link} {self.hovered_name}".strip()
        return f"{v} {self.hovered_name}".strip()

    def draw(self, surface):
        surface.blit(self.game.assets.get_image(f"bg_{self.state.room}"), (0, 0))
        props = [h for h in self.hotspots if self._visible(h) and h.data["art"][0] not in ("zone", "item")]
        props.sort(key=lambda h: h.rect.bottom)
        drawn = False
        for h in props:
            if not drawn and h.rect.bottom > self.pos[1]:
                self._draw_tano(surface)
                drawn = True
            art.draw_prop(surface, h.data["art"][0], h.rect, h.data["art"][1], h.data["id"])
        if not drawn:
            self._draw_tano(surface)
        for h in self.hotspots:
            if self._visible(h) and h.data["art"][0] == "item":
                art.draw_prop(surface, "item", h.rect, h.data["art"][1])
        self.dialogue.draw()
        if pygame.time.get_ticks() < self.title_until:
            title = self.font.render(self.room["title"], True, (255, 255, 255))
            surface.blit(title, title.get_rect(topleft=(12, 8)))
        self._draw_bar(surface)
        if self.fsm == DIALOGUE:
            self.box.draw()
        self.cursor.draw(surface, self.hovered)

    def _draw_tano(self, surface):
        speaking = self.fsm == SPEAKING and getattr(self, "speaker", "") == "Tano"
        art.draw_tano(surface, self.pos, self._scale(), self.facing, self.t,
                      self.fsm == WALKING, speaking)

    def _draw_bar(self, surface):
        pygame.draw.rect(surface, (20, 20, 35), (0, BAR_Y, surface.get_width(), surface.get_height() - BAR_Y))
        pygame.draw.line(surface, (110, 110, 160), (0, BAR_Y), (surface.get_width(), BAR_Y), 2)
        cmd = self.font.render(self._command_line(), True, (120, 220, 255))
        surface.blit(cmd, cmd.get_rect(centerx=surface.get_width() // 2, y=BAR_Y + 10))
        for v, r in self.verb_rects.items():
            on = v == self.verb
            pygame.draw.rect(surface, (255, 220, 0) if on else (70, 70, 110), r, border_radius=4)
            txt = self.font.render(v, True, (0, 0, 0) if on else (255, 255, 255))
            surface.blit(txt, txt.get_rect(center=r.center))
        self.inventory.selected = self.inventory.get(self.pending) if self.pending else None
        self.inventory.draw(surface, INV_ORIGIN, slot=INV_SLOT, horizontal=True)
