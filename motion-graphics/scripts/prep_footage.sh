#!/usr/bin/env bash
# Prepare real footage for an HTML motion page: SDR proxy (tonemapped if HDR), 60 fps JPEG frames, original audio.
#
#   bash prep_footage.sh IMG_7829.MOV out/            → out/sdr.mp4, out/vframes/f0001.jpg…, out/footage.wav
#
# iPhone clips are usually HDR (HLG, BT.2020, 10-bit). Without tonemapping they look grey and washed out in
# Chromium and on Instagram. Frames are numbered from 1; frame for footage time f is f%04d with index round(f*60)+1.
# Keep the frames out of git (put them under out/, which should be gitignored).
set -euo pipefail
SRC="$1"; OUT="${2:-out}"; mkdir -p "$OUT/vframes"
INFO=$(ffmpeg -hide_banner -i "$SRC" 2>&1 || true)
if echo "$INFO" | grep -qE "arib-std-b67|smpte2084"; then
  echo "HDR source → tonemapping to SDR BT.709"
  VF="zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0:peak=4,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=saturation=1.08:contrast=1.04"
else
  VF="format=yuv420p"
fi
ffmpeg -v error -y -i "$SRC" -map 0:v:0 -vf "$VF" -c:v libx264 -crf 14 -preset fast -r 60 "$OUT/sdr.mp4"
ffmpeg -v error -y -i "$OUT/sdr.mp4" -q:v 3 "$OUT/vframes/f%04d.jpg"
ffmpeg -v error -y -i "$SRC" -map 0:a:0 -ac 2 -ar 48000 "$OUT/footage.wav" 2>/dev/null || echo "(no audio track)"
echo "frames: $(ls "$OUT/vframes" | wc -l) · $(du -sh "$OUT/vframes" | cut -f1)"
