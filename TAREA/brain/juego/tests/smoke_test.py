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


def go_to_tablado(g, quemar=False):
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
    assert g.music_track == "mercado", g.music_track  # cada lugar con su tema
    on_hotspot(g, "yerbas", "Agarrar")
    combine(g, "yerba", "mate")
    assert "mate_cargado" in inv(g) and "yerba" not in inv(g), inv(g)
    combine(g, "mate_cargado", "termo")
    assert "mate_listo" in inv(g), inv(g)
    hacer_chori(g, quemar=quemar)
    on_hotspot(g, "a_tablado", "Mirar")
    assert g.state.room == "tablado" and g.music_track == "tablado"


def esperar_flag(g, flag, limit=1500):
    for _ in range(limit):
        if g.current_scene.has_flag(flag):
            settle(g)  # Tano avisa en voz alta ("¡Huele a gloria!")
            return
        step(g)
    raise AssertionError(f"nunca se activó {flag}")


def esperar_ida(g, hid, limit=600):
    """El gato/perro se va caminando (se dibuja corrido) hasta salir de la pantalla."""
    s = g.current_scene
    for _ in range(limit):
        if hid in s.state.gone:
            assert hid not in s.leaving
            return
        if hid in s.leaving:
            assert s.leaving[hid] != 0  # se está moviendo
        step(g)
    raise AssertionError(f"{hid} nunca terminó de irse")


def hacer_chori(g, quemar=False):
    """Mini-reto del Mercado: espantar al gato, armar el fuego y asar el chorizo a tiempo."""
    s = g.current_scene
    on_hotspot(g, "lena", "Agarrar")
    assert "lena" not in inv(g), "la leña no se puede agarrar con el gato encima"
    on_hotspot(g, "asador", "Dar", "diario")
    assert "diario" in inv(g), "el papel solo no alcanza"
    on_hotspot(g, "gato", "Usar", "termo")
    assert s.has_flag("gato_mojado") and "termo" in inv(g)
    esperar_ida(g, "gato")
    on_hotspot(g, "lena", "Agarrar")
    combine(g, "diario", "lena")
    assert "lena_papel" in inv(g), inv(g)
    on_hotspot(g, "parrilla", "Usar", "lena_papel")
    assert s.has_flag("parrilla_prendida") and {"chorizo", "pan"} <= set(inv(g)), inv(g)
    on_hotspot(g, "parrilla", "Usar", "chorizo")
    assert s.has_flag("chorizo_en_parrilla") and "chorizo" not in inv(g)
    on_hotspot(g, "parrilla", "Agarrar")  # demasiado pronto: sigue crudo
    assert "chorizo_asado" not in inv(g) and s.has_flag("chorizo_en_parrilla")
    if quemar:
        esperar_flag(g, "chorizo_quemado")
        on_hotspot(g, "parrilla", "Agarrar")  # carbón: el asador da otro chorizo
        assert "chorizo" in inv(g) and not s.has_flag("chorizo_en_parrilla"), inv(g)
        on_hotspot(g, "parrilla", "Usar", "chorizo")
    esperar_flag(g, "chorizo_a_punto")
    assert s._sprite_id(next(h for h in s.hotspots if h.data["id"] == "parrilla")) == "parrilla_chorizo_a_punto"
    on_hotspot(g, "parrilla", "Agarrar")
    assert "chorizo_asado" in inv(g) and not s.state.timers, (inv(g), s.state.timers)
    combine(g, "chorizo_asado", "pan")
    assert "choripan" in inv(g) and "pan" not in inv(g), inv(g)


def play_payada(g, errores):
    on_hotspot(g, "perro", "Dar", "choripan")
    assert g.current_scene.has_flag("perro_comido")
    esperar_ida(g, "perro")
    on_hotspot(g, "contramaestre", "Dar", "mate_listo")
    assert g.current_scene.fsm == gs.DIALOGUE, g.current_scene.fsm
    cantar(g, errores)


def cantar(g, errores):
    """Desde el nodo de inicio de la payada: acepta y canta con `errores` respuestas malas."""
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
    assert g.music_track == "menu"
    w = g.screen.get_width()

    # ---------- créditos ----------
    step(g, [click((w // 2, 398))], n=2)
    assert scene(g) == "CreditsScene", scene(g)
    step(g, [click((w // 2, 555))], n=2)
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

    # ---------- partida 2: Game Over (3 errores) -> Reintentar payada -> victoria ----------
    start_game(g)
    assert g.state.lives == 3 and not g.state.flags and not inv(g)
    assert g.checkpoint is None
    on_hotspot(g, "tacho", "Agarrar")
    assert g.current_scene._sprite_id(next(h for h in g.current_scene.hotspots
                                           if h.data["id"] == "tacho")) == "tacho_vacio"
    go_to_tablado(g, quemar=True)
    play_payada(g, errores=3)
    for _ in range(5):
        step(g)
        if scene(g) == "GameOverScene":
            break
        if g.current_scene.fsm == gs.DIALOGUE:
            choose(g, g.current_scene.box.current.choices[0][0])
    assert scene(g) == "GameOverScene", scene(g)
    step(g, [click((w // 2, 408))], n=2)  # "Reintentar payada"
    assert scene(g) == "GameScene", scene(g)
    s = g.current_scene
    assert s.fsm == gs.DIALOGUE and g.state.room == "tablado" and g.state.lives == 3
    assert s.has_flag("perro_comido") and s.has_flag("mate_dado")
    cantar(g, errores=1)
    settle(g)
    on_hotspot(g, "bombo", "Agarrar")
    step(g, n=3)
    assert scene(g) == "VictoryScene", scene(g)
    step(g, [click((w // 2, 400))], n=2)
    assert scene(g) == "MenuScene", scene(g)

    # ---------- Game Over -> Volver al menú (botón de abajo) ----------
    g.save_checkpoint()
    g.change_scene("game_over")
    step(g, n=2)
    step(g, [click((w // 2, 478))], n=2)
    assert scene(g) == "MenuScene", scene(g)

    # ---------- pausa con ESC ----------
    start_game(g)
    esc = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    step(g, [esc])
    s = g.current_scene
    assert s.paused
    pos = s.pos
    step(g, [click((450, 420))], n=30)  # click "debajo" de la pausa: no camina
    assert s.pos == pos
    musica = g.music_on
    step(g, [click(s.pause_buttons[1].rect.center)])
    assert g.music_on != musica
    step(g, [click(s.pause_buttons[0].rect.center)])  # Continuar
    assert not s.paused
    step(g, [esc])
    step(g, [click(s.pause_buttons[2].rect.center)], n=2)  # Volver al menú
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
