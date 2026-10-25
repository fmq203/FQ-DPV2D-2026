# aventura/data/items.py
"""Ítems del inventario y recetas de combinación."""
ITEMS = {
    "termo":        ("Termo",         "Un termo con agua caliente. Casi un órgano vital en Uruguay."),
    "mate":         ("Mate",          "Un mate vacío. Una tristeza nacional."),
    "yerba":        ("Yerba",         "Un paquete de yerba. Verde esperanza."),
    "mate_cargado": ("Mate cargado",  "Mate con yerba, pero sin agua. Seco como discurso de campaña."),
    "mate_listo":   ("Mate listo",    "¡Un mate cebado, calentito y espumoso! Irresistible."),
    "diario":       ("Diario",        "El diario de ayer. Titular: 'Primavera, día 40 de lluvia: culpan a El Niño'."),
    "choripan":     ("Chori al pan",  "Un chori al pan recién salido de la parrilla. Huele a gloria."),
}

# {frozenset({a, b}): (resultado, mensaje)}. Combinación en dos pasos (puzle 1).
RECIPES = {
    frozenset(("yerba", "mate")): ("mate_cargado", "Cargás el mate con yerba. Falta el agua."),
    frozenset(("mate_cargado", "termo")): ("mate_listo", "¡Cebás un mate perfecto, con espuma y todo!"),
}
