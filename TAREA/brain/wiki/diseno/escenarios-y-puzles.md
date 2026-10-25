---
title: Escenarios, hotspots y puzles
type: diseno
sources: [juego/aventura/data/rooms.py, juego/aventura/data/dialogs.py, juego/aventura/data/items.py]
updated: 2026-10-25
---

# Escenarios, hotspots y puzles — "El Murguista" (Montevideo)

**Premisa:** faltan 2 días para el Carnaval; robaron el bombo de la murga "Los Sin Tablado". **Tano**, aspirante a murguista, debe recuperarlo (tono cómico, referencias uruguayas: mate, termo, chori al pan, clima de El Niño (ropa que no se seca), candombe, payada).

## Escenarios (datos en `juego/aventura/data/rooms.py`)
Rambla de Pocitos ⇄ Mercado del Puerto ⇄ Tablado de Barrio Sur. Cada uno con zona navegable (ver [[walkmask]], [[mascara-caminabilidad]]) y hotspots definidos como datos (rect, punto donde Tano se para, respuestas por verbo, banderas `show_if`/`hide_if`/`needs`). Salidas = hotspots con `exit`. Ver [[hotspot]].

## Puzles
1. **Mate (combinación en 2 pasos):** termo + mate (Rambla) + yerba (Mercado): `yerba + mate → mate cargado`, `mate cargado + termo → mate listo`. Ver [[inventario-y-combinacion]].
2. **Chori al pan:** diario (tacho de la Rambla) → *Dar* al parrillero (o por diálogo) → chori al pan → *Dar* al perro del Tablado, que libera el paso.
3. **Payada (duelo, diálogo con opciones):** *Dar* el mate al Contramaestre. 4 versos, 3 opciones cada uno (una rima bien); **3 errores = Game Over**. Ganar → aparece el bombo → *Agarrar* → **Victoria**. Ver [[sistema-dialogos]].

Diálogos con opciones múltiples: Pescador (pista), Parrillero (diario / chori al pan), Contramaestre, payada. Guion/humor ajustable en `data/dialogs.py`. Ver [[fsm-verbos]].

## Dichos y frases populares
Incorporados con su significado correcto (fuentes: bodegagarzon.com/es/blog/dichos-uruguayos y descubreuruguay.com/cultura-uruguaya/frases-uruguayas): "Cayó piedra sin llover" (Pescador), "Matemáticamente tenemos chance" (Cielo, Pescador), "Difícil que el chancho chifle", "El día del golero", "Es lo que hay, valor", "En boca cerrada no entran moscas", "Curado de espanto" (Gato), "Atadito con alambre" (Tendedero, Parrillero), "A caballo regalado no se le miran los dientes" (Parrillero), "Como perro en bote" (Perro), "Abrí los ganchos", "Al pan pan y al vino vino" y "Agarrate Catalina" (Contramaestre), y en la payada "Chupate esa mandarina", "Cortita y al pie", "¡Uruguay nomá!", "No tiene goyete", "Andá a cantarle a Gardel", "Descuajeringado" y "Vayan pelando las chauchas". Frases genéricas por verbo en `DEFAULTS` de `game_scene.py`; frases de la payada en `OK_FRASES`/`MAL_FRASES` de `data/dialogs.py`.
