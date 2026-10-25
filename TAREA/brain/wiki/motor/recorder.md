---
title: engine/recorder.py y timeline.py — Recorder, Timeline
type: motor
sources: [juego/engine/recorder.py, juego/engine/timeline.py]
updated: 2026-10-25
---

# engine/recorder.py y timeline.py — Recorder, Timeline

- `Recorder(output_dir, fps=30)`: `capture(surface)` guarda `frames/frame_%05d.png`; `export("video.mp4")` usa **FFmpeg** si está en el PATH (si no, conserva los PNG); `clear()`. Sirve para el video de 15–40 s ([[video-guion]]); alternativa: grabador de pantalla del SO.
- `Timeline(duration, loop)`: `add_event(t, callback)`, `add_tween(obj, attr, start, end, t0, t1, easing)` (easings `linear/ease_in/ease_out/ease_in_out`), `update(dt)`. Útil para cinemáticas cortas o mover al personaje.
