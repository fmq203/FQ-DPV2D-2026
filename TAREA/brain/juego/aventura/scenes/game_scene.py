# aventura/scenes/game_scene.py
"""
Escena de juego: aventura point-and-click.

Máquina de estados (FSM) de la interacción:
    IDLE ──click──▶ WALKING ──llega──▶ (ejecuta acción) ──▶ IDLE | SPEAKING | DIALOGUE
    SPEAKING (Tano/NPC hablan; click salta la línea) ──▶ IDLE o acción encadenada
    DIALOGUE (opciones múltiples con mouse)           ──▶ IDLE
Dentro de IDLE/WALKING se arma el comando: verbo → [ítem] → objetivo ("Usar termo con mate").
"""
import math

import pygame

from engine.ui import Scene
from engine.cursor import Cursor
from engine.hotspot import Hotspot
from engine.inventory import Item
from engine.dialogue import DialogueBox
from engine.dialogue_manager import DialogueManager
from engine.walkmask import WalkMask
from aventura import art
from aventura.ui import SoundButton
from aventura.data import dialogs
from aventura.data.items import ITEMS, RECIPES
from aventura.data.rooms import ROOMS, TANO, TIMERS

BAR_Y = 450  # la barra de verbos/inventario ocupa y >= 450
VERBS = ["Mirar", "Agarrar", "Usar", "Hablar", "Dar"]
INV_ORIGIN, INV_SLOT = (360, BAR_Y + 42), 64  # 8 slots x 64 = 512 px de ancho
SPEED = 3.2

IDLE, WALKING, SPEAKING, DIALOGUE = "IDLE", "WALKING", "SPEAKING", "DIALOGUE"

SPEAKER_COLORS = {
    "Tano": TANO, "Pescador": (120, 220, 170), "Asador": (255, 170, 120),
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
    def __init__(self, game, retry=False):
        super().__init__(game)
        self.state = game.state
        self.retry = retry  # True: se vuelve directo a la payada (desde Game Over)
        self.paused = False
        w = game.screen.get_width()
        self.pause_buttons = [
            SoundButton(game, w // 2 - 140, 200, 280, 52, "Continuar", self.toggle_pause, font_size=34),
            SoundButton(game, w // 2 - 140, 265, 280, 52, "", game.toggle_music, font_size=34),
            SoundButton(game, w // 2 - 140, 330, 280, 52, "Volver al menú",
                        lambda: game.change_scene("menu"), font_size=34),
        ]
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
        if self.retry:
            return self.start_dialog("payada_intro")
        self.say([("Tano", "Mañana arranca el Carnaval y me robaron el bombo de la murga..."),
                  ("Tano", "¡Tengo que recuperarlo antes de la prueba de admisión!"),
                  ("Tano", "Y encima llueve desde que empezó la primavera... gracias, Niño.")])

    def on_exit(self):
        # Cursor.draw oculta el puntero del sistema: lo restauramos para menú/finales.
        pygame.mouse.set_visible(True)

    # ------------------------------------------------- API para los diálogos
    def toggle_pause(self):
        self.paused = not self.paused

    @property
    def inventory(self):
        return self.state.inventory

    def has_flag(self, f):
        return f in self.state.flags

    def flag(self, f):
        self.state.flags.add(f)

    def play(self, sound):
        self.game.audio.play_sound(sound)

    def finish_after(self, end):
        self.pending_end = end

    # ------------------------------------------------------------- escenarios
    def load_room(self, room, spawn_x=None):
        self.state.room = room
        self.room = ROOMS[room]
        self.game.play_music(room)  # cada lugar tiene su tema (musica_<room>.wav)
        self.walk = WalkMask((art.W, art.H), self.room["walk"])
        self.hotspots = []
        for d in self.room["hotspots"]:
            h = Hotspot(d["rect"], d["name"])
            h.data = d
            self.hotspots.append(h)
        self.leaving = {}  # id -> desplazamiento x de los que se están yendo (ver "leave" en rooms.py)
        for h in self.hotspots:  # si ya se fueron antes (o se volvió al lugar), no repetir la salida
            if h.data.get("leave") and self.has_flag(h.data["hide_if"]):
                self.state.gone.add(h.data["id"])
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
        for k in ([res["give"]] if isinstance(res.get("give"), str) else res.get("give", [])):
            self.give(k)
        if res.get("flag"):
            self.flag(res["flag"])
        for f in res.get("unflag", []):
            self.state.flags.discard(f)
        if res.get("timer"):
            self.state.timers[res["timer"]] = self.state.clock
        if res.get("timer_stop"):
            self.state.timers.pop(res["timer_stop"], None)
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
                    recipe = RECIPES[frozenset((first, key))]
                    for kept in recipe[2] if len(recipe) > 2 else ():
                        self.give(kept)  # ej. el termo sigue en el inventario después de cebar
                    return self.say(recipe[1])
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.play("click")
                self.toggle_pause()
                continue
            if self.paused:
                for b in self.pause_buttons:
                    b.handle_event(event)
                continue
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
        if self.paused:
            return
        self.t += 1
        self.state.clock += 1
        self._update_timers()
        self._update_leaving()
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

    def _update_timers(self):
        """Mini-retos de tiempo (TIMERS en rooms.py): al cumplirse cada etapa se activa su flag y,
        si Tano está en ese escenario y libre, avisa en voz alta."""
        for name, start in list(self.state.timers.items()):
            room, stages = TIMERS[name]
            for frames, flag, aviso in stages:
                if self.state.clock - start >= frames and not self.has_flag(flag):
                    self.flag(flag)
                    if self.state.room == room and self.fsm == IDLE:
                        self.say(aviso)
            if self.has_flag(stages[-1][1]):
                del self.state.timers[name]  # última etapa: el temporizador terminó

    def _update_leaving(self):
        """Hotspots con "leave": cuando se activa su hide_if dejan de ser clickeables, pero se siguen
        dibujando mientras caminan hasta to_x; al llegar quedan en state.gone."""
        for h in self.hotspots:
            leave, hid = h.data.get("leave"), h.data["id"]
            if not leave or hid in self.state.gone or not self.has_flag(h.data["hide_if"]):
                continue
            dist = leave["to_x"] - h.rect.x
            off = self.leaving.get(hid, 0.0) + leave["speed"] * (1 if dist > 0 else -1)
            if abs(off) >= abs(dist):
                self.state.gone.add(hid)
                self.leaving.pop(hid, None)
            else:
                self.leaving[hid] = off

    def _draw_hotspot(self, surface, h):
        hid, (kind, color) = h.data["id"], h.data["art"]
        rect, flip = h.rect, False
        if hid in self.leaving:
            leave, off = h.data["leave"], self.leaving[hid]
            hop = abs(math.sin(off / max(leave["speed"], 1) * 0.5)) * leave.get("hop", 0)
            rect = h.rect.move(int(off), -int(hop))
            flip = leave["to_x"] > h.rect.x  # los sprites miran a la izquierda
        art.draw_prop(surface, kind, rect, color, self._sprite_id(h), flip)

    # ---------------------------------------------------------------- dibujo
    def _command_line(self):
        v = self.verb
        if self.pending:
            link = "con" if v == "Usar" else "a"
            return f"{v} {ITEMS[self.pending][0]} {link} {self.hovered_name}".strip()
        return f"{v} {self.hovered_name}".strip()

    def draw(self, surface):
        surface.blit(self.game.assets.get_image(f"bg_{self.state.room}"), (0, 0))
        props = [h for h in self.hotspots
                 if (self._visible(h) or h.data["id"] in self.leaving) and h.data["art"][0] not in ("zone", "item")]
        props.sort(key=lambda h: h.rect.bottom)
        drawn = False
        for h in props:
            if not drawn and h.rect.bottom > self.pos[1]:
                self._draw_tano(surface)
                drawn = True
            self._draw_hotspot(surface, h)
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
            self._shade(surface, (0, BAR_Y, surface.get_width(), surface.get_height() - BAR_Y), 170)
            self.box.draw()
        if self.paused:
            self._draw_pause(surface)
        self.cursor.draw(surface, self.hovered and not self.paused)

    def _sprite_id(self, h):
        variants = h.data.get("sprite_if", [])
        if isinstance(variants, tuple):
            variants = [variants]
        sprite = h.data["id"]
        for flag, alt in variants:  # gana la última variante cuyo flag esté activo
            if self.has_flag(flag):
                sprite = alt
        return sprite

    @staticmethod
    def _shade(surface, rect, alpha):
        veil = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        veil.fill((0, 0, 0, alpha))
        surface.blit(veil, pygame.Rect(rect).topleft)

    def _draw_pause(self, surface):
        self._shade(surface, surface.get_rect(), 170)
        title = pygame.font.Font(None, 64).render("PAUSA", True, (255, 200, 60))
        surface.blit(title, title.get_rect(centerx=surface.get_width() // 2, y=120))
        self.pause_buttons[1].text = f"Música: {'Sí' if self.game.music_on else 'No'}"
        for b in self.pause_buttons:
            b.draw(surface)
        hint = self.small.render("ESC para seguir jugando", True, (200, 200, 220))
        surface.blit(hint, hint.get_rect(centerx=surface.get_width() // 2, y=400))

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
