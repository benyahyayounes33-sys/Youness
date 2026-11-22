/**
 * Renders price-list.html to an Instagram Story PNG (1080x1920) and checks the text and layout.
 *   node render.cjs            -> price-list-story.png
 */
const { chromium } = require("playwright");
const { execFileSync } = require("child_process");
const path = require("path");

const HERE = __dirname;
const EXPECTED = [
  "POSTER & STICKER PACKS",
  "Custom Prints • Delivery Across Morocco",
  "STARTER PACKS",
  "Mini Try-Me Pack|3 A4 + 3 A5 + 3 Stickers|60 DH",
  "Desk & Laptop Pack|6 A5 + 9 Stickers|75 DH",
  "100 DH MIX PACKS",
  "Classic Mix|6 A4 + 5 A5 + 5 Stickers|100 DH",
  "Wall & Laptop|6 A4 + 15 Stickers|100 DH",
  "Mini Wall & Stickers ★ BEST SELLER|9 A5 + 12 Stickers|100 DH",
  "VALUE PACKS",
  "Creator Mix ★ BEST VALUE|9 A4 + 9 A5 + 10 Stickers|150 DH",
  "Full Room Makeover|15 A4 + 12 A5 + 15 Stickers|220 DH",
  "DM to Order • Custom Photos & Themes",
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 2 });
  await page.goto("file://" + path.join(HERE, "price-list.html"));
  await page.waitForFunction(() => document.body.dataset.ready === "1");

  // ---- text check: rebuild each line from the DOM exactly as a reader sees it
  const got = await page.evaluate(() => {
    const txt = (el) => {
      let s = "";
      el.childNodes.forEach((n) => {
        if (n.nodeType === 3) s += n.textContent;
        else if (n.dataset && n.dataset.text) s += n.dataset.text;          // badge: star icon + label
        else if (n.getAttribute && n.getAttribute("aria-label")) s += n.getAttribute("aria-label"); // bullet dot
        else s += txt(n);
      });
      return s;
    };
    const clean = (s) => s.replace(/\s+/g, " ").trim();
    const out = [clean(document.querySelector(".l1").textContent + " " + document.querySelector(".l2").textContent), clean(txt(document.querySelector(".sub")))];
    document.querySelectorAll("section").forEach((sec) => {
      out.push(clean(sec.querySelector("h2").textContent));
      sec.querySelectorAll(".row").forEach((r) => out.push([txt(r.querySelector(".name")), r.querySelector(".items").textContent, r.querySelector(".price").textContent.replace("DH", " DH")].map(clean).join("|")));
    });
    out.push(clean(txt(document.querySelector(".cta"))));
    return out;
  });
  let ok = true;
  EXPECTED.forEach((e, i) => { if (got[i] !== e) { ok = false; console.log(`TEXT MISMATCH\n  expected: ${e}\n  got:      ${got[i]}`); } });
  console.log(ok && got.length === EXPECTED.length ? `text: all ${EXPECTED.length} lines match exactly` : "text: CHECK FAILED");

  // ---- layout check: everything inside the Instagram-safe zone, nothing overflowing
  const lay = await page.evaluate(() => {
    const r = (el) => el.getBoundingClientRect();
    const story = document.querySelector(".story");
    const blocks = [...story.children].map((c) => ({ tag: c.tagName, top: Math.round(r(c).top), bottom: Math.round(r(c).bottom) }));
    const gaps = blocks.slice(1).map((b, i) => b.top - blocks[i].bottom);
    const over = [...document.querySelectorAll(".row, .l1, .cta, .name, .items")].filter((el) => el.scrollWidth > el.clientWidth + 1 || r(el).right > 1080 - 63 || r(el).left < 63).map((el) => el.className);
    return { blocks, gaps, over, titleSize: getComputedStyle(document.getElementById("title")).fontSize };
  });
  console.log("title size", lay.titleSize, "| first top", lay.blocks[0].top, "| last bottom", lay.blocks.at(-1).bottom, "| gaps", lay.gaps.join(", "));
  console.log(lay.over.length ? "OVERFLOW: " + lay.over.join(", ") : "layout: no overflow, all inside 64 px margins");
  if (lay.blocks[0].top < 190 || lay.blocks.at(-1).bottom > 1720) console.log("WARNING: content outside the story safe zone");

  const hi = path.join(HERE, "price-list-story@2x.png");
  await page.screenshot({ path: hi });
  await browser.close();
  // supersampled render -> exact 1080x1920
  execFileSync("python3", ["-c", `
from PIL import Image
im = Image.open(${JSON.stringify(hi)}).convert("RGB")
im.resize((1080, 1920), Image.LANCZOS).save(${JSON.stringify(path.join(HERE, "price-list-story.png"))}, optimize=True)
`]);
  console.log("saved price-list-story.png (1080x1920) and price-list-story@2x.png (2160x3840)");
})();
