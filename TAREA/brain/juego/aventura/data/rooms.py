# aventura/data/rooms.py
"""
Escenarios, zonas navegables y hotspots definidos como DATOS.

Hotspot:
  id, name, rect, stand=(x, y) donde Tano se para, art=(tipo, color)
  show_if / hide_if : flag que lo muestra / oculta
  needs, blocked    : flag requerido para interactuar y mensaje si falta
  exit              : (cuarto, x_de_aparición) -> hotspot de salida
  acts              : tabla (verbo | "Verbo:item") -> resultado
Resultado: str (Tano lo dice) o dict con
  say (str|list|(hablante, texto)), give, take, flag, talk, end ("victory"),
  sound, y if_flag/if_item + "else" para resultados condicionales.
"""

TANO = (255, 220, 60)  # color del texto de Tano

ROOMS = {
    # ------------------------------------------------------------------ #
    "rambla": {
        "title": "Rambla de Barrio Sur",
        "walk": [(60, 295, 335, 35), (0, 330, 440, 40), (0, 370, 495, 40), (0, 410, 545, 40)],  # la vereda en perspectiva
        "start": (200, 390),
        "hotspots": [
            {"id": "cielo", "name": "Cielo", "rect": (0, 0, 900, 150),
             "stand": (450, 345), "art": ("zone", None),
             "acts": {
                 "Mirar": "Nubes grises, otra vez. Dicen que es primavera... pero con El Niño ya perdí la cuenta de los días de humedad. Matemáticamente tenemos chance de que salga el sol.",
                 "Hablar": "Le pido al cielo que pare. Me responde con una garúa.",
                 "Agarrar": "Quiero agarrar un poco de sol. Sí, ese día va a llegar el día del golero.",
             }},
            {"id": "rio", "name": "Río de la Plata", "rect": (560, 215, 340, 115),
             "stand": (480, 395), "art": ("zone", None),
             "acts": {
                 "Mirar": "El Río de la Plata: ancho como mar y marrón como dulce de leche.",
                 "Hablar": "Le hablo al río. Me devuelve una ola de mal gusto.",
                 "Agarrar": "No me lo cabe en el bolsillo.",
             }},
            {"id": "banco", "name": "Banco", "rect": (40, 330, 170, 70),
             "stand": (125, 420), "art": ("bench", (150, 100, 60)),
             "acts": {
                 "Mirar": "Un banco de la rambla. Testigo de mil mates y dos mil chismes.",
                 "Usar": "Me siento un segundo... no, no hay tiempo: el Carnaval no espera.",
             }},
            {"id": "termo", "name": "Termo", "rect": (80, 303, 34, 50),
             "stand": (125, 420), "art": ("item", "termo"), "hide_if": "termo_cogido",
             "acts": {
                 "Mirar": "Un termo con agua caliente. Alguien lo dejó... ¿un uruguayo olvidando el termo?",
                 "Agarrar": {"give": "termo", "flag": "termo_cogido",
                           "say": "Me llevo el termo. Es por una buena causa."},
             }},
            {"id": "mate", "name": "Mate", "rect": (430, 268, 36, 36),
             "stand": (420, 355), "art": ("item", "mate"), "hide_if": "mate_cogido",
             "acts": {
                 "Mirar": "Un mate abandonado sobre el muro. Vacío, claro.",
                 "Agarrar": {"give": "mate", "flag": "mate_cogido",
                           "say": "Un mate vacío. Es lo que hay, valor. Ahora a conseguir con qué llenarlo."},
             }},
            {"id": "tacho", "name": "Tacho de basura", "rect": (390, 340, 56, 80),
             "stand": (440, 435), "art": ("bin", (95, 110, 95)),
             "acts": {
                 "Mirar": "Un tacho de basura. Asoma un diario viejo.",
                 "Agarrar": {"give": "diario", "flag": "diario_cogido",
                           "if_flag_not": "diario_cogido",
                           "say": "Rescato el diario de ayer. Titular: 'Primavera, día 40 de lluvia: culpan a El Niño'.",
                           "else": "Ya me llevé el único diario que había."},
                 "Usar": {"give": "diario", "flag": "diario_cogido",
                          "if_flag_not": "diario_cogido",
                          "say": "Rescato el diario de ayer. Titular: 'Primavera, día 40 de lluvia: culpan a El Niño'.",
                          "else": "Ya me llevé el único diario que había."},
             }},
            {"id": "pescador", "name": "Pescador", "rect": (250, 310, 66, 112),
             "stand": (290, 436), "art": ("person", (70, 110, 90)),
             "acts": {
                 "Mirar": "Un pescador. Lleva ahí desde el Mundial del 50.",
                 "Hablar": {"talk": "pescador"},
                 "Agarrar": "No creo que le guste.",
             }},
            {"id": "a_mercado", "name": "Mercado del Puerto", "rect": (260, 235, 120, 60),
             "stand": (330, 305), "exit": ("mercado", 230), "art": ("zone", None),
             "acts": {"Mirar": "Hacia Ciudad Vieja y el Mercado del Puerto."}},
        ],
    },
    # ------------------------------------------------------------------ #
    "mercado": {
        "title": "Mercado del Puerto",
        "walk": [(400, 315, 140, 30), (395, 345, 200, 40), (380, 385, 260, 30), (200, 415, 520, 35)],  # pasillo de piedra
        "start": (230, 430),
        "hotspots": [
            {"id": "yerbas", "name": "Puesto de yerba", "rect": (100, 260, 120, 80),
             "stand": (240, 432), "art": ("zone", None),
             "acts": {
                 "Mirar": "Un puesto con paquetes de yerba hasta el techo. Hay para toda la nación. Algo húmeda: culpa de El Niño.",
                 "Hablar": "El vendedor está dormido, con la boca abierta. En boca cerrada no entran moscas, pero a él sí.",
                 "Agarrar": {"give": "yerba", "flag": "yerba_cogida", "if_flag_not": "yerba_cogida",
                           "say": "Tomo un paquete de yerba. Dejo unos pesos en el mostrador.",
                           "else": "Con un paquete alcanza. No soy un acaparador."},
             }},
            {"id": "parrilla", "name": "Parrilla", "rect": (380, 225, 160, 70),
             "stand": (460, 420), "art": ("zone", None),
             "acts": {
                 "Mirar": {"if_flag": "parrilla_prendida",
                           "say": "La parrilla chisporrotea. Huele a gloria.",
                           "else": "La parrilla está fría. Sin fuego no hay chori."},
                 "Usar": "No me dejan tocar la parrilla. Es sagrada.",
             }},
            {"id": "parrillero", "name": "Parrillero", "rect": (520, 300, 60, 95),
             "stand": (540, 420), "art": ("person", (240, 240, 235)),
             "acts": {
                 "Mirar": "El parrillero, con delantal de campeón y cara de pocos amigos.",
                 "Hablar": {"talk": "parrillero"},
                 "Dar:diario": {"take": "diario", "give": "choripan", "flag": "parrilla_prendida",
                                "sound": "combine",
                                "say": [("Parrillero", "¡Papel! Esto lo atamos con alambre y prende. Tomá un chori al pan, botija."),
                                        ("Tano", "¡Chori al pan conseguido!")]},
                 "Usar:diario": "Para dárselo uso 'Dar', no 'Usar'. Soy educado.",
                 "Dar:choripan": "¿Me devolvés mi propio chori? Qué gracioso.",
                 "Agarrar": "Tocarle el delantal al parrillero es mala idea.",
             }},
            {"id": "tendedero", "name": "Tendedero", "rect": (760, 70, 130, 120),
             "stand": (690, 432), "art": ("zone", None),
             "acts": {
                 "Mirar": "Ropa colgada desde que empezó la primavera, todo atadito con alambre. Sigue mojada. Una media ya echó raíces.",
                 "Agarrar": "Agarro una remera: está más mojada que antes de colgarla.",
                 "Usar": "Intento secar algo. El Niño se ríe de mí.",
                 "Hablar": "Le hablo a la ropa. Gotea con indiferencia.",
             }},
            {"id": "gato", "name": "Gato", "rect": (545, 385, 65, 40),
             "stand": (600, 442), "art": ("cat", (200, 130, 60)),
             "acts": {
                 "Mirar": "Un gato del Mercado, curado de espanto. Se cree el dueño de la parrilla.",
                 "Hablar": "Miau. (Traducción: 'pagame la entrada'.)",
                 "Agarrar": "Me mira con desprecio felino. Mejor no.",
             }},
            {"id": "a_rambla", "name": "Rambla de Barrio Sur", "rect": (0, 380, 120, 70),
             "stand": (205, 438), "exit": ("rambla", 330), "art": ("zone", None),
             "acts": {"Mirar": "De vuelta hacia la rambla."}},
            {"id": "a_tablado", "name": "Museo del Carnaval", "rect": (780, 380, 120, 70),
             "stand": (700, 438), "exit": ("tablado", 70), "art": ("zone", None),
             "acts": {"Mirar": "Hacia el Museo del Carnaval, donde está el tablado."}},
        ],
    },
    # ------------------------------------------------------------------ #
    "tablado": {
        "title": "Museo del Carnaval",
        "walk": [(0, 385, 900, 65), (20, 300, 170, 85), (720, 300, 160, 85)],  # franja delante del público + las dos calles
        "start": (70, 395),
        "hotspots": [
            {"id": "cartel", "name": "Cartel de la murga", "rect": (370, 150, 160, 60),
             "stand": (450, 425), "art": ("zone", None),
             "acts": {
                 "Mirar": "'CARNAVAL - TABLADO'. Abajo, con letra chica: 'Los Sin Tablado: ahora con tablado... si aparece el bombo.' Es lo que hay, valor. (Pegado con cinta: llueve desde que empezó la primavera.)",
                 "Agarrar": "Está bien pegado. Los carteles uruguayos no se despegan.",
             }},
            {"id": "perro", "name": "Perro", "rect": (230, 390, 100, 55),
             "stand": (170, 440), "art": ("dog", (120, 90, 60)), "hide_if": "perro_comido",
             "acts": {
                 "Mirar": "Un perro enorme con cara de pocos amigos. Gruñe como un bajo de murga.",
                 "Hablar": "¡Guau! (Traducción: 'chori, ya'.)",
                 "Agarrar": "Mejor no: tiene todos los dientes. Me quedo como perro en bote.",
                 "Usar": "Intento acariciarlo. Casi pierdo la mano.",
                 "Dar:choripan": {"take": "choripan", "flag": "perro_comido", "sound": "combine",
                                 "say": "El perro devora el chori y se va a dormir la siesta. ¡Camino libre!"},
                 "Dar:mate_listo": "El perro no toma mate. Es un perro de cerveza.",
             }},
            {"id": "contramaestre", "name": "Contramaestre", "rect": (600, 200, 55, 92),
             "stand": (610, 425), "art": ("person", (40, 90, 150)),
             "needs": "perro_comido", "blocked": "El perro no me deja acercarme. Abrí los ganchos, Tano: tiene hambre y mal humor.",
             "acts": {
                 "Mirar": "El Contramaestre: guardián del tablado, con un bigote que impone respeto.",
                 "Hablar": {"if_flag": "payada_ganada",
                            "say": [("Contramaestre", "Ya te di el bombo. Llevátelo y no me hagas cantar más.")],
                            "else": {"if_flag": "mate_dado", "talk": "payada_intro",
                                     "else": {"talk": "contramaestre"}}},
                 "Dar:mate_listo": {"take": "mate_listo", "flag": "mate_dado", "sound": "combine",
                                    "say": [("Contramaestre", "¡Un mate cebado como Dios manda!"),
                                            ("Contramaestre", "Bueno, te escucho. ¿Venís por el bombo?")],
                                    "talk": "payada_intro"},
                 "Agarrar": "Tocar al Contramaestre es una payada que no quiero cantar.",
             }},
            {"id": "bombo", "name": "Bombo", "rect": (545, 238, 55, 50),
             "stand": (560, 425), "art": ("drum", (190, 30, 40)), "show_if": "payada_ganada",
             "acts": {
                 "Mirar": "¡El bombo de la murga! Rojo, con su correa y un solo parche... pero de gloria.",
                 "Usar": "Me lo cuelgo de la correa y lo toco con el mazo. ¡Qué sonido!",
                 "Agarrar": {"end": "victory", "sound": "bombo",
                           "say": "¡Recuperé el bombo! ¡Que empiece el Carnaval!"},
             }},
            {"id": "a_mercado", "name": "Mercado del Puerto", "rect": (0, 300, 45, 150),
             "stand": (45, 420), "exit": ("mercado", 690), "art": ("zone", None),
             "acts": {"Mirar": "De vuelta hacia el Mercado."}},
        ],
    },
}
