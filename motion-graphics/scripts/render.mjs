// Deterministic HTML → MP4 renderer with real sub-frame motion blur and muxed procedural audio.
//
// The page must expose (see assets/template.html):
//   window.DURATION   seconds
//   window.renderAt(t) draws the frame at time t (may be async / return a Promise)
//   window.reelReady   a Promise that resolves when fonts/images/data are loaded
// The page is opened as  http://127.0.0.1:<port>/<page>?capture  from a local static server rooted at --root.
//
//   node render.mjs --page film.html --name film-20s --sound film_sound.py --sub 3
//   node render.mjs --page film.html --name f --stills 0.5,3.2,7.9     # PNG previews → <root>/out/f-<t>.png
//   node render.mjs --page film.html --name film-20s --from 5 --to 8 --noaudio   # re-render a range (splice later)
//
// Options: --root <dir> (default cwd)  --width 1920 --height 1080  --fps 60  --sub 3 (blur samples/frame)
//          --shutter 0.5  --workers 4  --crf 18  --sound <script.py> (run as: python3 <script> <out.wav>)
// Needs Playwright (Chromium) and ffmpeg on PATH (or FFMPEG=/path/to/ffmpeg).
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { spawnSync } from "node:child_process";
import { createRequire } from "node:module";

const args = Object.fromEntries(process.argv.slice(2).reduce((acc, a, i, arr) =>
  a.startsWith("--") ? [...acc, [a.slice(2), arr[i + 1] && !arr[i + 1].startsWith("--") ? arr[i + 1] : true]] : acc, []));
const ROOT = path.resolve(args.root || process.cwd()), OUT = path.join(ROOT, "out");
const FPS = +(args.fps || 60), SUB = +(args.sub || 3), SHUTTER = +(args.shutter || 0.5), CRF = String(args.crf || 18);
const WORKERS = +(args.workers || Math.max(1, Math.min(4, os.cpus().length)));
const FFMPEG = process.env.FFMPEG || "ffmpeg";
const PAGE = args.page || "index.html", W = +(args.width || 1920), H = +(args.height || 1080);
const NAME = args.name || path.basename(PAGE, ".html");
if (!fs.existsSync(path.join(ROOT, PAGE))) { console.error(`page not found: ${path.join(ROOT, PAGE)} (use --root)`); process.exit(1); }

async function loadPlaywright() {
  for (const id of ["playwright", "@playwright/test"]) { try { return (await import(id)).chromium; } catch {} }
  const req = createRequire(import.meta.url);
  const globalRoot = spawnSync("npm", ["root", "-g"], { encoding: "utf8" }).stdout.trim();
  return req(path.join(globalRoot, "playwright")).chromium;
}

const MIME = { ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".json": "application/json", ".css": "text/css",
  ".woff2": "font/woff2", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml", ".webp": "image/webp", ".mp4": "video/mp4", ".webm": "video/webm" };
function serve() {
  const srv = http.createServer((req, res) => {
    const p = path.join(ROOT, decodeURIComponent(new URL(req.url, "http://x").pathname));
    if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { "content-type": MIME[path.extname(p).toLowerCase()] || "application/octet-stream" });
    fs.createReadStream(p).pipe(res);
  });
  return new Promise(r => srv.listen(0, "127.0.0.1", () => r(srv)));
}

async function openPage(browser, port) {
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  page.on("pageerror", e => console.error("page error:", e.message));
  await page.goto(`http://127.0.0.1:${port}/${PAGE}?capture`);
  // module pages may only set reelReady after top-level awaits (fetch, fonts) — wait for it to exist, then for it to resolve
  await page.waitForFunction(() => window.reelReady !== undefined, null, { timeout: 120000 });
  await page.evaluate(() => window.reelReady);
  return page;
}

const chromium = await loadPlaywright();
const srv = await serve();
const port = srv.address().port;
// swiftshader keeps WebGL (three.js) working headless
const browser = await chromium.launch({ args: ["--force-color-profile=srgb", "--disable-lcd-text", "--enable-unsafe-swiftshader"] });
fs.mkdirSync(OUT, { recursive: true });

if (args.stills) {
  const page = await openPage(browser, port);
  for (const s of String(args.stills).split(",")) {
    await page.evaluate(t => window.renderAt(t), +s);
    await page.screenshot({ path: path.join(OUT, `${NAME}-${(+s).toFixed(2)}.png`) });
  }
  console.log("stills written to", OUT);
} else {
  const dur = await (await openPage(browser, port)).evaluate(() => window.DURATION);
  const frames = Math.round(dur * FPS);
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "reel-"));
  const f0 = args.from ? Math.round(+args.from * FPS) : 0, f1 = args.to ? Math.round(+args.to * FPS) : frames;
  const jobs = [];
  for (let f = f0; f < f1; f++) for (let s = 0; s < SUB; s++) jobs.push({ i: (f - f0) * SUB + s, t: (f + (SUB > 1 ? s / SUB * SHUTTER - SHUTTER / 2 : 0)) / FPS });
  let done = 0; const t0 = Date.now();
  await Promise.all([...Array(WORKERS)].map(async (_, w) => {
    const page = await openPage(browser, port);
    for (let j = w; j < jobs.length; j += WORKERS) {
      await page.evaluate(t => window.renderAt(Math.max(0, t)), jobs[j].t);
      await page.screenshot({ path: path.join(tmp, `f${String(jobs[j].i).padStart(6, "0")}.jpg`), type: "jpeg", quality: 96 });
      if (++done % 200 === 0) process.stdout.write(`\r${done}/${jobs.length} samples  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
  }));
  console.log(`\ncaptured ${jobs.length} samples; encoding…`);
  // average each group of SUB samples into one frame (= motion blur), then encode H.264
  const blur = SUB > 1 ? `tmix=frames=${SUB},select='eq(mod(n\\,${SUB})\\,${SUB - 1})',setpts=N/${FPS}/TB,` : "";
  const mp4 = path.join(OUT, `${NAME}.mp4`);
  const wav = path.join(OUT, `${NAME}.wav`);
  // regenerate every time so the audio never goes stale after a retime (stdlib synthesis takes seconds)
  if (args.sound && !args.noaudio) spawnSync("python3", [path.resolve(ROOT, args.sound), wav], { stdio: "inherit", cwd: ROOT });
  const audio = !args.noaudio && fs.existsSync(wav) ? ["-i", wav, "-c:a", "aac", "-b:a", "256k", "-shortest"] : [];
  const r = spawnSync(FFMPEG, ["-y", "-loglevel", "error", "-framerate", String(FPS * SUB), "-i", path.join(tmp, "f%06d.jpg"), ...audio.slice(0, 2),
    "-vf", `${blur}format=yuv420p`, "-r", String(FPS), "-c:v", "libx264", "-preset", "slow", "-crf", CRF,
    "-profile:v", "high", ...audio.slice(2), "-movflags", "+faststart", mp4], { stdio: "inherit" });
  if (r.status !== 0) process.exitCode = 1; else console.log("wrote", mp4);
  fs.rmSync(tmp, { recursive: true, force: true });
}
await browser.close();
srv.close();
