# Storyboarding: reference analysis, deliverables, copy

## When the user sends a reference video
Run `scripts/analyze_reference.py ref.mp4 out/ref --fps 2 --hi <times>` and **look at every contact sheet**. Then write down, in a table:
- **Canvas & colour:** background, grid or texture, how many accents and what they are used for.
- **Protagonist:** is there one object that travels or morphs through the film?
- **Transitions:** count the hard cuts (the script prints them; few cuts means morph-driven). Name each transition technique.
- **Rhythm:** move/hold durations, stepped vs smooth motion, camera drift.
- **Typography:** headlines vs UI-only text, mono labels, the end card.
- **Audio:** music-led (regular intervals ≈ 60/BPM) or SFX-led (dense irregular onsets).
- **Structure:** genesis → use → scale → proof → ecosystem → logo, or whatever its arc is.
Then map each technique onto the user's brand ("di referensi … → versi kita …"). That table goes in the storyboard doc, and it is what convinced the user the style was understood.

## Deliverables before building (when the user says "storyboard dulu")
1. **Storyboard sheet PNG** made from an HTML page (`<name>-board.html` → `scripts/shot.mjs`): a header with title and tokens, then 9–13 panels as real mini illustrations (CSS/SVG/canvas, using real footage frames and real tracking data when there is footage), each with name, time range and a 1–2 line motion description with the key object highlighted in the accent colour. Add a footer with 4 columns: motion grammar, pixel/stepped language or palette, typography, sound design. For HUD work, add a large hero panel with **lettered callouts A–J** and a legend: this is the "design metrik".
2. **Storyboard MD** (`storyboard-<name>.md`): reference analysis table → tokens table → motion rules → scene table (`# | time | scene | motion & effects | text motion | bridge to next scene`) → asset list → sound design per event → production plan → "what can be changed before ACC" (accent colour, duration, real content to insert, counter copy).
3. Send both, summarise in the user's language, and **wait for ACC**. Questions at the end should be few and concrete (colour, duration, which real assets go where).

## After ACC: production log
Update the MD: status "ACC → rendered", final timing table (after ramps), how to regenerate data and frames, render command. Keep the original draft below it ("Draf awal") when the plan changed (e.g. 52 s → 30 s).

## Final delivery
- MP4 at 1920×1080 60 fps (or 1080×1920 / 1080×1350 when asked), named `<name>-<dur>s.mp4`, in a `video/` folder.
- Thumbnail PNG from the most representative frame (usually the logo or CTA).
- Keyframe sheet (`scripts/keyframe_sheet.py`) with 12 frames, each at a readable moment.
- Commit sources (page, sound script, data JSON, small assets) and outputs. Leave big intermediate frames out of git.
- Reply: a short summary of how the brief was met (feedback point → what changed), the scene/time table, the audio summary, an offer to retime or swap copy, file paths.

## Copywriting (Indonesian brand promos)
- Short, spoken, a bit cheeky. Hook question → pain → product → "lebih gampang dari yang kamu kira" → proof → CTA. Examples that landed: "Punya ide bisnis, tapi semua masih manual?", "Bisnismu, versi otomatis.", "Dan BOOM.", "Butuh 3 bulan? Sebulan? Santai. 3 minggu cukup.", "Gerakanmu… jadi kode.", "Satu gerakan, semua ada di Labs.", "make things move."
- Keywords in the accent colour, at most 1–2 per line.
- CTA: action + channel (`Konsultasi via WhatsApp →`, `Gabung member → ngorz.xyz`) + handle.
- Absurd mode: jokes tied to visible things, in code syntax (`const jari = 5; // udah dicek 3x`).
