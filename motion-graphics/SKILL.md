---
name: motion-graphics
description: Produce motion-graphics videos (brand reels, promo/explainer videos, logo reveals, kinetic typography, isometric 3D builds, pixel brand films, AI "sensor HUD" overlays on real footage with hand tracking, absurd code-themed edits) as deterministic HTML/canvas pages rendered to MP4 with real motion blur and procedural sound design, plus storyboard sheets, design-metric sheets and keyframe sheets. Use this whenever the user asks for a motion video, video promosi/konten/reels, animasi, storyboard, "bikin video kayak referensi ini", a reference video to imitate, motion for a brand or service, a video from their own footage with effects/tracking/text, or wants an existing motion video re-timed, re-styled, made faster/more dramatic, or re-rendered — even if they don't say "motion graphics".
---

# Motion graphics

Make broadcast-quality motion videos with code. Each film is one HTML page whose look is a pure function of time `t` (`renderAt(t)`). A headless browser samples it frame by frame with sub-frame motion blur, and ffmpeg encodes the result with a procedurally synthesised soundtrack. Because everything is code you can match a reference precisely, use real tracking data, retime anything, and re-render any range.

Talk to the user in their language (the original user writes Indonesian, casually). Keep replies short: what was made, a scene table, what to check, file paths.

## Workflow

### 1. Understand the brief (and any reference)
- Note the brand tokens: logo, colours, fonts, handle/CTA. If the brand exists in the repo, reuse its tokens. Don't invent a new palette.
- If there is a **reference video**, run `scripts/analyze_reference.py` and **look at the contact sheets**. Describe its canvas, protagonist, transitions, rhythm, type and audio before designing (see `references/storyboarding.md`).
- If there is **footage of the user**, prep and track it first (`references/footage-hud.md`) so the storyboard shows real data.
- Pick or mix a look from `references/styles.md`.

### 2. Storyboard first when asked (or for anything over ~15 s)
If the user says "storyboard dulu", "jangan langsung bikin video", or "kalau ACC baru generate", deliver the storyboard sheet PNG and the storyboard MD, then **stop and wait for approval**. The format is in `references/storyboarding.md`. The sheet is an HTML page of real mini illustrations, screenshotted with `scripts/shot.mjs`, not a text list. For HUD/sensor work, add a lettered design-metric hero panel.

### 3. Build the page
- Start from `assets/template.html` (time helpers, easing, words reveal, scene layers, camera punches, `reelReady`). Copy `assets/fonts/` next to it. For footage HUDs, also copy `assets/vision-hud.js`.
- Follow `references/motion-language.md`: snap-and-hold timing, expo-out/spring easing, a punch on every hit, flowing morph transitions (no hard cuts), one component system, text colours that adapt to the background, one protagonist object and one accent.
- Keep everything deterministic (`references/gotchas.md`).

### 4. Check stills before the full render
`node scripts/render.mjs --root <dir> --page film.html --name f --stills 0.5,1.8,…` with 12–24 timestamps covering every scene and transition. Tile them into contact sheets (`ffmpeg … tile=4x3`) and **look**. Fix overflow off-screen, text overlapping cards, wrong morph anchors, unreadable text, empty frames. Iterate until clean. This loop is where the quality comes from.

### 5. Sound
Write `<name>_sound.py` with `scripts/sfx.py`. Map every visible event to a sound, using the same timeline constants as the page (`references/sound.md`). Choose music-led or SFX-led to match the style or reference.

### 6. Render, verify, deliver
- `node scripts/render.mjs --root <dir> --page film.html --name film-20s --sound film_sound.py --sub 3` (`--sub 2` for footage or WebGL). Run long renders in the background and write the docs meanwhile.
- Verify: `ffmpeg -i` (duration, 60 fps, audio stream) and `-af volumedetect` (mean ≈ −22 dB, max ≈ −3 dB). Extract frames at key times and look at them.
- Make the thumbnail and keyframe sheet (`scripts/keyframe_sheet.py`). Update or write the storyboard MD with final timing and the re-render command.
- Commit sources, data and outputs (not big intermediate frames). Send the MP4 and the keyframe sheet to the user.
- To fix one part later, re-render only that range (`--from/--to --noaudio`) and `scripts/splice.sh` it, then verify a frame inside the patch.

## Principles the user consistently rewarded
- **Fast and dramatic beats long and stiff.** Trim duration to the pacing (40→29 s, 52→30 s). Use expo-out snaps, camera punches with shake, and words every ~0.07 s.
- **Flowing transitions:** each scene's last object becomes the next scene's first (click → colour spill → logo → point → cards). Hard cuts and fades read as cheap.
- **Consistency:** one font family system, one card/chip/button system, one accent colour, text colour that adapts to the background.
- **Real over fake:** real tracking data, real detected objects, real footage frames in the storyboard, real numbers (or clearly neutral copy).
- **Creative boldness:** when the user says "se-creative mungkin" or "bikin absurd", commit fully to a concept (a whole-film metaphor like "the frame is a code editor") rather than adding effects.
- **Privacy and honesty:** no labels on bystanders, no invented stats or claims.

## Bundled resources
| Path | Use |
|---|---|
| `scripts/render.mjs` | HTML → MP4 (motion blur, workers, stills, range render, audio mux). Needs Playwright Chromium + ffmpeg. |
| `scripts/sfx.py` | Procedural audio: `Mix`, kicks, whooshes, risers, bells, typing, glitch, boing, footage resample, reverb, mastering. |
| `scripts/analyze_reference.py` | Contact sheets, hard cuts, audio onset rhythm of a reference video. |
| `scripts/prep_footage.sh` | HDR→SDR tonemap, 60 fps frames, audio from a phone clip. |
| `scripts/track_footage.py` | MediaPipe hand landmarks / object boxes → JSON (+ coverage map). |
| `scripts/keyframe_sheet.py`, `scripts/shot.mjs` | Keyframe sheet PNG from a video; screenshot any local HTML page. |
| `scripts/splice.sh` | Frame-accurate replacement of a re-rendered range. |
| `assets/template.html` | Starting page with all helpers. |
| `assets/vision-hud.js` | Sensor HUD kit for footage (skeleton, brackets, trails, telemetry, scan, edge-vision, object boxes). |
| `assets/fonts/` | Geist, Geist Mono, Instrument Serif, Plus Jakarta Sans, Syne, Anton (OFL). |
| `references/styles.md` | Catalog of 9 proven looks with tokens and motion signatures. Read when choosing a look. |
| `references/motion-language.md` | Timing, easing, camera, transitions, text motion. Read before building. |
| `references/sound.md` | Event→sound mapping, music-led vs SFX-led. Read before writing the sound script. |
| `references/footage-hud.md` | Real-footage pipeline, speed ramps, tracking HUD. Read when the user sends a clip. |
| `references/storyboarding.md` | Reference analysis, storyboard deliverables, delivery checklist, Indonesian copy. |
| `references/gotchas.md` | Mistakes that cost renders. Skim before every build. |

Environment notes: Playwright's Chromium is often preinstalled (`PLAYWRIGHT_BROWSERS_PATH`). Don't run `playwright install` if it is. WebGL needs the `--enable-unsafe-swiftshader` flag render.mjs already passes. three.js isn't bundled. Vendor `three@0.170` (`build/three.module.min.js` + `examples/jsm/geometries/RoundedBoxGeometry.js`) next to the page and load it with an importmap.
