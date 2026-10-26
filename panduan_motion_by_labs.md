# 🎬 Panduan Motion-By-Labs — Cara Bikin Video Sendiri

## Konsep Dasar

Project ini mengubah **halaman HTML biasa** menjadi **video MP4 berkualitas broadcast** (1920×1080, 60fps, motion blur). Semua animasi ditulis sebagai kode — murni fungsi dari waktu `t`. Tidak pakai After Effects, tidak pakai Premiere.

```
HTML page (renderAt(t)) → Playwright captures frames → FFmpeg encodes → MP4 + WAV audio
```

> [!IMPORTANT]
> Setiap video = **1 folder** berisi: `index.html` (animasi), `*_sound.py` (audio), dan folder `fonts/`.

---

## Arsitektur Project

```
Motion-By-Labs/
├── motion-graphics/          # 🧠 Engine & toolkit
│   ├── scripts/
│   │   ├── render.mjs        # HTML → MP4 renderer
│   │   ├── sfx.py            # Procedural audio library
│   │   ├── shot.mjs          # Screenshot utility
│   │   └── ...
│   ├── assets/
│   │   ├── template.html     # ⭐ Starting point untuk video baru
│   │   ├── fonts/            # Font bundle (Geist, Syne, Anton, dll)
│   │   └── vision-hud.js     # HUD overlay kit
│   └── references/           # Dokumentasi style & teknik
│       ├── styles.md         # 9 style yang sudah proven
│       ├── motion-language.md # Timing, easing, transisi
│       ├── sound.md          # Panduan sound design
│       └── gotchas.md        # Kesalahan umum
├── reel/                     # 🎥 Video showreel yang baru dibuat
│   ├── index.html
│   ├── showreel_sound.py
│   ├── fonts/
│   └── out/
│       ├── showreel.mp4
│       └── showreel.wav
```

---

## Cara Bikin Video Baru (Step by Step)

### Step 1: Buat Folder Baru

```powershell
mkdir c:\Users\ThinkPad\Desktop\Motion-By-Labs\video-baru
```

### Step 2: Copy Font & Template

```powershell
# Copy fonts
Copy-Item -Recurse motion-graphics\assets\fonts video-baru\fonts

# Copy template sebagai starting point
Copy-Item motion-graphics\assets\template.html video-baru\index.html
```

### Step 3: Edit `index.html`

Buka [template.html](file:///c:/Users/ThinkPad/Desktop/Motion-By-Labs/motion-graphics/assets/template.html) — ini sudah punya semua helper yang kamu butuhkan:

#### 3 Hal Wajib yang Harus Di-expose:

```javascript
window.DURATION = 10;              // durasi video (detik)
window.renderAt = renderAt;        // fungsi yang menggambar frame di waktu t
window.reelReady = (async () => {  // Promise: siap setelah font/data loaded
  await document.fonts.ready;
  renderAt(0);
  return true;
})();
```

#### Helper Bawaan Template:

| Helper | Kegunaan | Contoh |
|---|---|---|
| `seg(t, a, b)` | Progress 0→1 dari waktu `a` ke `b` | `seg(t, 1.0, 2.5)` → 0 di 1s, 0.5 di 1.75s, 1 di 2.5s |
| `ex(p)` | Expo-out easing (snap cepat, lalu pelan) | `ex(seg(t, 1, 2))` |
| `spring(p)` | Bounce/overshoot easing | `spring(seg(t, 1, 2))` |
| `mix(a, b, p)` | Linear interpolation | `mix(0, 100, p)` → 0 sampai 100 |
| `Lay(id, a, b, t)` | Tampilkan layer dari waktu a sampai b | `Lay("S1", 0, 3, t)` |
| `words(el, text)` | Split teks jadi per-kata untuk animasi | `words($("t1"), "Hello *World")` |
| `reveal(ws, t, t0)` | Animasi kata muncul satu-satu | `reveal(W1, t, 0.5, 0.07)` |
| `cam(t)` | Camera punch + shake | Auto dari array `PUNCH` |
| `hash(n)` | Deterministic random (bukan Math.random!) | `hash(42)` → 0.38... |

#### Contoh Scene Sederhana:

```javascript
const DURATION = 8;

function renderAt(t) {
  // Scene 1: Teks muncul (0-3s)
  if (Lay("S1", 0, 3.2, t)) {
    reveal(W1, t, 0.2, 0.07, 2.8);  // kata muncul mulai 0.2s, keluar di 2.8s
  }

  // Scene 2: Card masuk (2.8-6s)
  if (Lay("S2", 2.8, 6.2, t)) {
    const k = spring(seg(t, 2.9, 3.5));  // spring masuk
    $("card").style.transform = `translateY(${(1-k) * 400}px) scale(${0.8 + 0.2*k})`;
  }

  // Scene 3: Logo finale (6-8s)
  if (Lay("S3", 5.9, DURATION, t)) {
    const k = ex(seg(t, 6.0, 6.8));
    $("logo").style.opacity = k;
    $("logo").style.transform = `scale(${0.5 + 0.5*k})`;
  }

  // Camera punch
  const c = cam(t);
  $("world").style.transform = `translate(${c.x}px,${c.y}px) scale(${c.s})`;
}
```

### Step 4: Preview Stills (Cek Dulu Sebelum Render Penuh)

```powershell
node motion-graphics/scripts/render.mjs --root video-baru --page index.html --name preview --stills 0.5,2.0,4.0,6.0,7.5
```

Hasilnya ada di `video-baru/out/preview-*.png` — **cek** sebelum render penuh.

### Step 5: Bikin Sound Script

Buat `video-baru/video_sound.py` menggunakan library [sfx.py](file:///c:/Users/ThinkPad/Desktop/Motion-By-Labs/motion-graphics/scripts/sfx.py):

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'motion-graphics', 'scripts'))
from sfx import Mix, kick, whoosh, riser, blip, bell_chord, knock

DUR = 8.0  # sama dengan DURATION di HTML
m = Mix(DUR)

# Sync sound ke visual events
m.add(0.15, kick())          # saat kata pertama muncul
m.add(2.9,  kick(mid=90))    # saat card masuk
m.add(2.85, whoosh())        # whoosh sebelum card
m.add(6.0,  bell_chord())    # saat logo muncul
m.add(0.0,  riser(DUR))      # riser sepanjang video

m.write(sys.argv[1])
```

### Step 6: Render MP4

```powershell
$env:FFMPEG = "C:\Users\ThinkPad\.antigravity-ide\extensions\.5716d6d0-1b8a-4d86-b679-edfeb4f059c7\bin\ffmpeg.exe"
node motion-graphics/scripts/render.mjs --root video-baru --page index.html --name video-baru --sound video_sound.py --sub 3
```

> [!TIP]
> `--sub 3` = motion blur 3 sample. Pakai `--sub 1` untuk render cepat tanpa blur (preview). `--sub 2` untuk footage/WebGL.

Output: `video-baru/out/video-baru.mp4`

---

## Opsi Render yang Tersedia

| Flag | Default | Kegunaan |
|---|---|---|
| `--root <dir>` | cwd | Folder root video |
| `--page <file>` | index.html | File HTML utama |
| `--name <name>` | dari page | Nama output |
| `--fps 60` | 60 | Frame per second |
| `--sub 3` | 3 | Motion blur samples per frame |
| `--shutter 0.5` | 0.5 | Shutter angle |
| `--width 1920` | 1920 | Lebar pixel |
| `--height 1080` | 1080 | Tinggi pixel |
| `--crf 18` | 18 | H.264 quality (lower = better) |
| `--workers 4` | CPU count | Parallel capture threads |
| `--sound <script.py>` | - | Audio script (relative to root) |
| `--stills 0.5,2.0,...` | - | Screenshot mode (PNG previews) |
| `--from 5 --to 8` | - | Render hanya range tertentu |
| `--noaudio` | - | Skip audio |

---

## 9 Style yang Sudah Proven

Kamu bisa pakai atau mix dari style-style ini (detail lengkap di [styles.md](file:///c:/Users/ThinkPad/Desktop/Motion-By-Labs/motion-graphics/references/styles.md)):

| # | Style | Cocok Untuk |
|---|---|---|
| 1 | **Editorial Cream** | Brand premium, service promo |
| 2 | **Monochrome Studio** | Portfolio, lab showcase |
| 3 | **Isometric 3D Build** | Product story, 3D (three.js) |
| 4 | **Soft-Cyber Bento** | Tech/neon, dark mode |
| 5 | **SaaS Explainer** | Startup, product demo |
| 6 | **Pixel Brand Film** | Brand film minimalis |
| 7 | **Sensor HUD** | Real footage + AI/tracking |
| 8 | **Absurd Code Editor** | Humor, meme, experimental |
| 9 | **Kinetic Poster** | Typography-driven reel |

---

## Aturan Penting

> [!CAUTION]
> **Jangan pakai** `Math.random()` — pakai `hash(n)` untuk deterministic random.
> **Jangan pakai** CSS transitions/animations — semua harus dari `renderAt(t)`.
> **Jangan pakai** `requestAnimationFrame` state — halaman harus bisa di-render di waktu `t` manapun secara independen.

Baca [gotchas.md](file:///c:/Users/ThinkPad/Desktop/Motion-By-Labs/motion-graphics/references/gotchas.md) sebelum build untuk menghindari error render.

---

## Cara Paling Gampang: Minta AI 🤖

Kamu tidak perlu coding sendiri! Cukup bilang ke saya:

- *"Bikin video promo untuk brand X, warna biru-putih, 10 detik"*
- *"Bikin motion kinetic typography bertuliskan [teks kamu]"*
- *"Bikin video seperti referensi ini [kirim video/screenshot]"*
- *"Ubah showreel tadi, ganti teksnya jadi [teks baru]"*
- *"Bikin video dari footage saya dengan efek HUD tracking"*

Saya akan buatkan HTML + sound script + render jadi MP4 sesuai keinginanmu. 🚀

### Cara Kerja dengan Referensi Video

1. **Kirim video referensinya** ke saya (file video atau link)
2. Saya akan **analisis** pakai [`analyze_reference.py`](file:///c:/Users/ThinkPad/Desktop/Motion-By-Labs/motion-graphics/scripts/analyze_reference.py) — ini otomatis mengekstrak:
   - **Contact sheet** (thumbnails setiap scene)
   - **Hard cuts** (deteksi transisi antar scene)
   - **Audio onset rhythm** (timing beat musik/SFX)
3. Dari analisis itu, saya **describe** canvas, transisi, ritme, tipografi, dan audio dari referensi
4. Lalu saya **build** video baru yang mengikuti grammar/style referensi itu, tapi dengan **materi/brand kamu sendiri**

### Yang Bisa Kamu Kirim:

| Input | Contoh |
|---|---|
| **File video** | `.mp4`, `.mov`, `.webm` |
| **Screenshot/frame** | Screenshot dari reel IG yang kamu suka |
| **Link** | Link YouTube/Instagram |
| **Deskripsi** | "seperti video Apple product launch, tapi warna hitam-emas" |

### Contoh Prompt yang Bagus:

> *"Bikin video promo 15 detik untuk brand [X] dengan style seperti video referensi ini. Warna brand: biru #2E5BFF, font: Geist. Teksnya: [isi teks]."*

Jadi tinggal kirim referensinya + materi brand kamu, saya yang urus sisanya! 🚀