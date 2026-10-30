---
title: Escenarios, hotspots y puzles
type: diseno
sources: [juego/aventura/data/rooms.py, juego/aventura/data/dialogs.py, juego/aventura/data/items.py]
updated: 2026-10-30
---

# Escenarios, hotspots y puzles — "El Murguista" (Montevideo)

**Premisa:** faltan 2 días para el Carnaval; robaron el bombo de la murga "Los Sin Tablado". **Tano**, aspirante a murguista, debe recuperarlo (tono cómico, referencias uruguayas: mate, termo, chori al pan, clima de El Niño (ropa que no se seca), candombe, payada).

## Escenarios (datos en `juego/aventura/data/rooms.py`)
Rambla de Barrio Sur ⇄ Mercado del Puerto ⇄ Museo del Carnaval (con su tablado). Cada uno con zona navegable (ver [[walkmask]], [[mascara-caminabilidad]]) y hotspots definidos como datos (rect, punto donde Tano se para, respuestas por verbo, banderas `show_if`/`hide_if`/`needs`). Salidas = hotspots con `exit`. Ver [[hotspot]].

## Puzles
1. **Mate (combinación en 2 pasos):** termo + mate (Rambla) + yerba (Mercado): `yerba + mate → mate cargado`, `mate cargado + termo → mate listo`. Ver [[inventario-y-combinacion]].
2. **Chori al pan — mini-reto de la parrilla** (sugerencia del docente: "hacer el chori en la parrilla de la pantalla 2"):
   - *Usar* termo con el gato, que duerme sobre la leña y odia el agua; sale corriendo (salida animada con `leave`) y así se puede *Agarrar* la leña.
   - diario + leña = fuego armado.
   - *Usar* el fuego con la parrilla: el asador pone el fósforo y da chorizo + pan.
   - *Usar* el chorizo con la parrilla arranca el temporizador `chorizo` (`TIMERS` en `rooms.py`): a punto a los 8 s, quemado a los 18 s.
   - *Agarrar* a tiempo da el chorizo asado; si está quemado, el asador da otro.
   - chorizo asado + pan = chori al pan → *Dar* al perro del Museo, que libera el paso.

   El termo **se conserva** al cebar el mate (3.er elemento de la receta), para que no haya callejón sin salida.
3. **Payada (duelo, diálogo con opciones):** *Dar* el mate al Contramaestre. 4 versos, 3 opciones cada uno (una rima bien); **3 errores = Game Over**, con botón **Reintentar payada** (vuelve al punto de control guardado al aceptar el duelo). Ganar → aparece el bombo → *Agarrar* → **Victoria**. Ver [[sistema-dialogos]].

Diálogos con opciones múltiples: Pescador (pista), Asador (diario / chori al pan), Contramaestre, payada. Guion/humor ajustable en `data/dialogs.py`. Ver [[fsm-verbos]].

## Dichos y frases populares
Incorporados con su significado correcto (fuentes: bodegagarzon.com/es/blog/dichos-uruguayos y descubreuruguay.com/cultura-uruguaya/frases-uruguayas): "Cayó piedra sin llover" (Pescador), "Matemáticamente tenemos chance" (Cielo, Pescador), "Difícil que el chancho chifle", "El día del golero", "Es lo que hay, valor", "En boca cerrada no entran moscas", "Curado de espanto" (Gato), "Atadito con alambre" (Tendedero, Asador), "A caballo regalado no se le miran los dientes" (Asador), "Como perro en bote" (Perro), "Abrí los ganchos", "Al pan pan y al vino vino" y "Agarrate Catalina" (Contramaestre), y en la payada "Chupate esa mandarina", "Cortita y al pie", "¡Uruguay nomá!", "No tiene goyete", "Andá a cantarle a Gardel", "Descuajeringado" y "Vayan pelando las chauchas". Frases genéricas por verbo en `DEFAULTS` de `game_scene.py`; frases de la payada en `OK_FRASES`/`MAL_FRASES` de `data/dialogs.py`.
