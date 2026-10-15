# Motion By Labs: skill `motion-graphics`

Skill Claude untuk membuat video motion graphics dari kode. Hasilnya brand reel, video promosi/explainer, logo reveal, kinetic typography, isometric 3D, pixel brand film, HUD sensor AI di atas footage (hand tracking asli), sampai edit absurd bertema kode.

Setiap video adalah satu halaman HTML deterministik yang dirender ke MP4 60 fps, dengan motion blur asli dan sound design prosedural (tanpa sampel, tanpa musik berlisensi).

## Isi
- `motion-graphics/SKILL.md`: alur kerja (brief → storyboard → ACC → build → cek still → sound → render → kirim) dan prinsip desain.
- `motion-graphics/references/`: katalog 9 gaya, bahasa gerak (easing, tempo, kamera, transisi), sound design, footage + HUD sensor, storyboard, dan daftar jebakan.
- `motion-graphics/scripts/`: renderer, `sfx.py`, analisis video referensi, persiapan footage HDR, tracking tangan/objek, lembar keyframe, splice.
- `motion-graphics/assets/`: template halaman, kit HUD sensor, font OFL.

## Pasang
- **Claude Code (per proyek):** salin folder `motion-graphics/` ke `.claude/skills/` di repo proyekmu.
- **Claude Code (semua proyek):** salin ke `~/.claude/skills/`.
- **Claude.ai:** unggah `motion-graphics.skill` lewat Settings → Capabilities → Skills.

## Kebutuhan
Node 18+ dengan Playwright (Chromium), ffmpeg, Python 3. Untuk tracking footage juga perlu `pip install mediapipe`.
