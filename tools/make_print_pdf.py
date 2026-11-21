#!/usr/bin/env python3
"""
Build a print-ready A4 PDF (one design per page, 300 DPI, full bleed).

    python3 tools/make_print_pdf.py OUT.pdf IMG1 IMG2 ... [--sticker IMG] [--title "..."]

Posters that are not exactly A4-shaped are extended to A4 by continuing their own paper edge
(row/column-wise edge colour + grain), so nothing is cropped and no white bars appear.
--sticker images are centred on a white page instead (for die-cut sticker designs).
"""
import argparse
import os
import tempfile

import numpy as np
from PIL import Image, ImageFilter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

PX_W, PX_H = 2480, 3508  # A4 @ 300 dpi
A4R = PX_H / PX_W


def _smooth(a, k):
    k = max(1, int(k))
    ker = np.ones(k) / k
    return np.stack([np.convolve(np.pad(a[:, c], (k, k), mode="edge"), ker, mode="same")[k:-k] for c in range(3)], 1)


def _paper_tone(strip):
    """strip: (N, k, 3) pixels near an edge -> (N,3) clean paper colour (ink ignored, slowly varying)."""
    lum = strip.mean(axis=2)
    thr = np.percentile(lum, 60, axis=1, keepdims=True)
    m = (lum >= thr)[..., None]
    tone = (strip * m).sum(axis=1) / np.maximum(m.sum(axis=1), 1)
    return _smooth(tone, 151)


def _edge_fill(strip):
    """Clean light background -> flat colour; textured paper -> slowly varying paper tone."""
    if (strip.mean(axis=2) > 232).mean() > 0.85:
        col = np.median(strip.reshape(-1, 3), axis=0)
        return np.repeat(col[None], strip.shape[0], 0)
    return _paper_tone(strip)


def trim_white(img, thr=238):
    """Remove near-white margins around a poster (e.g. a scan or screenshot border)."""
    a = np.asarray(img.convert("RGB")).astype(np.float32).mean(axis=2)
    rows = np.where((a < thr).mean(axis=1) > 0.004)[0]  # a margin row/col is pure white
    cols = np.where((a < thr).mean(axis=0) > 0.004)[0]
    if len(rows) and len(cols):
        y0, y1, x0, x1 = rows[0], rows[-1] + 1, cols[0], cols[-1] + 1
        if (y1 - y0) * (x1 - x0) < 0.985 * a.size:
            return img.crop((x0, y0, x1, y1))
    return img


def _extend(strip_cols, length, rng):
    """strip_cols: (N,3) paper colours along the edge -> (N,length,3) paper continuation."""
    base = strip_cols[:, None, :].repeat(length, 1)
    grain = rng.normal(0, 2.2, base.shape[:2])[..., None]
    return np.clip(base + grain, 0, 255)


def to_a4(img, seed=0):
    rng = np.random.default_rng(seed)
    img = trim_white(img.convert("RGB"))
    w, h = img.size
    r = h / w
    if abs(r - A4R) < 0.012:
        return img.resize((PX_W, PX_H), Image.LANCZOS)
    if r > A4R:  # too tall -> fit height, continue left/right edges
        nw = int(round(w * PX_H / h))
        a = np.asarray(img.resize((nw, PX_H), Image.LANCZOS)).astype(np.float32)
        padl = (PX_W - nw) // 2
        padr = PX_W - nw - padl
        L = _extend(_edge_fill(a[:, 2:60]), padl, rng)
        R = _extend(_edge_fill(a[:, -60:-2]), padr, rng)
        out = np.concatenate([L, a, R], axis=1)
        for x0, sgn in ((padl, 1), (padl + nw, -1)):  # feather the seams
            for i in range(6):
                al = (i + 1) / 7
                xi = x0 + (i if sgn > 0 else -1 - i)
                xo = x0 - 1 - i if sgn > 0 else x0 + i
                out[:, xi] = out[:, xi] * al + out[:, min(max(xo, 0), PX_W - 1)] * (1 - al)
    else:  # too wide -> fit width, continue top/bottom edges
        nh = int(round(h * PX_W / w))
        a = np.asarray(img.resize((PX_W, nh), Image.LANCZOS)).astype(np.float32)
        padt = (PX_H - nh) // 2
        padb = PX_H - nh - padt
        T = _extend(_edge_fill(a[2:60].transpose(1, 0, 2)), padt, rng).transpose(1, 0, 2)
        B = _extend(_edge_fill(a[-60:-2].transpose(1, 0, 2)), padb, rng).transpose(1, 0, 2)
        out = np.concatenate([T, a, B], axis=0)
    return Image.fromarray(out.astype(np.uint8))


def sticker_page(img, width_frac=0.80):
    img = img.convert("RGB")
    page = Image.new("RGB", (PX_W, PX_H), (255, 255, 255))
    tw = int(PX_W * width_frac)
    th = int(img.height * tw / img.width)
    page.paste(img.resize((tw, th), Image.LANCZOS), ((PX_W - tw) // 2, (PX_H - th) // 2))
    return page


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("images", nargs="+")
    ap.add_argument("--sticker", action="append", default=[])
    ap.add_argument("--title", default="Print file")
    args = ap.parse_args()
    pages = [to_a4(Image.open(p), i) for i, p in enumerate(args.images)]
    pages += [sticker_page(Image.open(p)) for p in args.sticker]
    with tempfile.TemporaryDirectory() as td:
        c = canvas.Canvas(args.out, pagesize=A4)
        c.setTitle(args.title)
        c.setAuthor("ONELINE")
        c.setSubject("A4 210x297 mm, 300 dpi, full bleed - print at 100% scale")
        for i, pg in enumerate(pages):
            fp = os.path.join(td, f"p{i:02d}.jpg")
            pg = pg.filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=2))
            pg.save(fp, quality=95, subsampling=0, dpi=(300, 300))
            c.drawImage(fp, 0, 0, width=A4[0], height=A4[1])
            c.showPage()
        c.save()
    print(f"{args.out}: {len(pages)} pages, {os.path.getsize(args.out) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
