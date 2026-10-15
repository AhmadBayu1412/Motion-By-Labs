# Motion language: timing, easing, camera, transitions, text

These numbers came from rounds of user feedback ("masih kaku" = still stiff, "lebih cepat dan dramatis" = faster and more dramatic, "transisinya jelek, buat mengalir" = the transition is ugly, make it flow). Start here, then tune by looking at stills.

## Easing (all in assets/template.html)
- **expo-out `ex`**: the default for anything entering. It snaps in, then glides. Feels fast without being jerky.
- **expo-in `exin`**: exits and falls (cards flying out, a pixel dropping).
- **expo-in-out `exio`**: camera moves, tilts, unwraps.
- **spring** `1 − e^(−6p)·cos(11p)`: ~15% overshoot that settles fast. Use it for pops, chips, tags, buttons and cards landing.
- Avoid linear motion except scan lines and progress bars. Avoid long sine easing; it reads as "floaty / stiff".

## Tempo
- Typical move 0.35–0.6 s, then **hold 0.4–0.8 s** (snap & hold). Nothing should drift for more than ~1 s without a beat.
- Words land every **0.055–0.085 s** (fast) or on the beat (0.25 s at 120 BPM). Letters fly at 0.018–0.07 s each.
- Scene length: 1.5–3.5 s. 30 s holds ~10–12 scenes. Users preferred trimming 40→29 s and 52→30 s to keep it tight.
- Hold the final CTA or logo for ≥1.8 s (a 0.5 s CTA was a bug the user caught).
- Speed ramps on footage: 0.5× for a hero moment (lock-on), 1.25–2× through boring pans. Blend speed changes over ~0.24 s so they don't jump (see footage-hud.md).

## Camera
- Put a `#world` wrapper around everything and apply the camera there: `translate + scale` around the centre.
- **Punch:** on every hard hit (slam, click, BOOM, logo), scale += a·e^(−7d) with a ≈ .02–.08, plus a shake of ±14 px decaying e^(−10d). List punches in one array and fire a matching kick in the sound script.
- **Drift:** 2–4% push or pan per scene, so even holds feel alive.
- **Follow:** when a dot travels, shift the camera by ~22% of its offset from centre.
- **Whip-pan** (bento): 0.6 s spring with a zoom dip, motion blur from sub-frames, a thin accent flash on landing.
- Base scale 1.035 on footage so shakes never reveal edges.

## Transitions that "flow" (no hard cuts)
Every scene should end with an object that becomes the first object of the next scene. Tested patterns:
- **Click spill:** a cursor clicks a button, the brand colour floods out of the *click point* (`clip-path: circle(r at x y)`), the logo appears, the colour shrinks back to a point, and new content bursts out of that point. Measure the click point from the DOM in `reelReady`; don't hard-code it.
- **Box bloom:** a small keyframe box or pill animates its rect into the next card (left/top/width/height/radius/colour together).
- **Collapse to pixel:** highlights fly to the centre and become one pixel, which then extrudes into a 3D cube.
- **Mosaic flood:** cells fill from the edges inward (threshold by edge distance + noise, stepped at 12 fps), then shrink away to reveal the next scene.
- **Unwrap:** a sphere's lat/long lines lerp into a flat grid whose rect equals the next card's rect.
- **Dither / wireframe / code sweeps:** three stacked layers revealed by left→right `clip-path: inset()` fronts, stepped at 24 fps.
- **Line collapse:** a black bar closes from top and bottom to a 4 px accent line, which then opens into the outro.
- **Stair wipe:** a stepped wedge of accent and grey columns sweeps across and leaves white behind.
- **Scan reveal:** footage, a headline or edge-vision is visible only above a moving scan line.
- Overlap scene windows by 0.1–0.3 s so the morph objects exist in both scenes.

## Text motion
- **Word slide-up + unblur** (template `reveal`): opacity, translateY 40→0, blur 12→0. Exit: blur and rise.
- **Typed** text with a block cursor for code, terminal and "AI is reading" moments (cps 22–60). Pair it with key-press foley.
- **Letters born from an object:** each letter flies from a tracked point (fingertip, star, pixel) to its slot, scale .3→1.
- **Tethered labels:** a headline next to the subject with a leader line to a tracked point. Keep it on-screen: right-align against a 80–96 px safe margin.
- **Scan-revealed headline:** clip the text to the scanned area.
- **Big beat words:** thin display weight for the hook word, 800 for statements, mono uppercase for labels.
- **Colour adapts to the background:** dark gradient ink on light, white on dark or navy, a glass capsule on busy imagery. Never navy on navy.
- Watch word spacing when you split words into spans (`margin:0 .12em`), or "versiotomatis" glues together.

## Components (keep ONE system per film)
Card radius, border, shadow, chip height, icon tile size, button shape: define them once as classes or tokens and reuse them. Mismatched components were a direct user complaint.

## Stepped vs smooth
Use stepped time `q(t, 12)` for pixels, counters, typing and HUD jitter, and smooth time for camera and cards. The contrast reads as "digital" and premium. Snap stepped positions to the grid (`snap(v, 30)`).

## Motion blur
render.mjs averages `--sub` samples across a 180° shutter. Use `--sub 2–3` for most films, 6 for slow hero reels, 2 for WebGL or footage (render time).
