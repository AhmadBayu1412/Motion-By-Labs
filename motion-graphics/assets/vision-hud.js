// LABS.VISION — sensor HUD drawn on top of real footage from MediaPipe hand landmarks (assets/vision/track.json).
// All drawing happens in 1920×1080 space; callers scale the context for smaller previews.
// Shared by labs-vision-board.html (storyboard / metric design sheet) and the final video page.

export const ACC = "#2E5BFF", ACC2 = "#7FA0FF", INK = "#0B0D14", WHITE = "#F4F6FB";
export const W = 1920, H = 1080;
const BONES = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 5], [5, 6], [6, 7], [7, 8], [5, 9], [9, 10], [10, 11], [11, 12], [9, 13], [13, 14], [14, 15], [15, 16], [13, 17], [17, 18], [18, 19], [19, 20], [0, 17]];
const TIPS = [4, 8, 12, 16, 20];
const TOKENS = ["const", "hand", "=", "track(", "x:", "0.42", "y:", "0.61", ")", "spring(", "{", "mass:", "1", "}", "<Sequence>", "from={12}", "ease.out", "=>", "frame", "++", "render()", "fps:60", "if(", "pinch", ")", "move()", "</>", "λ", "0x2E5B", "vec3", "lerp(", "t", ")", ";"];

// ------------------------------------------------------------------ track data
export function loadTrack(json) {
  const fps = json.fps, F = json.frames.map(hs => hs.map(h => h.p.map(([x, y, z]) => [x * W, y * H, z])));
  // keep the dominant hand per frame (largest), smooth with neighbours to kill jitter
  const main = F.map(hs => hs.length ? hs.reduce((a, b) => span(b) > span(a) ? b : a) : null);
  const sm = main.map((h, i) => {
    if (!h) return null;
    const nb = [main[i - 1], h, h, main[i + 1]].filter(Boolean);
    return h.map((_, k) => [0, 1, 2].map(c => nb.reduce((s, n) => s + n[k][c], 0) / nb.length));
  });
  const conf = json.frames.map(hs => hs.length ? Math.max(...hs.map(h => h.s)) : 0);
  return { fps, hands: sm, conf, n: sm.length };
}
function span(h) { const xs = h.map(p => p[0]), ys = h.map(p => p[1]); return (Math.max(...xs) - Math.min(...xs)) * (Math.max(...ys) - Math.min(...ys)); }

// hand at time t (linear interpolation between 30 fps samples); null when not tracked
export function handAt(T, t) {
  const f = t * T.fps, i = Math.floor(f), a = T.hands[i], b = T.hands[i + 1], u = f - i;
  if (!a) return null; if (!b) return a;
  return a.map((p, k) => [p[0] + (b[k][0] - p[0]) * u, p[1] + (b[k][1] - p[1]) * u, p[2] + (b[k][2] - p[2]) * u]);
}
// how long the hand has been continuously tracked at t (for lock-on animations)
export function lockAge(T, t) { let i = Math.floor(t * T.fps), n = 0; while (i >= 0 && T.hands[i]) { i--; n++; } return n / T.fps; }
export function lostAge(T, t) { let i = Math.floor(t * T.fps), n = 0; while (i >= 0 && !T.hands[i]) { i--; n++; } return n / T.fps; }

export function metrics(T, t) {
  const h = handAt(T, t); if (!h) return null;
  const p = handAt(T, Math.max(0, t - 1 / 15)) || h;
  const vel = Math.hypot(h[0][0] - p[0][0], h[0][1] - p[0][1]) * 15;
  const d = (a, b) => Math.hypot(h[a][0] - h[b][0], h[a][1] - h[b][1]);
  const palm = d(0, 9) || 1, spread = Math.min(1, (d(4, 8) + d(8, 12) + d(12, 16) + d(16, 20)) / palm / 2.6);
  const curl = [8, 12, 16, 20].reduce((s, k) => s + d(k, 0) / palm, 0) / 4;           // ~1.9 open, ~1 fist
  const a1 = Math.atan2(h[4][1] - h[2][1], h[4][0] - h[2][0]), a2 = Math.atan2(h[8][1] - h[5][1], h[8][0] - h[5][0]);
  let ang = Math.abs(a1 - a2) * 180 / Math.PI; if (ang > 180) ang = 360 - ang;
  const pinch = d(4, 8) / palm;
  const g = { OPEN: clamp((curl - 1.25) / .6) * clamp(spread * 1.4), FIST: clamp((1.45 - curl) / .5), PINCH: clamp((.45 - pinch) / .35), POINT: clamp((d(8, 0) / palm - 1.4) / .5) * clamp((1.5 - d(12, 0) / palm) / .5) };
  const xs = h.map(q => q[0]), ys = h.map(q => q[1]);
  const box = [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)];
  return { h, vel, spread, curl, ang, pinch, g, box, conf: T.conf[Math.floor(t * T.fps)] || 0 };
}
const clamp = x => Math.max(0, Math.min(1, x));
export const gestureName = g => Object.entries(g).sort((a, b) => b[1] - a[1])[0][0];

// ------------------------------------------------------------------ primitives
function glow(ctx, c = ACC, b = 14) { ctx.shadowColor = c; ctx.shadowBlur = b; }
function noGlow(ctx) { ctx.shadowBlur = 0; }
export function mono(ctx, s, x, y, size = 15, col = WHITE, align = "left", weight = 500) {
  ctx.font = `${weight} ${size}px "Geist Mono", monospace`; ctx.letterSpacing = "0px"; ctx.textAlign = align; ctx.textBaseline = "alphabetic"; ctx.fillStyle = col; ctx.fillText(s, x, y);
}
export function tab(ctx, s, x, y, bg = ACC, fg = "#fff", size = 15) {
  ctx.font = `600 ${size}px "Geist Mono", monospace`; ctx.letterSpacing = "0px"; const w = ctx.measureText(s).width + 18, h = size + 13;
  ctx.fillStyle = bg; ctx.fillRect(x, y - h, w, h); ctx.fillStyle = fg; ctx.textAlign = "left"; ctx.textBaseline = "middle"; ctx.fillText(s, x + 9, y - h / 2 + 1); ctx.textBaseline = "alphabetic"; return w;
}

// footage grade + vignette + scanlines (call after drawing the frame)
export function grade(ctx, k = 1) {
  ctx.save(); ctx.globalCompositeOperation = "multiply"; ctx.fillStyle = `rgba(150,165,205,${.42 * k})`; ctx.fillRect(0, 0, W, H);
  ctx.globalCompositeOperation = "source-over"; const g = ctx.createRadialGradient(960, 540, 300, 960, 540, 1150);
  g.addColorStop(0, "rgba(5,8,20,0)"); g.addColorStop(1, `rgba(5,8,20,${.62 * k})`); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = `rgba(0,0,0,${.07 * k})`; for (let y = 0; y < H; y += 4) ctx.fillRect(0, y, W, 1); ctx.restore();
}

// ------------------------------------------------------------------ hand layers
// reveal: 0→1 lock-on (landmarks pop in order, bones draw), a: overall alpha
export function drawHand(ctx, m, { reveal = 1, a = 1, ids = true, mesh = true, label = "HAND_01", t = 0 } = {}) {
  if (!m) return; const h = m.h; ctx.save(); ctx.globalAlpha = a;
  if (mesh) { ctx.fillStyle = "rgba(46,91,255,.16)"; ctx.beginPath(); [0, 1, 5, 9, 13, 17].forEach((k, i) => i ? ctx.lineTo(h[k][0], h[k][1]) : ctx.moveTo(h[k][0], h[k][1])); ctx.closePath(); ctx.fill();
    ctx.strokeStyle = "rgba(127,160,255,.35)"; ctx.lineWidth = 1; [[0, 9], [1, 5], [5, 13], [9, 17], [0, 13]].forEach(([p, q]) => { ctx.beginPath(); ctx.moveTo(h[p][0], h[p][1]); ctx.lineTo(h[q][0], h[q][1]); ctx.stroke(); }); }
  // bones
  glow(ctx, ACC, 18); ctx.strokeStyle = WHITE; ctx.lineWidth = 3.2; ctx.lineCap = "round";
  BONES.forEach(([p, q], i) => { const r = clamp(reveal * 1.6 - i / BONES.length * .9); if (r <= 0) return;
    ctx.beginPath(); ctx.moveTo(h[p][0], h[p][1]); ctx.lineTo(h[p][0] + (h[q][0] - h[p][0]) * r, h[p][1] + (h[q][1] - h[p][1]) * r); ctx.stroke(); });
  noGlow(ctx);
  // joints
  h.forEach(([x, y], k) => { const r = clamp(reveal * 2.2 - k / 21 * 1.2); if (r <= 0) return; const tip = TIPS.includes(k);
    if (k === 0) { ctx.strokeStyle = WHITE; ctx.lineWidth = 2; const s = 16 * r; ctx.beginPath(); ctx.moveTo(x - s, y); ctx.lineTo(x + s, y); ctx.moveTo(x, y - s); ctx.lineTo(x, y + s); ctx.stroke();
      ctx.strokeStyle = ACC2; ctx.beginPath(); ctx.arc(x, y, 9 * r, 0, Math.PI * 2); ctx.stroke(); }
    else if (tip) { ctx.strokeStyle = ACC2; ctx.lineWidth = 2.4; glow(ctx, ACC, 12); ctx.beginPath(); ctx.arc(x, y, 11 * r * (1 + .12 * Math.sin(t * 8 + k)), 0, Math.PI * 2); ctx.stroke(); noGlow(ctx);
      ctx.fillStyle = WHITE; ctx.fillRect(x - 3, y - 3, 6, 6); }
    else { ctx.fillStyle = WHITE; const s = 7 * r; ctx.fillRect(x - s / 2, y - s / 2, s, s); }
    if (ids && r >= 1 && (tip || k === 0)) mono(ctx, String(k).padStart(2, "0"), x + 15, y - 12, 13, ACC2, "left", 600); });
  ctx.restore();
}

export function drawBrackets(ctx, m, { a = 1, k = 1, label = "HAND_01", t = 0 } = {}) {
  if (!m) return; const [x0, y0, x1, y1] = m.box, p = 30, L = 34;
  const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2, s = 1 + (1 - k) * .5;
  const X0 = cx + (x0 - p - cx) * s, X1 = cx + (x1 + p - cx) * s, Y0 = cy + (y0 - p - cy) * s, Y1 = cy + (y1 + p - cy) * s;
  ctx.save(); ctx.globalAlpha = a * k; ctx.strokeStyle = ACC2; ctx.lineWidth = 3; glow(ctx, ACC, 10);
  [[X0, Y0, 1, 1], [X1, Y0, -1, 1], [X0, Y1, 1, -1], [X1, Y1, -1, -1]].forEach(([x, y, dx, dy]) => { ctx.beginPath(); ctx.moveTo(x + dx * L, y); ctx.lineTo(x, y); ctx.lineTo(x, y + dy * L); ctx.stroke(); });
  noGlow(ctx); ctx.globalAlpha = a * clamp(k * 2 - 1);
  tab(ctx, `${label} · LOCK ${(.9 + m.conf * .099).toFixed(2)}`, X0, Y0 - 10);
  mono(ctx, `${Math.round(X1 - X0)}×${Math.round(Y1 - Y0)} PX`, X1, Y1 + 26, 14, WHITE, "right");
  mono(ctx, gestureName(m.g), X0, Y1 + 26, 14, ACC2, "left", 700);
  ctx.restore(); return [X0, Y0, X1, Y1];
}

// angle arc between thumb and index (at index MCP) + pinch distance
export function drawAngle(ctx, m, a = 1) {
  if (!m) return; const h = m.h, [cx, cy] = h[2]; const a1 = Math.atan2(h[4][1] - cy, h[4][0] - cx), a2 = Math.atan2(h[8][1] - h[5][1], h[8][0] - h[5][0]);
  ctx.save(); ctx.globalAlpha = a; ctx.strokeStyle = ACC2; ctx.lineWidth = 2; ctx.setLineDash([4, 5]);
  ctx.beginPath(); ctx.moveTo(h[4][0], h[4][1]); ctx.lineTo(h[8][0], h[8][1]); ctx.stroke(); ctx.setLineDash([]);
  const mx = (h[4][0] + h[8][0]) / 2, my = (h[4][1] + h[8][1]) / 2; tab(ctx, `d ${m.pinch.toFixed(2)}`, mx + 10, my - 8, "rgba(11,13,20,.75)", ACC2, 13);
  let s = a1, e = a2; if (Math.abs(e - s) > Math.PI) e += e < s ? Math.PI * 2 : -Math.PI * 2;
  ctx.strokeStyle = WHITE; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(cx, cy, 58, Math.min(s, e), Math.max(s, e)); ctx.stroke();
  const am = (s + e) / 2; mono(ctx, `${Math.round(m.ang)}°`, cx + Math.cos(am) * 84, cy + Math.sin(am) * 84 + 5, 16, WHITE, "center", 700);
  ctx.restore();
}

// code tokens streaming along each fingertip's recent path ("line code" trails)
export function drawTrails(ctx, T, t, { a = 1, len = .55, tips = TIPS } = {}) {
  ctx.save(); ctx.globalAlpha = a; ctx.font = `500 15px "Geist Mono", monospace`; ctx.letterSpacing = "0px"; ctx.textBaseline = "middle";
  tips.forEach((k, ti) => {
    const pts = []; for (let s = 0; s <= 24; s++) { const tt = t - len * s / 24; if (tt < 0) break; const h = handAt(T, tt); if (!h) break; pts.push(h[k]); }
    if (pts.length < 3) return;
    // thin guide line
    ctx.strokeStyle = k === 8 ? "rgba(127,160,255,.55)" : "rgba(244,246,251,.25)"; ctx.lineWidth = k === 8 ? 2 : 1.2; ctx.beginPath(); pts.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.stroke();
    // tokens placed by arc length
    let acc = 0, next = 18, tok = Math.floor(t * 9) + ti * 7;
    for (let i = 1; i < pts.length; i++) { const [x0, y0] = pts[i - 1], [x1, y1] = pts[i], L = Math.hypot(x1 - x0, y1 - y0); acc += L;
      if (acc < next) continue; next = acc + 30 + (tok % 3) * 10; const fade = 1 - i / pts.length;
      const word = TOKENS[(tok++) % TOKENS.length]; ctx.save(); ctx.translate(x1, y1); let r = Math.atan2(y0 - y1, x0 - x1); if (Math.abs(r) > Math.PI / 2) r += Math.PI; ctx.rotate(r);
      ctx.fillStyle = k === 8 ? `rgba(127,160,255,${fade})` : `rgba(244,246,251,${fade * .85})`; ctx.fillText(word, 0, 0); ctx.restore(); }
  });
  ctx.restore();
}

// telemetry panel (top-left)
export function drawPanel(ctx, T, t, { x = 56, y = 120, a = 1, title = "HAND_TRACKING" } = {}) {
  const m = metrics(T, t); ctx.save(); ctx.globalAlpha = a;
  ctx.fillStyle = "rgba(9,11,20,.62)"; ctx.fillRect(x, y, 360, 300); ctx.strokeStyle = "rgba(127,160,255,.35)"; ctx.lineWidth = 1; ctx.strokeRect(x + .5, y + .5, 359, 299);
  ctx.fillStyle = ACC; ctx.fillRect(x, y, 4, 300);
  mono(ctx, "LABS.VISION", x + 22, y + 32, 15, WHITE, "left", 700); mono(ctx, title, x + 338, y + 32, 13, ACC2, "right", 600);
  const row = (k, v, i, col = WHITE) => { mono(ctx, k, x + 22, y + 66 + i * 27, 13, "rgba(244,246,251,.55)"); mono(ctx, v, x + 338, y + 66 + i * 27, 14, col, "right", 600); };
  row("FPS", "60.0", 0); row("LATENCY", `${(11 + 3 * Math.sin(t * 3)).toFixed(1)} ms`, 1);
  row("WRIST XY", m ? `${(m.h[0][0] / W).toFixed(3)}  ${(m.h[0][1] / H).toFixed(3)}` : "— —", 2);
  row("VELOCITY", m ? `${Math.round(m.vel)} px/s` : "0 px/s", 3, ACC2); row("SPREAD", m ? `${Math.round(m.spread * 100)} %` : "—", 4);
  // velocity sparkline
  ctx.strokeStyle = ACC2; ctx.lineWidth = 1.6; ctx.beginPath();
  for (let i = 0; i <= 40; i++) { const tt = t - (40 - i) / 30; const mm = tt >= 0 ? metrics(T, tt) : null; const v = mm ? Math.min(1, mm.vel / 2200) : 0; const px = x + 22 + i * 7.9, py = y + 222 - v * 34; i ? ctx.lineTo(px, py) : ctx.moveTo(px, py); }
  ctx.stroke();
  // gesture bars
  const G = m ? m.g : { OPEN: 0, FIST: 0, PINCH: 0, POINT: 0 };
  Object.entries(G).forEach(([k, v], i) => { const bx = x + 22 + i * 82; mono(ctx, k, bx, y + 248, 11, "rgba(244,246,251,.6)"); ctx.fillStyle = "rgba(244,246,251,.14)"; ctx.fillRect(bx, y + 258, 70, 8);
    ctx.fillStyle = v > .5 ? ACC2 : "rgba(244,246,251,.55)"; ctx.fillRect(bx, y + 258, 70 * v, 8); mono(ctx, v.toFixed(2), bx, y + 285, 11, v > .5 ? ACC2 : "rgba(244,246,251,.5)"); });
  ctx.restore();
}

// REC bar + corner frame
export function drawFrameHud(ctx, t, { a = 1, mode = "HAND_TRACKING ON" } = {}) {
  ctx.save(); ctx.globalAlpha = a; ctx.strokeStyle = "rgba(244,246,251,.7)"; ctx.lineWidth = 2;
  [[40, 40, 1, 1], [1880, 40, -1, 1], [40, 1040, 1, -1], [1880, 1040, -1, -1]].forEach(([x, y, dx, dy]) => { ctx.beginPath(); ctx.moveTo(x + dx * 40, y); ctx.lineTo(x, y); ctx.lineTo(x, y + dy * 40); ctx.stroke(); });
  const blink = Math.floor(t * 2) % 2 === 0; ctx.fillStyle = blink ? "#FF3B4E" : "rgba(255,59,78,.35)"; ctx.beginPath(); ctx.arc(76, 1004, 7, 0, Math.PI * 2); ctx.fill();
  const tc = `${String(Math.floor(t / 60)).padStart(2, "0")}:${String(Math.floor(t) % 60).padStart(2, "0")}:${String(Math.floor(t * 60) % 60).padStart(2, "0")}`;
  mono(ctx, `REC  ${tc}   LABS.VISION · CAM_01 · 1920×1080 · 60 FPS · ${mode}`, 94, 1009, 15, WHITE);
  mono(ctx, "ngorz.xyz", 1864, 1009, 15, "rgba(244,246,251,.7)", "right");
  ctx.restore();
}

// horizontal scan line with trailing gradient; returns current y
export function drawScan(ctx, p, { a = 1, h = 220 } = {}) {
  const y = -40 + p * (H + 80); ctx.save(); ctx.globalAlpha = a;
  const g = ctx.createLinearGradient(0, y - h, 0, y); g.addColorStop(0, "rgba(46,91,255,0)"); g.addColorStop(1, "rgba(46,91,255,.28)"); ctx.fillStyle = g; ctx.fillRect(0, y - h, W, h);
  ctx.fillStyle = ACC2; glow(ctx, ACC, 18); ctx.fillRect(0, y - 1.5, W, 3); ctx.restore(); return y;
}

// edge-vision: Sobel edges of the current frame tinted blue, revealed above the scan line
export function edgeLayer(src, sw = 480, sh = 270) {
  const c = document.createElement("canvas"); c.width = sw; c.height = sh; const x = c.getContext("2d", { willReadFrequently: true }); x.drawImage(src, 0, 0, sw, sh);
  const d = x.getImageData(0, 0, sw, sh), p = d.data, g = new Float32Array(sw * sh);
  for (let i = 0; i < sw * sh; i++) g[i] = p[i * 4] * .3 + p[i * 4 + 1] * .59 + p[i * 4 + 2] * .11;
  const o = x.createImageData(sw, sh);
  for (let y = 1; y < sh - 1; y++) for (let X = 1; X < sw - 1; X++) { const i = y * sw + X;
    const gx = -g[i - sw - 1] - 2 * g[i - 1] - g[i + sw - 1] + g[i - sw + 1] + 2 * g[i + 1] + g[i + sw + 1];
    const gy = -g[i - sw - 1] - 2 * g[i - sw] - g[i - sw + 1] + g[i + sw - 1] + 2 * g[i + sw] + g[i + sw + 1];
    const m = Math.min(255, Math.hypot(gx, gy) * 1.4); const v = m > 60 ? m : 0; o.data[i * 4] = 127; o.data[i * 4 + 1] = 160; o.data[i * 4 + 2] = 255; o.data[i * 4 + 3] = v; }
  x.putImageData(o, 0, 0); return c;
}

// object box (manually keyframed targets: laptop, phone, glass)
export function drawObj(ctx, [x, y, w, h], label, { a = 1, k = 1, sub = "" } = {}) {
  ctx.save(); ctx.globalAlpha = a; ctx.strokeStyle = WHITE; ctx.lineWidth = 2; ctx.setLineDash([10, 7]); ctx.lineDashOffset = -k * 40;
  const s = 1 + (1 - k) * .25, cx = x + w / 2, cy = y + h / 2; ctx.strokeRect(cx - w * s / 2, cy - h * s / 2, w * s, h * s); ctx.setLineDash([]);
  ctx.fillStyle = ACC2; [[0, 0], [1, 0], [0, 1], [1, 1]].forEach(([u, v]) => ctx.fillRect(cx - w * s / 2 + u * w * s - 4, cy - h * s / 2 + v * h * s - 4, 8, 8));
  if (k > .6) { const tw = tab(ctx, label, cx - w * s / 2, cy - h * s / 2 - 8, "rgba(244,246,251,.95)", INK, 14); if (sub) mono(ctx, sub, cx - w * s / 2 + tw + 10, cy - h * s / 2 - 16, 13, ACC2, "left", 600); }
  ctx.restore();
}
