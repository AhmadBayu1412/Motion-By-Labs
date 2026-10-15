#!/usr/bin/env python3
"""Study a reference video before storyboarding: contact sheets, hard-cut times, and audio rhythm.

    python3 analyze_reference.py ref.mp4 out/ref [--fps 2] [--hi 0.8,4.2,9.0]

Writes:
  <out>/sheet0.png …   6×4 contact sheets (one tile every 1/fps s; tile k = t ≈ k/fps)
  <out>/hi.png         large frames at the --hi times (for details: type, UI, textures)
Prints: duration/fps/size, scene cuts (ffmpeg scene > .25), audio onsets and their most common
intervals. Intervals near 60/BPM mean the cut is music-led. Dense onsets every .25–.35 s with
irregular gaps mean it is SFX-led.
Look at the sheets yourself afterwards (Read the PNGs). The numbers alone don't describe the style.
"""
import argparse, os, re, struct, subprocess, sys
from collections import Counter

ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("out"); ap.add_argument("--fps", type=float, default=2); ap.add_argument("--hi", default="")
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
run = lambda *c: subprocess.run(c, capture_output=True, text=True)
info = run("ffmpeg", "-i", a.video).stderr
print("\n".join(l.strip() for l in info.splitlines() if re.search(r"Duration|Stream.*(Video|Audio)", l)))
if re.search(r"arib-std-b67|smpte2084", info): print("NOTE: HDR source (HLG/PQ) — tonemap before using frames (see prep_footage.sh)")

# contact sheets
fr = os.path.join(a.out, "f%04d.png")
run("ffmpeg", "-v", "error", "-y", "-i", a.video, "-vf", f"fps={a.fps},scale=320:-1", fr)
n = len([f for f in os.listdir(a.out) if re.match(r"f\d{4}\.png", f)])
for k in range(0, n, 24):
    run("ffmpeg", "-v", "error", "-y", "-start_number", str(k + 1), "-i", fr, "-frames:v", "1", "-vf", "tile=6x4:padding=4:color=red", os.path.join(a.out, f"sheet{k // 24}.png"))
print(f"{n} tiles → {(n + 23) // 24} sheets in {a.out} (tile i ≈ t={1 / a.fps:.2f}·(i-1) s)")
if a.hi:
    for i, t in enumerate(a.hi.split(",")):
        run("ffmpeg", "-v", "error", "-y", "-ss", t, "-i", a.video, "-frames:v", "1", "-vf", "scale=640:-1", os.path.join(a.out, f"hi{i}.png"))
    run("ffmpeg", "-v", "error", "-y", "-i", os.path.join(a.out, "hi%d.png"), "-frames:v", "1", "-vf", "tile=4x2", os.path.join(a.out, "hi.png"))

# hard cuts
cuts = re.findall(r"pts_time:([\d.]+)", run("ffmpeg", "-i", a.video, "-vf", "select='gt(scene,0.25)',showinfo", "-an", "-f", "null", "-").stderr)
print("scene cuts:", " ".join(f"{float(c):.2f}" for c in cuts) or "none (continuous / morph-based)")

# audio onsets (energy jumps, 50 ms windows)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout
if raw:
    s = struct.unpack("<%dh" % (len(raw) // 2), raw); w = 400
    e = [sum(abs(x) for x in s[i:i + w]) / w for i in range(0, len(s) - w, w)]; on = []
    for i in range(2, len(e)):
        if e[i] > 1.8 * e[i - 1] + 300 and e[i] > 1500 and (not on or i * .05 - on[-1] > .18): on.append(round(i * .05, 2))
    iv = [round(b - a_, 2) for a_, b in zip(on, on[1:])]
    print(f"audio onsets: {len(on)} in {len(e) * .05:.1f}s (≈{len(on) / max(1, len(e) * .05):.1f}/s)")
    print("most common intervals:", Counter(iv).most_common(6))
else:
    print("no audio stream")
