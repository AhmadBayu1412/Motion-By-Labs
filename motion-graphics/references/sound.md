# Sound design (procedural, stdlib only)

Every film ships with its own `<name>_sound.py` that builds a WAV with `scripts/sfx.py`. render.mjs runs it and muxes the result. No samples and no licensed music, so there are no rights problems on Instagram or YouTube.

## Two modes, pick per style
1. **Music-led** (promos, SaaS explainers, Soft-Cyber): a BPM grid (120–128), a pad chord loop (F–C–Am–G or Am–F–C–G), kick on 1/4, off-beat hats, an 8th-note pluck arpeggio. Arrange it in sections: **drop** when the product appears, **break** on a soft line ("lebih gampang…"), **drop** on BOOM, **stop the beat** for riddles (single kicks per question), **drop** for the finale, **resolve** on the logo. Every word that lands on the beat gets a transient tick.
2. **SFX-led** (brand films, HUD, absurd): no drum grid, just a thin drone (Am, low gain .008–.03) plus **one micro-sound every ~0.25–0.35 s**. This density was measured on the Firecrawl reference (129 onsets in 66 s). Big hits only at 2–3 key moments.

## Map events → sounds (the core of it)
List every visible event with its time, then add a sound per row. Reuse the page's own timeline constants (or recompute them identically) so audio stays locked when you retime.
| Visual event | Sound |
|---|---|
| Camera punch / slam / BOOM | `kick(70–120 → 30–45)` gain .2–.46 + short noise |
| Logo / final lock-up | sub drop `kick(55,26,1.6,2.6)` + `bell_chord` (4–5 notes, 30 ms stagger) |
| Morph / whip / scene change | `whoosh(.35–.6)` rising, or falling for collapses |
| Pixel step / landmark pop / tag | `blip(k)` pentatonic, rising pitch while building, falling while breaking apart |
| Typed text | `typing(t0, chars, cps)`, one knock per character |
| Click | `knock(1800–2200)` |
| Lock-on / bracket | `lock()` |
| Card / chip pop | `pop(500–1000)` stepped up in pitch |
| Error | `bonk` (kick 420→180 + low bell), `buzz` for a segfault |
| Absurd / comedic beat | `boing` |
| Glitch / mosaic | `glitch(t, dur)` + a sub drop when it covers the screen |
| Riser before a reveal | `riser(.25–.6, low→high)` |
| ✓ / ✦ / success | `tone(1567.98, .9, …, "bell")` + an octave above |

## Footage audio
Keep the original ambience at gain ≈.28 under the SFX. With speed ramps, resample it through the same time map (`Mix.footage(wav, time_map)`). Slow-mo then drops in pitch like tape, which sells the effect.

## Levels
`Mix.write` normalises the peak to −0.9 dBFS through tanh. Approved films measured mean −21…−25 dB and max ≈ −2.7 dB (`ffmpeg -af volumedetect`). If the hook is too quiet (a real complaint once), raise the first 2 s of SFX gains instead of the master.

## Skeleton
```python
import sys; sys.path.insert(0, "<skill>/scripts"); import sfx
m = sfx.Mix(DUR)
m.drone(0, DUR, [110.0, 164.81, 220.0], .01)
# … events …
m.write(sys.argv[1])
```
