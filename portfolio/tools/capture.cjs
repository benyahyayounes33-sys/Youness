/**
 * Records the scripted walkthrough of The Well, frame by frame, with its offline-rendered soundtrack.
 *   node tools/capture.cjs [out.mp4] [width] [height] [fps]     (needs `npm run preview` on :4173)
 */
const { chromium } = require("playwright");
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

const OUT = path.resolve(process.argv[2] || "out/the-well-walkthrough.mp4");
const W = +(process.argv[3] || 1280), H = +(process.argv[4] || 720), FPS = +(process.argv[5] || 30);
fs.mkdirSync(path.dirname(OUT), { recursive: true });

const sm = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
const ease = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);

/* ---- the script: scroll position p(t) and interaction commands, t in seconds of video ---- */
const ENTER = 4.6, END = 71;
const keys = [ // [t, p] — piecewise smooth
  [ENTER, 0], [8.5, 0.035], [11.5, 0.075], [16, 0.17], [17.2, 0.27], [21, 0.31], [24, 0.33],
  [37, 0.36], [42.4, 0.47], [43.3, 0.555], [47.5, 0.62], [51, 0.82], [62.5, 0.84], [69, 1.0], [END, 1.0],
];
function pAt(t) {
  if (t <= keys[0][0]) return 0;
  for (let i = 1; i < keys.length; i++) {
    const [t0, p0] = keys[i - 1], [t1, p1] = keys[i];
    if (t <= t1) return p0 + (p1 - p0) * ease((t - t0) / (t1 - t0));
  }
  return 1;
}
function cmdAt(t, f) {
  const c = {};
  // look around during the descent, then hover a screen before clicking it
  if (t > 20 && t < 27.6) c.pointer = [0.42 * sm(20, 23, t), 0.05];
  if (f === Math.round(27.6 * FPS)) c.focus = "pointer";
  if (t > 28.8 && t < 33.8) c.scrub = 0.063 / FPS;   // ~0.3 of the page over 5 s, independent of fps
  if (f === Math.round(34.2 * FPS)) c.unfocus = true;
  // at the bottom: look at a ring screen (the figure turns to it), then another, then back to the zoetrope
  const A = [-0.2, 0.92], B = [0.3, 0.9];
  const mix = (u, v, k) => [u[0] + (v[0] - u[0]) * k, u[1] + (v[1] - u[1]) * k];
  if (t > 53.5 && t < 57) c.pointer = mix([0, 0], A, sm(53.5, 55, t));
  else if (t >= 57 && t < 59.6) c.pointer = mix(A, B, sm(57, 58.2, t));
  else if (t >= 59.6 && t < 62) c.pointer = mix(B, [0, 0], sm(59.6, 61, t));
  return c;
}

(async () => {
  const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  page.on("pageerror", (e) => console.error("PAGEERROR", e.message));
  await page.goto("http://localhost:4173/?capture=1", { waitUntil: "networkidle" });
  await page.waitForFunction(() => window.__cap && window.__cap.ready, null, { timeout: 120000 });
  await page.evaluate(([w, h]) => __cap.size(w, h), [W, H]);
  const cdp = await page.context().newCDPSession(page);

  const silent = OUT.replace(/\.mp4$/, "_video.mp4");
  const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "mjpeg", "-i", "-",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", silent], { stdio: ["pipe", "inherit", "inherit"] });

  const N = Math.round(END * FPS);
  const t0 = Date.now();
  let entered = false, focusIdx = -1;
  for (let f = 0; f < N; f++) {
    const t = f / FPS;
    if (t < ENTER) {
      await page.evaluate(([t, press]) => { __cap.press(press); __cap.gate(t); }, [t, t > 3.9]);
    } else {
      if (!entered) { await page.evaluate((t) => __cap.enter(t), t); entered = true; }
      const c = cmdAt(t, f);
      if (c.focus === "pointer") { focusIdx = await page.evaluate(() => __cap.screenIndexNear(0.42, 0.05)); c.focus = focusIdx >= 0 ? focusIdx : null; }
      await page.evaluate(([t, p, c, fps]) => __cap.frame(t, 1 / fps, p, c), [t, pAt(t), c, FPS]);
    }
    const shot = await cdp.send("Page.captureScreenshot", { format: "jpeg", quality: 93 });
    if (!ff.stdin.write(Buffer.from(shot.data, "base64"))) await new Promise((r) => ff.stdin.once("drain", r));
    if (f % 150 === 0) console.log(`frame ${f}/${N}  ${((Date.now() - t0) / 1000).toFixed(0)}s  focus=${focusIdx}`);
  }
  ff.stdin.end();
  await new Promise((r) => ff.on("close", r));

  console.log("rendering audio…");
  const b64 = await page.evaluate(([d, s]) => __cap.audio(d, s), [END, ENTER]);
  const wav = OUT.replace(/\.mp4$/, ".wav");
  fs.writeFileSync(wav, Buffer.from(b64, "base64"));
  console.log("events:", await page.evaluate(() => __cap.eventCount()));
  await browser.close();
  await new Promise((r) => spawn("ffmpeg", ["-y", "-loglevel", "error", "-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], { stdio: "inherit" }).on("close", r));
  console.log("done", OUT, ((Date.now() - t0) / 60000).toFixed(1), "min");
})();
