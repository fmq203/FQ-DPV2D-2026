# El Murguista — Documento de diseño

**Videojuegos 2D · Tecnólogo en Informática · 2026** · Opción 1: Aventura gráfica (point-and-click estilo *The Secret of Monkey Island*)
Python 3.12 + Pygame 2.6, sobre el motor del curso.

---

## 1. Concepto

Faltan dos días para el Carnaval y robaron el **bombo** de la murga *Los Sin Tablado*. **Tano**, aspirante a murguista, recorre Montevideo para recuperarlo antes de la prueba de admisión. Tiene que juntar objetos, combinarlos, convencer a los personajes y ganar un **duelo de payada**.

- **Tono:** comedia costumbrista uruguaya: mate, chori al pan, la lluvia de El Niño, ropa que no se seca y dichos populares usados con su significado real.
- **Duración:** de 10 a 15 minutos en la primera partida.
- **Objetivo de diseño:** cubrir todos los mínimos de la Opción 1 con un prototipo vertical corto y completo, en el que cada mecánica (verbos, inventario, combinación, diálogo, puzle) aparezca al menos una vez de forma necesaria para avanzar.

## 2. Mecánicas

### 2.1 Verbos e interacción (máquina de estados)
Cinco verbos: **Mirar, Agarrar, Usar, Hablar y Dar**. Se usa *Agarrar* y no *Coger* porque en Uruguay *coger* es vulgar. El jugador elige un verbo y después un objetivo. Si el verbo es *Usar* o *Dar*, primero se elige un ítem del inventario. La línea de comando se arma sola mientras se pasa el mouse: «Dar Chori al pan a Perro».

La interacción es una máquina de estados finitos (`aventura/scenes/game_scene.py`):

```
IDLE ──clic en hotspot──▶ WALKING ──llega──▶ ejecuta la acción ──▶ IDLE | SPEAKING | DIALOGUE
SPEAKING (Tano o un NPC hablan; clic = saltar la línea) ──▶ IDLE o la acción encadenada
DIALOGUE (opciones múltiples con el mouse)              ──▶ IDLE (o Game Over / Victoria)
```

Mientras Tano camina o habla no se aceptan otras acciones, lo que evita estados inconsistentes. La respuesta a cada acción se busca en una tabla por hotspot con claves `"Verbo"` o `"Verbo:ítem"`. Si no hay una entrada, hay una respuesta por defecto con humor, para que ningún clic quede «mudo». La pausa (ESC) congela la máquina de estados.

### 2.2 Navegación
Cada escenario tiene una **máscara de caminabilidad**: una unión de rectángulos convertida a `pygame.mask`. Un clic fuera de la zona lleva a Tano al punto caminable más cercano, y si choca con un borde se desliza a lo largo de él. Tano **se achica con la profundidad** (escala de 0.7 a 1.1 según la Y) y se dibuja ordenado por Y con los demás personajes, así puede pasar por delante o por detrás de ellos.

### 2.3 Inventario y combinación
Barra inferior horizontal de 8 casillas, como en Monkey Island. Para combinar se elige **Usar**, después un ítem y después otro ítem. Las recetas son una tabla de datos `{frozenset({a, b}): resultado}`, así que el orden no importa.

### 2.4 Diálogos con opciones múltiples
Árboles de nodos (`DialogueNode`) con 2 a 4 opciones que se eligen con el mouse. Las opciones pueden depender del inventario y de las banderas: por ejemplo, el parrillero cambia lo que dice según si la parrilla ya está prendida o si ya tenés el chori. Las líneas sueltas flotan sobre quien habla, con un color por personaje.

## 3. Escenarios

| Escenario | Qué hay | Función |
|---|---|---|
| **Rambla de Barrio Sur** | Banco con termo, mate sobre el muro, tacho con diario, pescador | Recolección inicial; el pescador da la pista con opciones de diálogo |
| **Mercado del Puerto** | Puesto de yerba, parrilla, parrillero, gato durmiendo sobre la leña, tendedero | Combinación del mate; **mini-reto de la parrilla**: prender el fuego y asar el chorizo a tiempo |
| **Museo del Carnaval** (tablado) | Perro hambriento, Contramaestre, cartel y, al final, el bombo | Obstáculo (perro), duelo de payada y victoria |

Los escenarios están conectados en línea (Rambla ⇄ Mercado ⇄ Museo) mediante hotspots de salida.

## 4. Puzles

```
Rambla:   termo ─┐   mate ─┐                     diario (tacho)
                 │         │                          │
Mercado:         │  yerba + mate = mate cargado       │   Usar termo con gato → el gato se va
                 ├─ mate cargado + termo = MATE LISTO │   Agarrar leña
                 │  (el termo se conserva)            diario + leña = FOGATA
                 └──────────────────────────────▶ Usar fogata con parrilla → chorizo + pan
                                                      Usar chorizo con parrilla → ⏱ asar
                                                      Agarrar a tiempo → chorizo asado
                                                      chorizo asado + pan = CHORI AL PAN
Museo:   Dar chori al perro → se va a dormir la siesta → libera el paso → Dar mate listo al Contramaestre
                                     │
                             PAYADA (4 versos) ──▶ bombo ──▶ VICTORIA
                                     └── 3 errores ──▶ GAME OVER (con "Reintentar payada")
```

1. **El mate (combinación en dos pasos):** objetos repartidos en dos escenarios, para obligar a explorar.
2. **El chori al pan (mini-reto de la parrilla):** el jugador hace el chori él mismo, en cuatro pasos:
   - **Espantar al gato**, que duerme sobre la leña: solo le teme al agua y el termo tiene agua. Se lo ve salir corriendo a los saltos.
   - **Armar la fogata**: diario + leña. El papel solo no alcanza, igual que el mate necesita yerba *y* agua.
   - **Prender la parrilla**: el parrillero pone el fósforo y da el chorizo y el pan.
   - **Asar el chorizo con tiempo**: crudo al principio, a punto a los 8 s (Tano avisa «¡huele a gloria!») y quemado a los 18 s, aunque te vayas del Mercado.

   Si se quema, el parrillero da otro, así que equivocarse no traba la partida. La parrilla muestra cómo se va haciendo el chorizo.
3. **La payada (diálogo como desafío):** cuatro versos del Contramaestre, cada uno con tres remates posibles; solo uno rima y tiene sentido. **Tres errores = Game Over.**

### Decisiones de jugabilidad
- **Pistas en el mundo:** el pescador anticipa «mate y chori». El parrillero explica cómo armar el fuego, dice dónde está la leña y que al gato «lo único que lo espanta es el agua». Así ningún puzle depende de probar todo con todo.
- **Mini-retos por pantalla:** la Rambla tiene la recolección y el diálogo con el pescador; el Mercado, la parrilla (combinar y calcular el tiempo); el Museo, el perro y la payada.
- **Sin callejones sin salida:** los ítems clave no se pueden perder ni gastar mal. El termo no se gasta al cebar el mate, porque también hace falta para el gato. Un chorizo quemado se reemplaza, y dar el ítem equivocado solo devuelve un chiste.
- **Perder no castiga de más:** la única forma de perder es la payada. Al perder, **«Reintentar payada»** vuelve al estado guardado justo al aceptar el duelo, sin repetir los tres escenarios.
- **Ritmo:** cualquier línea de texto se salta con un clic, y las caminatas son cortas.
- **Feedback sonoro:** hay sonido en cada clic de UI, al juntar o combinar ítems, en cada acierto o error de la payada, en la victoria y en la derrota. Además, **cada lugar tiene su música**: retirada de murga en el menú, un tema lento con lluvia en la Rambla, candombe en el Mercado y marcha camión en el Museo. Al cambiar de lugar pasa con un fundido, y se puede apagar desde la pausa.

## 5. Pantallas y flujo

**Menú** (Comenzar Juego · Créditos · Salir) → **Juego** (ESC: Continuar · Música Sí/No · Volver al menú) → **Victoria** o **Game Over** (Reintentar payada · Volver al menú). Los **créditos** se leen de una lista de datos (`aventura/data/creditos.py`), así que es fácil sumar gente.

## 6. Arquitectura técnica

- **Una sola `GameScene` parametrizada por datos**, en lugar de una clase por escenario. Escenarios, zonas, hotspots y respuestas están en `aventura/data/rooms.py`; los diálogos y la payada en `dialogs.py`; los ítems y recetas en `items.py`. Agregar un escenario o un puzle es, en general, agregar datos.
- **Estado global** en `game.state` (escenario actual, inventario, banderas de puzles y errores de la payada), separado de las escenas. Las escenas se recrean al cambiar.
- **Arte con respaldo** (`aventura/art.py`): si existe el PNG en `assets/` se usa; si no, se dibuja un reemplazo por código. Un hotspot puede cambiar de sprite según banderas (el tacho sin diario, la parrilla apagada, prendida o con el chorizo crudo, a punto o quemado). Los **temporizadores** (`TIMERS` en `rooms.py`) avanzan con el reloj del juego, que se frena en la pausa, y activan banderas por etapas. Así se programa un mini-reto de tiempo como datos. Un hotspot con `leave` (el gato y el perro) no desaparece de golpe: sale caminando de la pantalla, dado vuelta y con saltitos, mientras el juego sigue.
- **Prueba automática** (`tests/smoke_test.py`): juega partidas completas con eventos reales de mouse, sin ventana. Cubre la victoria, el Game Over con reintento, los créditos, la pausa y los límites de la zona caminable.

### Cambios al motor del curso
Todos están marcados en el código con `# [Tarea 2026]`.

| Módulo | Cambio | Motivo |
|---|---|---|
| `engine/walkmask.py` (nuevo) | Máscara de caminabilidad: `contains`, `nearest`, `step` | Zonas navegables |
| `engine/inventory.py` | Dibujo horizontal y `combine(a, b, recipes)` | Barra inferior y combinación de ítems |
| `engine/dialogue.py` | Opciones con mouse y hooks `on_confirm`/`on_end` | Antes solo se elegía con teclado |
| `engine/dialogue_manager.py` | Texto con color, posición sobre el hablante, ajuste de línea y contorno | Texto flotante estilo Monkey Island |

## 7. Assets y uso de IA

| Asset | Origen |
|---|---|
| Fondos (menú, Rambla, Mercado, Museo) | Pixel art generado con **Pixellab.ai** (IA) |
| Personajes, objetos e íconos | Pixel art generado por código (`tools/gen_sprites.py`); PNG editables |
| Música (un tema por lugar) y efectos de sonido | Sintetizados por código (`tools/gen_musica.py`, `tools/gen_sonidos.py`) |
| Código y diseño | Desarrollo propio con asistencia de **Claude Sonnet 5.5 y Claude Opus 5.5** (Anthropic) |

La lista completa con el origen de cada archivo está en [`brain/wiki/entrega/assets-lista.md`](brain/wiki/entrega/assets-lista.md).

## 8. Posibles mejoras

- Más escenarios (Ciudad Vieja, un conventillo con candombe) y un segundo acto.
- Pathfinding (BFS sobre la máscara) para zonas caminables con obstáculos en el medio.
- Guardar y cargar partida.
- Animaciones de los NPC y retratos en los diálogos.
