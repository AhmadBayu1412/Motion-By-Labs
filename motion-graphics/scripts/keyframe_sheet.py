#!/usr/bin/env python3
"""Keyframe sheet of a rendered video: a 3-column grid of frames with scene names and time ranges.
Send it alongside the MP4. It lets people review the whole film at a glance.

    python3 keyframe_sheet.py out/film.mp4 film-keyframes.png \
        --times 0.7,2.6,4.8 --labels "Boot|Hand lock|Line code" --ranges "0–1.5|1.5–3.5|3.5–6.9" \
        --kicker "brand · 20 s · 60 fps" --title "Labs<b>.</b> <i>make things move.</i>" --theme dark --accent "#2E5BFF"

--title accepts inline HTML: <b> is coloured with the accent, <i> is Instrument Serif italic.
Use 9 or 12 frames, picked at each scene's most readable moment (text fully in, not mid-transition).
"""
import argparse, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__)); FONTS = os.path.join(HERE, "..", "assets", "fonts")
ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("out"); ap.add_argument("--times", required=True); ap.add_argument("--labels", default=""); ap.add_argument("--ranges", default="")
ap.add_argument("--title", default=""); ap.add_argument("--kicker", default=""); ap.add_argument("--note", default=""); ap.add_argument("--theme", default="light"); ap.add_argument("--accent", default="#2E5BFF")
ap.add_argument("--cols", type=int, default=3)
a = ap.parse_args()
times = a.times.split(","); labels = a.labels.split("|") if a.labels else [""] * len(times); ranges = a.ranges.split("|") if a.ranges else times
d = tempfile.mkdtemp(prefix="sheet-"); os.makedirs(os.path.join(d, "fonts"))
for f in os.listdir(FONTS):
    if f.endswith(".woff2"): shutil.copy(os.path.join(FONTS, f), os.path.join(d, "fonts", f))
for i, t in enumerate(times):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", t, "-i", a.video, "-frames:v", "1", "-vf", "scale=960:-1", os.path.join(d, f"k{i}.png")], check=True)
dark = a.theme == "dark"; bg, fg, mut, bd = ("#07080D", "#F4F6FB", "#8D93A8", "#ffffff1a") if dark else ("#F4F4F2", "#0E0F12", "#8C8C88", "#0000001a")
cells = "".join(f'<div class="c"><img src="k{i}.png"><div class="h"><b>{labels[i] if i < len(labels) else ""}</b><span class="mono">{ranges[i] if i < len(ranges) else ""}</span></div></div>' for i in range(len(times)))
html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:G;src:url(fonts/Geist-normal.woff2) format("woff2");font-weight:100 900}}
@font-face{{font-family:GM;src:url(fonts/GeistMono-normal.woff2) format("woff2");font-weight:100 900}}
@font-face{{font-family:IS;src:url(fonts/InstrumentSerif-italic.woff2) format("woff2");font-style:italic}}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1920px;background:{bg};color:{fg};font-family:G;padding:60px 72px 64px;-webkit-font-smoothing:antialiased}}
h1{{font-size:60px;font-weight:800;letter-spacing:-.045em;line-height:1.05}}h1 b{{color:{a.accent}}}h1 i{{font-family:IS;font-weight:400;font-size:.9em;letter-spacing:0;margin-left:12px}}
.mono{{font-family:GM;text-transform:uppercase;letter-spacing:.16em;font-size:13px;color:{mut}}}
.top{{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:34px}}
.g{{display:grid;grid-template-columns:repeat({a.cols},1fr);gap:30px 26px}}.c img{{width:100%;display:block;border-radius:10px;border:1px solid {bd}}}
.c .h{{display:flex;justify-content:space-between;margin-top:12px;gap:12px}}.c b{{font-size:20px;font-weight:650;letter-spacing:-.02em}}
</style></head><body><div class="top"><div><div class="mono" style="margin-bottom:12px">{a.kicker}</div><h1>{a.title}</h1></div><div class="mono">{a.note}</div></div>
<div class="g">{cells}</div><script>document.fonts.ready.then(()=>Promise.all([...document.images].map(i=>i.decode()))).then(()=>window.ready=true)</script></body></html>'''
open(os.path.join(d, "sheet.html"), "w").write(html)
r = subprocess.run(["node", os.path.join(HERE, "shot.mjs"), d, "sheet.html", os.path.abspath(a.out)])
shutil.rmtree(d, ignore_errors=True); sys.exit(r.returncode)
