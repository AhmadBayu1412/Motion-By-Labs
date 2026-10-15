#!/usr/bin/env bash
# Replace a time range of a rendered film with a re-render, frame-accurately, and re-mux the audio.
#
#   node render.mjs --page film.html --name fix --from 5 --to 8 --noaudio      # → out/fix.mp4 (3 s)
#   bash splice.sh out/film.mp4 out/fix.mp4 5 8 out/film.wav out/film-final.mp4 [fps=60]
#
# Why a single filter graph: cutting parts with `select` and joining them with the concat demuxer
# shifted timestamps (≈2 s late in one case) because the parts' durations rounded to 5.04 s / 21.04 s.
# trim by frame number + concat filter in ONE ffmpeg call is exact.
# Always verify afterwards: extract a frame inside the patched range and compare it with the fix render.
set -euo pipefail
FULL="$1"; FIX="$2"; FROM="$3"; TO="$4"; WAV="$5"; OUT="$6"; FPS="${7:-60}"
A=$(python3 -c "print(round($FROM*$FPS))"); B=$(python3 -c "print(round($TO*$FPS))"); N=$((B-A))
ffmpeg -v error -y -i "$FULL" -i "$FIX" -i "$WAV" -filter_complex \
 "[0:v]trim=start_frame=0:end_frame=$A,setpts=PTS-STARTPTS[a];[1:v]trim=end_frame=$N,setpts=PTS-STARTPTS[b];[0:v]trim=start_frame=$B,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0,fps=$FPS[v]" \
 -map "[v]" -map 2:a -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
ffmpeg -i "$OUT" 2>&1 | grep -E "Duration" || true
