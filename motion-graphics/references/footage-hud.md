# Real footage + AI sensor HUD

The approach: run real computer vision on the user's clip and draw the HUD from that data. The overlay then sticks to the hand and objects for real, which is what impressed the user ("ikut pergerakan tangan aku"). Never fake tracking with hand-keyframed points when the model can do it.

## Pipeline
1. **Prep** (`scripts/prep_footage.sh clip.MOV out/`): detects HDR (HLG/PQ) and tonemaps to SDR BT.709 (`zscale … tonemap=hable`). Writes `out/sdr.mp4`, 60 fps JPEG frames `out/vframes/f%04d.jpg` (~140 MB per 16 s, keep out of git) and `out/footage.wav`.
2. **Track** (`scripts/track_footage.py hands out/sdr.mp4 assets/track.json`). It prints a coverage map: `#` means a hand was found, `.` means none. Read it to plan scenes around the tracked windows.
3. **Detect objects** (`… objects … assets/obj.json --allow "laptop,cell phone,cup,chair,dining table"`). Keep `person` out unless the user explicitly wants people labelled. Bystanders in a cafe didn't consent.
4. **Verify**: draw the skeleton on ~12 frames (PIL or a quick page) and look at them before building. Check for left/right label flips (MediaPipe assumes selfie view, so show `HAND_01`, not L/R) and for other people's hands. Label those `HAND_02` or make a joke of it.
5. **Build** the page with `assets/vision-hud.js` (loadTrack, handAt, metrics, lockAge, lostAge, drawHand, drawBrackets, drawAngle, drawTrails, drawPanel, drawFrameHud, drawScan, edgeLayer, drawObj, grade).

## Page mechanics
- `renderAt(t)` is **async**: compute footage time, `await` the frame image (Map cache, ~24 entries), draw it on a 1920×1080 canvas with the camera transform, then the HUD.
- **Speed ramp:** speeds are defined per *footage* time (`[[0,1],[2.0,.5],[2.8,1],[6.2,1.25],[8.4,1.5],[10.8,1]]`) and blended over ±0.12 s. Integrate at 1/1200 s into a table `MAP[out_index] = footage_time` to get `ft(t)` and its inverse `outAt(f)`. Derive **every scene anchor** from `outAt(footage_key)` so text, punches and sound all follow when you retime. Export `window.ANCHORS` and print them, and recompute the same table in the sound script.
- **Smoothing:** loadTrack averages each landmark with its neighbours (±1 frame), keeps the dominant hand and interpolates 30→60 fps.
- **Lost tracking:** keep drawing the last pose for 0.22 s while fading out. Don't pop off.
- **Lock-on reveal:** `reveal = lockAge / 0.3–0.45` (in footage seconds, so slow-mo makes it slower). Points pop wrist→tips and bones draw in order.
- **Objects:** accept a detection only if it matches (IoU > .3) in ≥3 of ±2 frames. Average the box over those frames and animate its lock by its "age" (consecutive frames tracked). Hide boxes that would collide with headlines.
- **Edge-vision / ASCII:** compute per frame from the current image (Sobel at 480×270, ASCII at 14 px cells). Fine for render cost.
- **Glitch:** redraw horizontal slices of the frame shifted by hash-based offsets plus a screen-blended copy.
- Keep a REC/HUD bar and crop marks the whole time. It sells "camera feed".

## Privacy & taste
- No boxes, labels or "detections" on strangers. Track the user's hands and objects.
- Don't show fake metrics as real claims about a business (e.g. "120+ prompts") unless the user confirms them. Use neutral copy or technical facts (1800 frames = 30 s × 60 fps).
