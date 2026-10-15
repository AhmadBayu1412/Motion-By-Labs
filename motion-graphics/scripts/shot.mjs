// Full-page screenshot of a local HTML file served over http (so ES modules, fetch and fonts work).
//   node shot.mjs <root-dir> <page.html> <out.png> [width=1920]
// The page signals readiness by setting window.ready = true (fonts loaded, canvases drawn).
import http from "node:http"; import fs from "node:fs"; import path from "node:path";
import { spawnSync } from "node:child_process"; import { createRequire } from "node:module";
const [root, page, out, width = "1920"] = process.argv.slice(2); const ROOT = path.resolve(root);
const r = createRequire(import.meta.url);
let chromium; try { chromium = (await import("playwright")).chromium; } catch { chromium = r(path.join(spawnSync("npm", ["root", "-g"], { encoding: "utf8" }).stdout.trim(), "playwright")).chromium; }
const MIME = { ".html": "text/html", ".js": "text/javascript", ".json": "application/json", ".jpg": "image/jpeg", ".png": "image/png", ".woff2": "font/woff2", ".svg": "image/svg+xml" };
const srv = http.createServer((q, s) => { const p = path.join(ROOT, decodeURIComponent(new URL(q.url, "http://x").pathname)); if (!p.startsWith(ROOT) || !fs.existsSync(p)) { s.writeHead(404); return s.end(); } s.writeHead(200, { "content-type": MIME[path.extname(p)] || "application/octet-stream" }); fs.createReadStream(p).pipe(s); });
await new Promise(res => srv.listen(0, "127.0.0.1", res));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +width, height: 400 } }); p.on("pageerror", e => console.error("page error:", e.message));
await p.goto(`http://127.0.0.1:${srv.address().port}/${page}`);
await p.waitForFunction(() => window.ready === true, null, { timeout: 180000 }); await p.waitForTimeout(250);
await p.screenshot({ path: path.resolve(out), fullPage: true }); await b.close(); srv.close(); console.log("wrote", out);
