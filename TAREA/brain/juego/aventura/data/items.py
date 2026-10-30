# aventura/data/items.py
"""Ítems del inventario y recetas de combinación."""
ITEMS = {
    "termo":        ("Termo",         "Un termo con agua caliente. Casi un órgano vital en Uruguay."),
    "mate":         ("Mate",          "Un mate vacío. Una tristeza nacional."),
    "yerba":        ("Yerba",         "Un paquete de yerba. Verde esperanza."),
    "mate_cargado": ("Mate cargado",  "Mate con yerba, pero sin agua. Seco como discurso de campaña."),
    "mate_listo":   ("Mate listo",    "¡Un mate cebado, calentito y espumoso! Irresistible."),
    "diario":       ("Diario",        "El diario de ayer. Titular: 'Primavera, día 40 de lluvia: culpan a El Niño'."),
    "lena":         ("Leña",          "Unos troncos secos. Lo único seco en todo Montevideo."),
    "lena_papel":   ("Fogata armada", "Leña con papel abajo. Solo falta el fósforo... y una parrilla."),
    "chorizo":      ("Chorizo",       "Un chorizo crudo. Todavía no es un chori: es una promesa."),
    "pan":          ("Pan",           "Un pan flauta crujiente, esperando a su chorizo."),
    "chorizo_asado": ("Chorizo asado", "Dorado por fuera, jugoso por dentro. Le falta el pan."),
    "choripan":     ("Chori al pan",  "Un chori al pan recién salido de la parrilla. Huele a gloria."),
}

# {frozenset({a, b}): (resultado, mensaje[, ítems que se conservan])}.
# Puzle del mate (2 pasos) y del chori (fuego + armado). El termo no se gasta al cebar: también sirve con el gato.
RECIPES = {
    frozenset(("yerba", "mate")): ("mate_cargado", "Cargás el mate con yerba. Falta el agua."),
    frozenset(("mate_cargado", "termo")): ("mate_listo", "¡Cebás un mate perfecto, con espuma y todo! (El termo me lo quedo.)",
                                           ("termo",)),
    frozenset(("diario", "lena")): ("lena_papel", "Papel abajo, leña arriba: fogata armada. Ahora, a la parrilla."),
    frozenset(("chorizo_asado", "pan")): ("choripan", "¡Chorizo en el pan: chori al pan como Dios manda!"),
}
