"""showreel_sound.py: Procedural soundtrack & SFX for 15s Motion Designer Showreel.
Generates 15.0s 48kHz stereo WAV using pure Python stdlib from motion-graphics/scripts/sfx.py.
"""
import sys
import os

# Import sfx engine from ../motion-graphics/scripts
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_scripts = os.path.abspath(os.path.join(script_dir, "..", "motion-graphics", "scripts"))
if parent_scripts not in sys.path:
    sys.path.insert(0, parent_scripts)

# pyrefly: ignore[missing-import]
import sfx

def generate_soundtrack(out_path):
    DUR = 15.0
    m = sfx.Mix(DUR)

    # ------------------------------------------------ Ambient Bed & Tension Drone
    m.drone(0.0, 15.0, [55.0, 110.0, 164.81], gain=0.016, send=0.6)
    m.drone(6.2, 12.5, [130.81, 196.0, 261.63], gain=0.008, send=0.5)

    # ------------------------------------------------ SCENE 1 (0.0s - 3.2s): THE HOOK
    # 0.0s Opening Impact: sub thump + wide air release
    m.put(0.0, sfx.kick(160, 42, 0.7, 1.8), gain=0.35, pan=0.0, send=0.35)
    m.put(0.0, sfx.whoosh(0.6, 400, 6500, 0.4), gain=0.12, pan=-0.2, send=0.3)

    # Staggered typography clicks & blips
    # "MOTION AS CODE"
    for i, t_offset in enumerate([0.15, 0.22, 0.29]):
        m.blip(t_offset, 2 + i * 2, g=0.045, pan=-0.3 + i * 0.3)
    
    # 0.85s "BUILT FOR IMPACT" punch
    m.put(0.85, sfx.kick(140, 45, 0.5, 1.5), gain=0.28, pan=0.0, send=0.25)
    m.put(0.85, sfx.zip_(0.3, up=True), gain=0.08, pan=0.2)
    for i, t_offset in enumerate([0.88, 0.95, 1.02]):
        m.blip(t_offset, 5 + i * 2, g=0.04, pan=-0.2 + i * 0.2)

    # 1.4s Serif subtitle slide
    m.put(1.4, sfx.glide(0.4, 440, 880), gain=0.03, pan=0.0)

    # 2.05s - 2.8s Stutter: Rapid pentatonic cascade + glitch ticks
    for idx, st_time in enumerate([2.05, 2.30, 2.55]):
        m.put(st_time, sfx.knock(1800 + idx * 400), gain=0.12, pan=(idx - 1) * 0.4)
        m.put(st_time, sfx.tone(440 * (idx + 1), 0.12, 0.001, 0.03, "bell"), gain=0.06, pan=(idx - 1) * 0.3)
        m.tick(st_time + 0.08, g=0.05)

    # 2.8s Suction & Gravitational collapse into center
    m.put(2.8, sfx.whoosh(0.35, 4500, 300, 0.8), gain=0.14, pan=0.0, send=0.4)

    # ------------------------------------------------ SCENE 2 (3.0s - 6.4s): 3D TOPOLOGY
    # 3.0s Explosion into 3D core
    m.put(3.0, sfx.kick(150, 38, 0.8, 2.0), gain=0.38, pan=0.0, send=0.4)
    m.put(3.0, sfx.whoosh(0.55, 300, 5000, 0.5), gain=0.12, pan=0.3, send=0.3)

    # 3D vertices spinning & Bézier calibration blips
    for k in range(12):
        t_blip = 3.2 + k * 0.22
        m.blip(t_blip, k % 10, g=0.035, pan=((k % 5) - 2) * 0.3, d=0.04)
        if k % 3 == 0:
            m.tick(t_blip + 0.05, g=0.03)

    # 4.6s Easing curve settle lock
    m.put(4.6, sfx.thud(1.2), gain=0.22, pan=0.1, send=0.25)
    m.put(4.6, sfx.tone(880, 0.25, 0.001, 0.08, "sine"), gain=0.05, pan=0.2)

    # 6.0s Tension riser into Bento scene
    m.put(5.8, sfx.riser(0.4, 220, 1200, 0.4), gain=0.16, pan=0.0)

    # ------------------------------------------------ SCENE 3 (6.2s - 9.6s): BENTO CHOREOGRAPHY
    # 6.2s Bento drop impact
    m.put(6.2, sfx.kick(130, 44, 0.6, 1.7), gain=0.32, pan=0.0, send=0.3)
    m.put(6.2, sfx.whoosh(0.4, 500, 4000, 0.4), gain=0.09, pan=-0.2)

    # Waveform scrubbing sound (continuous micro ticks)
    for w in range(16):
        t_scrub = 6.4 + w * 0.14
        m.tick(t_scrub, g=0.035, pan=-0.4 + (w / 16.0) * 0.8)

    # 7.15s Cursor click & Button State Transformation
    m.put(7.15, sfx.knock(2400), gain=0.22, pan=0.25, send=0.15)
    m.put(7.18, sfx.pop(720), gain=0.24, pan=0.25, send=0.25)
    m.put(7.20, sfx.tone(1174.66, 0.4, 0.002, 0.12, "bell"), gain=0.08, pan=0.25, send=0.5)

    # 8.4s 3D perspective tilt swoosh
    m.put(8.4, sfx.whoosh(0.5, 400, 3200, 0.5), gain=0.10, pan=0.2)

    # 9.1s Pre-surge riser & glitch
    m.glitch(9.1, 0.25, g=0.09)
    m.put(9.15, sfx.riser(0.3, 300, 1800, 0.5), gain=0.18)

    # ------------------------------------------------ SCENE 4 (9.4s - 12.6s): KINETIC SPEED SURGE
    # 9.4s Maximum velocity hit
    m.put(9.4, sfx.kick(170, 48, 0.6, 2.2), gain=0.42, pan=0.0, send=0.3)
    m.put(9.4, sfx.whoosh(0.65, 800, 8000, 0.3), gain=0.18, pan=0.1)

    # Rhythmic syncopated hits on speed strips
    for b_idx, b_time in enumerate([9.8, 10.2, 10.6, 11.0, 11.4, 11.8]):
        m.put(b_time, sfx.kick(115, 50, 0.28, 1.4), gain=0.24, pan=((b_idx % 2) * 2 - 1) * 0.2)
        m.put(b_time + 0.1, sfx.zip_(0.18, up=(b_idx % 2 == 0)), gain=0.06)

    # 10.8s Center card slam
    m.put(10.8, sfx.thud(1.4), gain=0.28, pan=0.0, send=0.3)

    # 12.0s - 12.5s Grand Climax Riser
    m.put(12.0, sfx.riser(0.52, 90, 2400, 0.6), gain=0.26)
    m.glitch(12.35, 0.15, g=0.1)

    # ------------------------------------------------ SCENE 5 (12.4s - 15.0s): GRAND FINALE
    # 12.5s Massive sub-bass drop & final brand lock
    m.put(12.5, sfx.kick(65, 24, 2.2, 2.8), gain=0.55, pan=0.0, send=0.6)
    m.put(12.5, sfx.thud(1.6), gain=0.35, pan=0.0, send=0.4)
    m.put(12.5, sfx.whoosh(0.8, 1200, 200, 0.2), gain=0.16, pan=0.0, send=0.5)

    # Heavenly resonant bell chord resolution
    chord = [261.63, 329.63, 392.0, 523.25, 659.25, 783.99]
    m.bell_chord(12.55, chord, g=0.075, dur=2.4)

    # 13.1s Subtle CTA badge snap
    m.put(13.1, sfx.knock(2100), gain=0.12, pan=0.0, send=0.2)
    m.blip(13.15, 9, g=0.05, pan=0.0, d=0.1)

    # 13.5s Gentle concluding sparkle
    m.put(13.5, sfx.tone(1046.5, 1.2, 0.005, 0.6, "sine"), gain=0.04, pan=-0.2, send=0.7)
    m.put(13.7, sfx.tone(1318.51, 1.0, 0.005, 0.5, "sine"), gain=0.035, pan=0.2, send=0.7)

    # Write final mastered audio
    m.write(out_path, reverb=0.22, fade_out=0.8)

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "showreel.wav"
    generate_soundtrack(out_file)
