# AGENTS.md — Brain de la Tarea Videojuegos 2D 2026 (Opción 1: Aventura gráfica)

@MEMORY.md

## 1. Rol
Sos el mantenedor de este brain (wiki en Markdown) **y** el desarrollador de la aventura gráfica
point-and-click (estilo Monkey Island 1) en Python + Pygame, sobre el motor del curso (`juego/engine/`).
Idioma de trabajo y de código/comentarios: español (como el curso).

## 2. Mapa de directorios
| Ruta | Qué es | Quién escribe |
|---|---|---|
| `AGENTS.md` | Mapa y reglas (este archivo, < 200 líneas) | humano + agente (solo ante correcciones repetidas) |
| `CLAUDE.md` | Una línea `@AGENTS.md` para que Claude Code cargue este archivo; no agregarle contenido | humano |
| `MEMORY.md` | Hechos permanentes: fechas, stack, juego elegido, restricciones | agente |
| `LEARNINGS.md` | Lecciones aprendidas durante el desarrollo | agente |
| `decisions.md` | Log de decisiones (incluye cambios al motor) | agente, append-only |
| `raw/` | Fuentes originales: tarea PDF, guía brain PDF, notebooks clases 1-4/5/6/8, `aventura.py` (clase 6), zip del motor | **INMUTABLE** — nunca editar |
| `wiki/index.md` | Catálogo de TODAS las páginas | agente |
| `wiki/log.md` | Registro append-only de actividad | agente |
| `wiki/hot-cache.md` | Estado actual + próximos pasos | agente |
| `wiki/requisitos/` | Qué exige la tarea | agente |
| `wiki/clases/` | Resumen de lo aprendido por clase | agente |
| `wiki/motor/` | Una página por módulo de `engine/` | agente |
| `wiki/diseno/` | Arquitectura y diseño del juego | agente |
| `wiki/entrega/` | Checklist, README, assets, guion de video | agente |
| `juego/` | Proyecto ejecutable (`engine/` + `aventura/` + `tests/`) | agente |
| `tools/lint.py` | Lint del brain (links, index, frontmatter) | agente |

## 3. Protocolo de lectura (siempre, antes de responder o codear)
1. `MEMORY.md` → `wiki/hot-cache.md` → `wiki/index.md`.
2. Abrir solo las páginas relevantes; antes de usar un módulo del motor leer su página en `wiki/motor/` **y** el código real en `juego/engine/`.
3. Si algo no está en el brain ni en `raw/`, decirlo como **gap**; no inventar.
4. Citar páginas con wikilinks al responder.

## 4. Convenciones de escritura
- Un tema = un archivo. Nombres en kebab-case minúsculas (`fsm-verbos.md`). Sin espacios.
- Frontmatter obligatorio en `wiki/**`: `title`, `type` (requisito|clase|motor|diseno|entrega), `sources` (rutas en `raw/` o `juego/`), `updated` (AAAA-MM-DD).
- Enlaces internos con wikilinks: doble corchete + slug (slug = nombre de archivo sin `.md`).
- Toda página nueva → agregar línea a `wiki/index.md` y una entrada a `wiki/log.md` (`AAAA-MM-DD | acción | página`).
- Al cerrar una sesión: actualizar `wiki/hot-cache.md` (hecho / siguiente / bloqueos) y, si hubo aprendizajes, `LEARNINGS.md`.
- Operaciones nombradas: **ingest** (incorporar una fuente nueva a `raw/` y compilarla en wiki), **query** (responder citando páginas), **lint** (huérfanos, links rotos, contradicciones, páginas fuera de `index.md`).

## 5. Restricciones duras
- Solo Python + Pygame. Ejecutable con `python -m aventura.main` desde `juego/`.
- Usar el motor del curso; cualquier cambio/extensión a `engine/` se marca con `# [Tarea 2026]` en el código y se documenta en `decisions.md` y `wiki/motor/cambios-al-motor.md` (la tarea lo exige).
- **Todo** click/interacción de UI (botones, verbos, inventario, diálogos) reproduce sonido (requisito común).
- Pantallas obligatorias: Inicio (botón "Comenzar Juego"), Game Over, Victoria, ambas con volver al menú.
- Mínimos opción 1: verbos, inventario con combinación, ≥3 escenarios conectados con zona navegable, diálogos con opciones múltiples, ≥2 puzles, FSM, hotspots.
- Todo asset externo se registra en `wiki/entrega/assets-lista.md` con su origen/licencia.
- No commitear `.venv/`, `.idea/`, `__pycache__/`. Nunca editar `raw/`.
- El motor falla en silencio si falta un sonido: aun así, entregar los `.wav` reales.

## 6. Comandos
- Correr el juego: `cd juego && python -m aventura.main`
- Prueba de humo (sin ventana): `cd juego && python tests/smoke_test.py`. Correrla antes de dar algo por terminado y ampliarla con cada feature.
- Lint del brain: `python3 tools/lint.py`. Correrlo después de crear o mover páginas.

## 7. Fechas clave
Parcial 23-oct-2026 (ya pasó, esperado 50%). **Entrega final 6-nov-2026** (GitLab público + README + doc de diseño + lista de assets + video 15–40 s + defensa).
