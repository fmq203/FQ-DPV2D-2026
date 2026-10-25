"""
Prueba de humo sin ventana ni audio. Desde juego/:
    python tests/smoke_test.py
Juega la partida COMPLETA con eventos reales de mouse:
menú -> 3 escenarios -> puzle del mate (combinación) -> puzle del chori al pan
-> payada (diálogo con opciones) -> victoria; y una segunda partida que pierde la payada.
"""
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

from aventura.game import AventuraGame
from aventura.data.dialogs import PAYADA
from aventura.scenes import game_scene as gs


def step(game, events=(), n=1):
    for e in events:
        pygame.event.post(e)
    for _ in range(n):
        game._handle_events()
        game._update()
        game._draw()


def scene(game):
    return type(game.current_scene).__name__


def click(pos):
    return pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1)


def settle(g, limit=2500):
    """Avanza frames hasta que Tano deje de caminar/hablar (saltando líneas con click)."""
    for _ in range(limit):
        s = g.current_scene
        if s.fsm == gs.IDLE or s.fsm == gs.DIALOGUE:
            return
        step(g, [click((450, 100))] if s.fsm == gs.SPEAKING else [])
    raise AssertionError("la escena no se estabilizó")


def verb(g, name):
    step(g, [click(g.current_scene.verb_rects[name].center)])


def on_hotspot(g, hid, v, item=None):
    """Elige verbo (+ ítem del inventario) y hace click real sobre el hotspot."""
    s = g.current_scene
    verb(g, v)
    if item:
        i = [it.name for it in s.inventory.items].index(item)
        step(g, [click(s.inventory._slot_rect(gs.INV_ORIGIN, i, gs.INV_SLOT, True).center)])
    h = next(h for h in s.hotspots if h.data["id"] == hid)
    assert s._visible(h), f"hotspot {hid} no visible"
    step(g, [click(h.rect.center)])
    settle(g)


def inv(g):
    return [i.name for i in g.current_scene.inventory.items]


def combine(g, a, b):
    s = g.current_scene
    verb(g, "Usar")
    for k in (a, b):
        i = inv(g).index(k)
        step(g, [click(s.inventory._slot_rect(gs.INV_ORIGIN, i, gs.INV_SLOT, True).center)])
    settle(g)


def choose(g, text_start):
    """Click real sobre la opción de diálogo cuyo texto empieza con `text_start`."""
    box = g.current_scene.box
    step(g)  # dibuja y calcula choice_rects
    for (label, _), rect in zip(box.current.choices, box.choice_rects):
        if label.startswith(text_start):
            step(g, [click(rect.center)])
            return
    raise AssertionError(f"no hay opción '{text_start}' en {[c[0] for c in box.current.choices]}")


def start_game(g):
    w = g.screen.get_width()
    step(g, [click((w // 2, 320))], n=3)  # botón "Comenzar Juego"
    assert scene(g) == "GameScene", scene(g)
    settle(g)


def go_to_tablado(g, con_mate_y_chori=True):
    """Resuelve los dos puzles y llega al Tablado."""
    assert g.state.room == "rambla"
    on_hotspot(g, "termo", "Agarrar")
    on_hotspot(g, "mate", "Agarrar")
    on_hotspot(g, "tacho", "Agarrar")
    assert {"termo", "mate", "diario"} <= set(inv(g)), inv(g)
    # Diálogo con opciones del pescador
    on_hotspot(g, "pescador", "Hablar")
    assert g.current_scene.fsm == gs.DIALOGUE
    choose(g, "Me robaron"); choose(g, "¿Y cómo"); choose(g, "Mate y chori")
    assert g.current_scene.fsm == gs.IDLE and g.current_scene.has_flag("pista_tablado")
    on_hotspot(g, "a_mercado", "Mirar")
    assert g.state.room == "mercado", g.state.room
    on_hotspot(g, "yerbas", "Agarrar")
    combine(g, "yerba", "mate")
    assert "mate_cargado" in inv(g) and "yerba" not in inv(g), inv(g)
    combine(g, "mate_cargado", "termo")
    assert "mate_listo" in inv(g), inv(g)
    on_hotspot(g, "parrillero", "Dar", "diario")
    assert "choripan" in inv(g) and "diario" not in inv(g), inv(g)
    on_hotspot(g, "a_tablado", "Mirar")
    assert g.state.room == "tablado"


def play_payada(g, errores):
    on_hotspot(g, "perro", "Dar", "choripan")
    assert g.current_scene.has_flag("perro_comido")
    on_hotspot(g, "contramaestre", "Dar", "mate_listo")
    assert g.current_scene.fsm == gs.DIALOGUE, g.current_scene.fsm
    choose(g, "Acepto")
    for i, (verso, opciones) in enumerate(PAYADA):
        ok = [t for t, es in opciones if es][0]
        mal = [t for t, es in opciones if not es][0]
        choose(g, mal if i < errores else ok)
        if g.state.lives <= 0:
            return
        if scene(g) == "GameScene" and g.current_scene.box.current.choices[0][0].startswith("(Seguir"):
            choose(g, "(Seguir)")
    if errores < 3:
        choose(g, "¡Gracias, maestro!")


def main():
    g = AventuraGame()
    step(g, n=2)
    assert scene(g) == "MenuScene", scene(g)

    # ---------- partida 1: victoria ----------
    start_game(g)
    go_to_tablado(g)
    play_payada(g, errores=0)
    settle(g)
    assert g.current_scene.has_flag("payada_ganada")
    on_hotspot(g, "bombo", "Agarrar")
    step(g, n=3)
    assert scene(g) == "VictoryScene", scene(g)
    w = g.screen.get_width()
    step(g, [click((w // 2, 400))], n=2)  # "Volver al menú"
    assert scene(g) == "MenuScene", scene(g)
    assert pygame.mouse.get_visible(), "el cursor del sistema quedó oculto"

    # ---------- partida 2: Game Over (3 errores) ----------
    start_game(g)
    assert g.state.lives == 3 and not g.state.flags and not inv(g)
    go_to_tablado(g)
    play_payada(g, errores=3)
    for _ in range(5):
        step(g)
        if scene(g) == "GameOverScene":
            break
        if g.current_scene.fsm == gs.DIALOGUE:
            choose(g, g.current_scene.box.current.choices[0][0])
    assert scene(g) == "GameOverScene", scene(g)
    step(g, [click((w // 2, 400))], n=2)
    assert scene(g) == "MenuScene", scene(g)

    # ---------- bloqueos ----------
    start_game(g)
    step(g, [click((10, 10))])  # click en el cielo: camina
    g.current_scene.walk_to((5, 5))
    for _ in range(300):
        step(g)
    assert g.current_scene.walk.contains(g.current_scene.pos), "Tano salió de la zona navegable"
    print("OK smoke test")
    pygame.quit()


if __name__ == "__main__":
    main()
