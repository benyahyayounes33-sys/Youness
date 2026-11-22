/**
 * Records the nine walls: full-page captures of the ONELINE store, saved as scroll strips for the screens.
 *   node tools/capture-sites.cjs [storeUrl]      (default http://localhost:3100 — run the store with `npm run start` in ../web)
 */
const { chromium } = require("playwright");
const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const BASE = process.argv[2] || "http://localhost:3100";
const RAW = path.join(__dirname, ".raw");
const DST = path.join(__dirname, "..", "public", "sites");
const PAGES = [["home", "/"], ["shop", "/shop"], ["anime", "/collections/anime-gaming"], ["cars", "/collections/jdm-luxury-cars"],
  ["movies", "/collections/movies-series"], ["music", "/collections/music-artists"], ["football", "/collections/football-sports"],
  ["minimal", "/collections/minimal-aesthetic"], ["motivation", "/collections/motivational"]];

(async () => {
  fs.mkdirSync(RAW, { recursive: true });
  fs.mkdirSync(DST, { recursive: true });
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 1280, height: 800 } })).newPage();
  for (const [slug, route] of PAGES) {
    await p.goto(BASE + route, { waitUntil: "networkidle" });
    await p.addStyleTag({ content: ".grain::after{display:none!important}" });
    const h = await p.evaluate(() => document.body.scrollHeight);
    for (let y = 0; y < h; y += 400) { await p.evaluate((y) => scrollTo(0, y), y); await p.waitForTimeout(90); }
    await p.evaluate(() => scrollTo(0, 0));
    await p.waitForTimeout(1500);
    await p.screenshot({ path: path.join(RAW, `${slug}.png`), fullPage: true });
    // 512 px wide strip (max 4096 tall) + a thumbnail, via Python/Pillow
    execFileSync("python3", ["-c", `
from PIL import Image
im = Image.open(${JSON.stringify(path.join(RAW, slug + ".png"))}).convert("RGB")
W = 512; im = im.resize((W, int(im.height * W / im.width)), Image.LANCZOS)
im = im.crop((0, 0, W, min(im.height, 4096)))
im.save(${JSON.stringify(path.join(DST, slug + ".jpg"))}, quality=82, optimize=True, progressive=True)
im.crop((0, 0, W, 320)).save(${JSON.stringify(path.join(DST, slug + "-thumb.jpg"))}, quality=80)
`]);
    console.log("recorded", slug);
  }
  await b.close();
  fs.rmSync(RAW, { recursive: true, force: true });
})();
