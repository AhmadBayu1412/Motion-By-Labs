# Gotchas (each one cost a render)

- **Determinism:** no `Math.random()`, `Date.now()`, CSS transitions/animations or rAF state in capture mode. Use `hash(n)` and compute everything from `t`. Cache per-frame data only if it is a pure function of t.
- **`reelReady` with ES modules:** top-level `await` (fetch, fonts) runs before `window.reelReady` exists. render.mjs waits for it to be defined. If you write your own harness, do the same.
- **Fonts:** `font-display:block` plus `await document.fonts.load('800 100px "Family"')` for every family/weight before the first frame, and before building canvas-texture labels in three.js.
- **Canvas `letterSpacing` leaks:** `ctx.letterSpacing` persists across `fillText` calls. Reset it to `"0px"` in every mono helper, or HUD text gets squished.
- **Word spans glue together:** `display:inline-block` words need `margin:0 .12em`.
- **Measure, don't guess, morph anchors:** positions like "where the cursor clicks" or "where the last word ends" should be measured in `reelReady` with transforms temporarily reset. A guessed click point (1215,718) once spilled from the wrong place.
- **Edges and safe areas:** right-aligned headlines (`align:"right"` at x=1830–1840) instead of left-anchored ones that run off-screen. Clamp floating cards (x 180–1740, y ≥ 110) and object labels (x ≥ gutter).
- **Overlaps:** check stills for text over cards and boxes. Fixes that worked: fade the headline earlier, filter boxes intersecting the headline band, put text in a glass capsule.
- **Splicing re-renders:** concat-demuxing separately encoded parts shifted timing by ~2 s. Use `scripts/splice.sh` (one filter graph, trim by frame) and verify a frame inside the patched range.
- **HDR footage** looks washed out unless tonemapped (prep_footage.sh).
- **MediaPipe:** needs `libegl1 libgles2`; it may crash in its close handler, so the script calls `os._exit(0)` after writing. The left/right label is unreliable on POV footage.
- **WebGL speed:** VSM 1024 shadows, an adaptive frustum and `--sub 2`. PCF 2048 took ~100 min.
- **`pkill -f <pattern>`** can kill your own shell (exit 144) when the pattern matches the command line. Use distinct `pgrep` patterns.
- **Stale audio:** render.mjs regenerates the WAV on every render. If you mux by hand, regenerate after any retime.
- **Claims:** don't invent stats ("120+ modul", "4,9/5") as fact. Mark them as examples or ask.
- **Long renders:** run in the background, tell the user, and use the time to write the docs and the keyframe-sheet template. A 20 s footage film at `--sub 2` takes ~3–4 min, a 30 s DOM film at `--sub 3` ~4–10 min.
