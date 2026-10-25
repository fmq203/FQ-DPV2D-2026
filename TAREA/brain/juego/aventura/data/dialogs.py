# aventura/data/dialogs.py
"""
Árboles de diálogo (DialogueNode del motor) con opciones múltiples.
Cada `build_*` recibe `ctx` (la GameScene) para condicionar opciones y aplicar efectos.
"""
from engine.dialogue import DialogueNode as N

# Payada: (verso del Contramaestre, [(opción, ¿es la correcta?)]).
PAYADA = [
    ("Con un mate y un chori se arregla cualquier problema,",
     [("y el bombo se lo robaron, pero eso es otro dilema", True),
      ("yo prefiero la milanesa con puré y ensalada", False),
      ("Nacional es lo mejor y Peñarol no vale nada", False)]),
    ("En Montevideo la rambla es larga como una canción,",
     [("tomo mate, tomo mate y después me voy a dormir", False),
      ("llueve fuerte en la Ciudad Vieja y se mojan los pies", False),
      ("y en el tablado el tambor late como un corazón", True)]),
    ("Si querés cantar con nosotros tenés que tener humildad,",
     [("y comer mucho chori para tener buena voz", False),
      ("porque en la murga el que canta lo hace con verdad", True),
      ("porque el Carnaval es largo y la noche no se acaba", False)]),
    ("El bombo es el alma de la murga, no lo podés robar,",
     [("devolvelo al tablado que lo vamos a hacer retumbar", True),
      ("yo me voy para mi casa porque ya me quiero ir", False),
      ("el candombe es patrimonio de la humanidad entera", False)]),
]


OK_FRASES = ["¡Chupate esa mandarina! Rima y alma. ¡Seguí!", "¡Cortita y al pie, así se canta!",
             "¡Eso es! Rima y alma. ¡Seguí!", "¡Uruguay nomá! ¡Qué verso!"]
MAL_FRASES = ["¡Esa rima no tiene goyete!", "¡Andá a cantarle a Gardel!",
              "¡Esa rima está descuajeringada!", "¡Eso es un desastre!"]


def build(name, ctx):
    return _BUILDERS[name](ctx)


def _pescador(ctx):
    return {
        "start": N("¡Cayó piedra sin llover! ¿Qué hacés, botija? Cara de haber perdido algo.", "Pescador",
                   [("Me robaron el bombo de la murga.", "bombo"),
                    ("¿Siempre llueve así por acá?", "clima"),
                    ("Nada, solo miro el río.", None)]),
        "clima": N("¡Es El Niño, botija! Desde que arrancó la primavera está todo húmedo y lluvioso. "
                   "Hasta los peces andan con paraguas.", "Pescador",
                   [("¿Y va a parar la lluvia?", "para"), ("Y el Carnaval, ¿lo van a mojar?", "carnaval"),
                    ("¿Y la ropa, se seca?", "ropa"), ("Qué lástima.", "start")]),
        "ropa": N("¿Secarse? Mi señora tiene una sábana colgada desde setiembre. "
                  "Ya la usamos de paraguas.", "Pescador", [("Qué desastre.", "start")]),
        "para": N("¿Que pare? Difícil que el chancho chifle. Pero matemáticamente tenemos chance.",
                  "Pescador", [("Ojalá.", "start")]),
        "carnaval": N("Seguro. Pero el uruguayo canta bajo la lluvia, tira el paraguas y sigue.", "Pescador",
                      [("Tiene razón.", "start")]),
        "bombo": N("Ah, vi unos tipos con un bombo rumbo al Museo del Carnaval, pasando el Mercado.",
                   "Pescador", [("¿Y cómo hago para recuperarlo?", "quien"),
                                ("¿Cómo llego?", "ruta")]),
        "ruta": N("Seguí la rambla hasta el Mercado del Puerto y después al Museo del Carnaval.", "Pescador",
                  [("Gracias, voy para allá.", None)]),
        "quien": N("Lo cuida un tal Contramaestre. Solo habla con quien comparte un mate... "
                   "y hay un perro hambriento que no deja pasar a nadie.", "Pescador",
                   [("Mate y chori. Anotado.", None)],
                   action=lambda n: ctx.flag("pista_tablado")),
    }


def _parrillero(ctx):
    inv = ctx.inventory
    start_choices = [("¿Un chori al pan? ¿Cuánto sale?", "precio"),
                     ("¿Y de dónde saco un diario?", "pista")]
    if inv.has("diario") and not ctx.has_flag("parrilla_prendida"):
        start_choices.insert(0, ("Tengo este diario, ¿sirve?", "entrega"))
    start_choices.append(("Chau.", None))
    if ctx.has_flag("parrilla_prendida"):
        return {"start": N("Ya te di tu chori, flaco. A caballo regalado no se le miran los dientes, pero comelo que se enfría.", "Parrillero",
                           [("Gracias, maestro.", None)])}
    return {
        "start": N("Buenas. Si querés chori, el fuego está apagado y sin papel no prende.",
                   "Parrillero", start_choices),
        "precio": N("Para vos es gratis si me ayudás a prender la parrilla. Con papel, ¿eh? Papel.",
                    "Parrillero", [("Entendido.", "start")]),
        "pista": N("Buscá por la rambla. En los tachos siempre hay diarios de ayer.",
                   "Parrillero", [("Gracias.", "start")]),
        "entrega": N("¡Papel! Con esto prendo el fuego. Tomá, tu chori al pan bien doradito.", "Parrillero",
                     [("¡Gracias!", None)],
                     action=lambda n: ctx.trade("diario", "choripan", "parrilla_prendida")),
    }


def _contramaestre(ctx):
    return {
        "start": N("¿Y vos quién sos? No hablo con extraños sin mate.", "Contramaestre",
                   [("Vengo por el bombo de la murga.", "bombo"), ("Chau.", None)]),
        "bombo": N("Primero un mate. Después hablamos. Al pan pan y al vino vino.", "Contramaestre",
                   [("Ya vuelvo con uno.", None)]),
    }


def _payada_intro(ctx):
    nodes = {
        "start": N("Para tener el bombo tenés que ganarlo: una payada. ¡Agarrate Catalina! Tres errores y te vas.",
                   "Contramaestre", [("Acepto el desafío.", "r0"), ("Mejor otro día.", None)]),
    }
    n = len(PAYADA)
    for i, (verso, opciones) in enumerate(PAYADA):
        choices = []
        for j, (texto, ok) in enumerate(opciones):
            choices.append((texto, f"r{i}_{'ok' if ok else 'mal'}"))
        nodes[f"r{i}"] = N(verso, "Contramaestre", choices)
        nxt = f"r{i + 1}" if i + 1 < n else "gana"
        nodes[f"r{i}_ok"] = N(OK_FRASES[i % len(OK_FRASES)], "Contramaestre", [("(Seguir)", nxt)],
                              action=lambda nd: ctx.play("combine"))

        def mal(nd, nxt=nxt, i=i):
            ctx.state.lives -= 1
            ctx.play("nope")
            if ctx.state.lives <= 0:
                nd.text = "¡Vayan pelando las chauchas! Se acabó, pibe: ¡afuera del tablado!"
                nd.choices = [("(...)", "pierde")]
            else:
                nd.text = f"{MAL_FRASES[i % len(MAL_FRASES)]} Te quedan {ctx.state.lives} errores."
                nd.choices = [("(Seguir)", nxt)]
        nodes[f"r{i}_mal"] = N("", "Contramaestre", [], action=mal)
    nodes["pierde"] = N("(El Contramaestre te saca a patadas del tablado.)", "Narrador", [("...", None)],
                        action=lambda nd: ctx.finish_after("game_over"))
    nodes["gana"] = N("¡Qué payada, botija! ¡Uruguay nomá! Te ganaste el respeto del Sur. El bombo es tuyo, está ahí atrás.",
                      "Contramaestre", [("¡Gracias, maestro!", None)],
                      action=lambda nd: ctx.flag("payada_ganada"))
    return nodes


_BUILDERS = {
    "pescador": _pescador,
    "parrillero": _parrillero,
    "contramaestre": _contramaestre,
    "payada_intro": _payada_intro,
}
