# Style catalog

Every look below has been rendered, reviewed and approved. Each entry gives its tokens, motion signature and what made it work, so you can reuse it or mix it. Source pages live in the Otak Rental repo under `motion/` when that repo is available. They are worth opening for exact code.

Contents
1. Editorial cream (Otak Rental reels)
2. Monochrome studio (Labs intro / portfolio reel)
3. Isometric 3D build (three.js)
4. Soft-Cyber bento
5. SaaS explainer: light + navy
6. Pixel brand film
7. Sensor HUD on real footage
8. Absurd full-code editor
9. Kinetic poster (Syne)
10. Choosing / mixing

---

## 1. Editorial cream (Otak Rental brand reels)
*Sources: showreel.html (15 s), sample.html, konsultasi-eror.html, web-examples.html, tutorial-claude-code.html*
- **Tokens:** cream `#FAF7F0`, paper `#FFFDF8`, forest ink `#05100E`, emerald `#17463A`, lime accent `#D4E751`, line `#E6DFD0`, coral `#EE5A32` only for errors.
- **Type:** Geist (UI and headlines), Geist Mono (labels, countdowns, boot lines), Instrument Serif italic (taglines).
- **Motion signature:** a lime drop squashes and bursts into the 8-petal emblem. Chips crash in. A countdown turns red with camera shake. Formula tiles flip with slot-machine digits. Match cut from the total card into a service card. A 3D bento tilt. A lime iris and staggered ink bars as wipes.
- **Why it works:** a warm, premium base, with one loud accent kept for the protagonist (the drop and the CTA).

## 2. Monochrome studio (Labs.)
*Sources: labs-intro.html (45 s), labs-reel.html, labs-ui-object.html, labs/banner.html*
- **Tokens:** dark `#030407` / `#0A0A0A` or light `#F4F4F2`, fg `#F2F4F8`, navy glow `rgba(40,80,200,.22)`, grid lines at 6%, crop marks in 4 corners, grain 7% overlay.
- **Type:** big Geist 800 wordmark `Labs.`, Instrument Serif italic tagline (*make things move.*), Geist Mono uppercase labels with .18em tracking (`01 · MOTION`).
- **Motion signature:** a wireframe sphere "draws itself" line by line, an orbit ring with a travelling dot, and banner pills with leader lines pointing at the sphere.

## 3. Isometric 3D build
*Sources: labs-iso-story.html (30 s), otak-services.html · three.js r170 vendored (`vendor/three.module.min.js` + RoundedBoxGeometry)*
- **Tokens:** navy `#121D4D`, mid `#2C3F94`, glow `#4C7DFF`, light floor `#F3F4F7`.
- **Camera:** PerspectiveCamera with fov ≈15 placed far away gives a near-orthographic isometric 3/4 view. Use `setViewOffset` to slide the composition (a negative value moves the scene right). Floor is a ShadowMaterial. VSM shadows at 1024 with blurSamples 10, and the shadow frustum fitted to the content (2048 PCF took ~100 min to render).
- **Motion signature:** one continuous build, with no cuts. Blocks rise from the floor on springs and modules snap together. The camera orbits slowly while the story grows into a full lab.
- **Gotcha:** canvas-texture labels need `await document.fonts.load(...)` before the scene is built.

## 4. Soft-Cyber bento
*Source: otak-softcyber.html (46 s, 120 BPM)*
- **Tokens:** charcoal `#07080B`, fg `#EEF1F7`, neon cyan `#22D3EE`, violet `#8B5CF6`, orange `#FB923C`, red `#F43F5E` for problems. Three slow colour fogs, a thin grid, 6% grain.
- **Materials:** real frosted glass (`backdrop-filter: blur(26px) saturate(160%)`, radius 38, top highlight, inner shadow). "Soft clay" icons (rounded, highlight plus inner shadow). Neon circuits run *behind* the glass, sharp in the gaps and blurred under the cards.
- **Motion signature:** a "Bento Box" camera with 0.6 s whip-pans between cards (spring easing, ~4% landing bounce, zoom dip, cyan flash), and a 3.5% push-in while it holds on a card. Pattern per service: a **problem card (messy)** → whip → **solution card (tidy)** → that circuit lights up.
- **Type:** kinetic Geist 800 at 100–150 px. **Each word lands on the beat** (0.25 s): scale 1.35→1, blur 10→0, elastic. Keywords get a neon gradient and glow.

## 5. SaaS explainer: light + navy blur
*Sources: otak-saas.html (40 s), **otak-saas-v2.html (29 s, the approved one)**. Modelled on a "Vyve"-style SaaS reference.*
- **Tokens:** light bg `#F4F6FB` plus a navy blurred gradient (`#0B1640 → #1E3A8A → #3B5BDB`). Text **adapts to its background**: on light it is gradient ink `#0B1640→#1E3A8A` with keywords in gradient blue `#1E3A8A→#3B5BDB`, on navy it is white with accent `#BFD0FF`. Text that sits over busy cards goes in a light glass capsule.
- **Type:** Plus Jakarta Sans everywhere: display 200 (thin "Punya"), headline 800, narration 600, labels 700 uppercase.
- **Components (one system):** card radius 24, 1 px border, one shadow; chip 56 px pill; icon tile 96 px radius 26 with gradient stroke; pill gradient button; accent = navy `fill` variant.
- **Motion signature:** a giant thin word zooms through the camera. Words land at 0.055–0.085 s each. A 3D "×" slams with punch and shake. A tilted dashboard flies in, the cursor clicks a KPI, then pulls back to the hero. **Flowing transition:** cursor clicks the CTA → navy floods out of the click point (`clip-path: circle()`) → white logo → navy shrinks back to a point → 5 service cards burst out of that point. Then "BOOM." shockwave rings, a process list (doc → 9-screen board → tool pipeline → release spinner → ✓), a time riddle ("3 bulan? Sebulan? **Santai.** 3 minggu cukup."), a 20-card helix, and a CTA where the star flies in and grows into the navy lock-up.
- **User feedback that shaped v2:** "too stiff" → faster and more dramatic (expo-out, punch and shake on every hit, 40 s → 29 s). "ugly font" → Plus Jakarta Sans. "text colour doesn't adapt" → the adaptive ink rules above. "inconsistent components" → one component system. "transition into the logo is ugly" → the click-spill flow.

## 6. Pixel brand film
*Source: labs-pixel-film.html (30 s). Modelled on Firecrawl's brand film.*
- **Tokens:** off-white `#F4F4F2` with a 55–60 px grid and `+` marks at intersections, ink `#0E0F12`, pixel greys `#E4E4E1 / #C9C9C5 / #8C8C88`, dark cards `#17181B`, **one accent** `#2E5BFF` (Labs Blue; the reference used orange `#FF4F00`).
- **Protagonist:** **one accent pixel** that keeps changing form: blinking dot → pixel flask → dot sliding along an easing curve → keyframe box → card → 3D cube → tile on a globe → button → counter digits → stair wipe.
- **Motion grammar:** pixels move **stepped** (12 steps/s, snapped to the grid) while camera and cards stay smooth at 60 fps. Snap and hold (expo-out 0.35–0.6 s, hold 0.4–0.8 s). Constant slow camera drift (2–4% per scene). **No hard cuts.** Every scene ends with an object that *becomes* the next scene's first object.
- **Signature transitions (use each once):** dark pixel mosaic flooding from the edges; halftone dither dissolve (ordered Bayer 4×4, warm source colours → accent dots); grid ⇄ wireframe globe unwrap; 3D tilted wall of pages plus a grey dim veil to focus one card; flip-board counter; stepped pixel stair wipe → white → wordmark.
- **Type:** no narration headlines. Text appears only inside UI cards and as mono bracket labels `[ PROMPT ] [ ANIMATE ] [ RENDER ]`. The only big type is a counter and the logo.
- **Audio:** SFX-led, no beat (see sound.md).

## 7. Sensor HUD on real footage ("LABS.VISION")
*Sources: labs-vision.html + vision-hud.js (20 s), labs-vision-board.html (storyboard + metric design sheet)*
- **Data:** real MediaPipe hand landmarks (21 points at 30 fps) and EfficientDet object boxes from the footage (see footage-hud.md).
- **Grade:** multiply rgba(150,165,205,.42), vignette, 4 px scanlines at 7%, so the HUD glows without killing skin tones.
- **HUD kit (A–J):** a 21-point skeleton (white bones 3.2 px with blue glow, square joints, pulsing fingertip rings with IDs, wrist crosshair); palm mesh at 16%; lock-on brackets that shrink 1.5→1× with a `HAND_01 · LOCK 0.97` tab; **code-token trails** along fingertip paths; thumb↔index angle arc and pinch distance; telemetry panel (FPS, latency, wrist XY, velocity sparkline, spread, gesture bars); camera HUD (crop marks, blinking REC, timecode, mode); scan line + Sobel edge-vision; dashed marching object boxes; UI cards fanning out of the palm and following it.
- **Story:** boot → hand lock (0.5× slow-mo) → line code ("Gerakanmu… / …jadi kode.", where the letters fly out of the index fingertip) → object scan (typed) → room scan (2× ramp, edge-vision, headline revealed by the scan line) → re-lock with a portal ring → cards on the palm → glitch → outro where the brackets lock onto the logo.

## 8. Absurd full-code editor ("tangan.js")
*Source: tangan-js.html (20 s, same footage and data as #7, no brand)*
- **Frame = code editor:** tabs `tangan.js ● kantin.json badan.ts TODO_ending.md`, a scrolling line-number gutter, a status bar whose error count climbs 0→404, `JavaScript (katanya)`.
- **Palette (syntax):** keyword `#C792EA`, function `#FFD866`, string `#FF9E64`, number `#B5E8A0`, comment `#6E8B74`, var `#8FD3FF`, type `#5EE6C8`, error `#FF5C7A`. Everything is Geist Mono.
- **Devices:** bones drawn as repeated text (`telunjuk[0] telunjuk[0]…`); fingers as processes (`kelingking.exe → janji()`); a `$ top -tangan` panel with real CPU% from fingertip speed; console logs (`418 I'm a teapot`); objects labelled with ridiculous constructors (`new Laptop({ tab: 47, ram: "nangis" })`); the room re-rendered as coloured **ASCII**; a cascade of error toasts; floating code windows on the palm; a literal stack overflow (`console.log("halo")` flood); a terminal ending (`Segmentation fault`, a self-blaming git commit, a falling `}`, `// TODO: kasih ending`).
- **Humour rule:** jokes are specific to what is on screen (5 fingers, es teh, the cafeteria). Generic programmer memes land worse.

## 9. Kinetic poster (Syne / Anton)
*Sources: everything-moves.html (30 s), reel30.html (9:16)*
- Syne or Anton display, Instrument Serif italic counter-voice, Geist Mono captions. Large type is the image. Use it for portfolio or "motion reel" pieces where typography carries the whole piece.

## 10. Choosing / mixing
| Brief sounds like… | Start from |
|---|---|
| Service promo, "explain what we do", SaaS-ish | #5 (light + one gradient) or #4 (dark neon) |
| Brand film, "make it flow", minimal | #6 pixel film |
| Product or lab story, 3D, "isometric" | #3 |
| Real footage + "AI / sensor / tracking" | #7 |
| Funny, meme-y, "absurd", no brand | #8 |
| Portfolio reel, type-driven | #9 or #2 |

Mixing rule: keep **one** protagonist object and **one** accent colour per film. When the user sends a reference video, its grammar wins. Analyse it first (storyboarding.md) and map it onto the brand's tokens.
