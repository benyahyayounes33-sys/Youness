#!/usr/bin/env python3
"""Prepare A4-shaped product images + scenes for the Next.js store (web/public).

    python3 tools/prep_web_assets.py [--originals DIR] [--upscaled DIR]

--originals : folder with the ONELINE original designs (tools/make_originals.py output)
--upscaled  : optional folder with *_x4.png Real-ESRGAN versions (used when present)
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from make_print_pdf import to_a4, trim_white  # noqa: E402

OUT = os.path.join(ROOT, "web/public/products")
W_, H_ = 1000, 1414
A4R = H_ / W_


def crop_a4(img, anchor):
    w, h = img.size
    if h / w > A4R:
        nh = int(round(w * A4R))
        y0 = int((h - nh) * anchor)
        return img.crop((0, y0, w, y0 + nh))
    nw = int(round(h / A4R))
    x0 = int((w - nw) * anchor)
    return img.crop((x0, 0, x0 + nw, h))


def sticker_mockup(img):
    im = img.convert("RGB")
    a = np.asarray(im)
    tmp = im.copy()
    w, h = im.size
    for c in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        ImageDraw.floodfill(tmp, c, (255, 0, 255), thresh=12)
    t = np.asarray(tmp)
    m = ~((t[..., 0] == 255) & (t[..., 1] == 0) & (t[..., 2] == 255))
    alpha = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1))
    bg = np.zeros((H_, W_, 3), np.float32)
    yy, xx = np.mgrid[0:H_, 0:W_].astype(np.float32)
    r = np.sqrt(((xx - W_ / 2) / W_) ** 2 + ((yy - H_ * 0.45) / H_) ** 2)
    bg[:] = (np.array([46, 46, 50]) * (1 - np.clip(r * 1.3, 0, 1))[..., None] + np.array([22, 22, 25]))
    page = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8))
    tw = int(W_ * 0.78)
    th = int(h * tw / w)
    st = im.resize((tw, th), Image.LANCZOS)
    al = alpha.resize((tw, th), Image.LANCZOS)
    x, y = (W_ - tw) // 2, int(H_ * 0.45 - th / 2)
    shadow = al.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.7))
    page.paste((0, 0, 0), (x + 10, y + 24), shadow)
    page.paste(st, (x, y), al)
    return page


def main():
    args = sys.argv[1:]
    originals = args[args.index("--originals") + 1] if "--originals" in args else None
    upscaled = args[args.index("--upscaled") + 1] if "--upscaled" in args else None
    cat = json.load(open(os.path.join(ROOT, "tools/web_catalog.json")))
    os.makedirs(OUT, exist_ok=True)
    for item in cat:
        src = item["src"]
        if src.startswith("orig:"):
            path = os.path.join(originals, src[5:] + ".jpg")
        else:
            path = os.path.join(ROOT, src)
            if upscaled:
                cand = os.path.join(upscaled, os.path.splitext(os.path.basename(src))[0] + "_x4.png")
                if os.path.exists(cand):
                    path = cand
        img = Image.open(path).convert("RGB")
        fit = item.get("fit", "pad")
        if fit == "sticker":
            out = sticker_mockup(img)
        elif fit == "crop":
            out = crop_a4(trim_white(img), item.get("anchor", 0.5)).resize((W_, H_), Image.LANCZOS)
        else:
            out = to_a4(img).resize((W_, H_), Image.LANCZOS)
        out.save(os.path.join(OUT, item["slug"] + ".jpg"), quality=86, optimize=True, progressive=True)
        print(item["slug"], os.path.basename(path))


if __name__ == "__main__":
    main()
