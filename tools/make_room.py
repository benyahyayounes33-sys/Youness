#!/usr/bin/env python3
"""Render the 'before / after' room scene used on the store (identical light, empty vs. poster wall).

Golden-hour gallery corner: plaster wall, window light with dappled leaf shadows, oak console,
out-of-focus plant in the foreground.

    python3 tools/make_room.py OUT_DIR poster1.jpg ... poster6.jpg
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 2400, 1500
FLOOR_Y = 1250
CONSOLE = (700, 990, 1700, 1250)   # x0, top, x1, bottom


def noise(w, h, r, seed, amp):
    a = np.random.default_rng(seed).normal(0, 1, (h // 4, w // 4)).astype(np.float32)
    im = Image.fromarray(np.clip(128 + 40 * a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)).resize((w, h), Image.BICUBIC)
    n = np.asarray(im).astype(np.float32)
    return (n - n.mean()) / (n.std() + 1e-6) * amp


def mask(fn, blur=1.5):
    m = Image.new("L", (W, H), 0)
    fn(ImageDraw.Draw(m))
    if blur:
        m = m.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(m).astype(np.float32)[..., None] / 255


def comp(a, m, color):
    return a * (1 - m) + np.array(color, np.float32) * m


def vgrad(y0, y1, c0, c1):
    t = np.clip((np.arange(H, dtype=np.float32) - y0) / max(1, y1 - y0), 0, 1)[:, None, None]
    return np.array(c0, np.float32) * (1 - t) + np.array(c1, np.float32) * t


def scene(files=None):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    a = np.ones((H, W, 3), np.float32) * np.array([222, 214, 202], np.float32)
    a *= (1 + noise(W, H, 2.5, 1, 0.010) + noise(W, H, 12, 2, 0.012))[..., None]
    # floor
    fl = vgrad(FLOOR_Y, H, (150, 112, 80), (112, 80, 56))
    a = np.where((yy >= FLOOR_Y)[..., None], fl * (1 + noise(W, H, 1, 3, 0.03))[..., None], a)
    a[FLOOR_Y - 22:FLOOR_Y] = np.array([232, 228, 221], np.float32)
    # posters
    if files:
        pw, ph, gap = 236, 334, 40
        x0 = 1200 - (3 * pw + 2 * gap) / 2
        for i, f in enumerate(files[:6]):
            r, c = divmod(i, 3)
            x, y = int(x0 + c * (pw + gap)), int(96 + r * (ph + gap))
            a *= 1 - 0.32 * mask(lambda d, x=x, y=y: d.rectangle((x + 6, y + 14, x + pw + 6, y + ph + 14), fill=255), 13)
            p = Image.open(f).convert("RGB")
            if p.height / p.width > ph / pw:
                nh = int(p.width * ph / pw)
                p = p.crop((0, (p.height - nh) // 2, p.width, (p.height - nh) // 2 + nh))
            a[y:y + ph, x:x + pw] = np.asarray(p.resize((pw, ph), Image.LANCZOS)).astype(np.float32) * 0.97
    # console + objects (contact shadow first)
    x0, top, x1, bot = CONSOLE
    a *= 1 - 0.5 * mask(lambda d: d.rectangle((x0 - 30, top + 40, x1 + 60, bot + 20), fill=255), 35)
    a = comp(a, mask(lambda d: d.rectangle((x0, top + 24, x1, bot), fill=255)), (150, 110, 76))
    a = comp(a, mask(lambda d: d.rectangle((x0, top, x1, top + 24), fill=255)), (178, 136, 98))
    for gx in (x0 + 333, x0 + 666):
        a = comp(a, mask(lambda d, gx=gx: d.line((gx, top + 40, gx, bot - 16), fill=255, width=3)), (118, 84, 56))
    books = [(820, 52, (40, 40, 44)), (812, 40, (196, 74, 58)), (826, 34, (214, 206, 190))]
    by = top
    for bx, bh, col in books:
        a = comp(a, mask(lambda d, bx=bx, by=by, bh=bh: d.rectangle((bx, by - bh, bx + 230, by), fill=255)), col)
        by -= bh
    a = comp(a, mask(lambda d: d.ellipse((1405, top - 130, 1515, top + 4), fill=255)), (206, 199, 188))
    a = comp(a, mask(lambda d: d.rectangle((1444, top - 172, 1476, top - 110), fill=255)), (206, 199, 188))
    a = comp(a, mask(lambda d: d.rounded_rectangle((1570, top - 90, 1630, top), 6, fill=255)), (236, 232, 224))
    # light: window patch with mullions + dappled leaves, warm key from left
    win = mask(lambda d: d.polygon([(-200, -100), (1150, -100), (1650, 1000), (300, 1000)], fill=255), 0)
    mull = mask(lambda d: (d.line((475, -100, 975, 1000), fill=255, width=46),
                           d.line((-100, 430, 1500, 430), fill=255, width=40)), 0)
    win = np.clip(win - mull, 0, 1)
    rng = np.random.default_rng(7)

    def leaves(d):
        for _ in range(70):
            cx, cy = rng.uniform(0, 1500), rng.uniform(-100, 950)
            rx, ry = rng.uniform(25, 70), rng.uniform(10, 26)
            d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
    lv = mask(leaves, 0)
    sun = np.asarray(Image.fromarray((np.clip(win * (1 - 0.85 * lv), 0, 1)[..., 0] * 255).astype(np.uint8))
                     .filter(ImageFilter.GaussianBlur(14))).astype(np.float32)[..., None] / 255
    sun *= (yy < FLOOR_Y)[..., None]
    amb = 0.70 + 0.18 * np.exp(-((xx - 400) ** 2 + (yy - 200) ** 2) / (2 * 1100 ** 2))[..., None]
    L = amb + sun * np.array([0.55, 0.42, 0.25], np.float32)
    L = L * (1 - 0.38 * np.clip(((xx - 1150) / 1300) ** 2 + ((yy - 650) / 1300) ** 2, 0, 1))[..., None]
    a = a * L
    # foreground plant, out of focus
    rng2 = np.random.default_rng(11)

    def plant(d):
        for _ in range(34):
            cx, cy = rng2.uniform(-80, 330), rng2.uniform(820, 1560)
            rx, ry = rng2.uniform(60, 150), rng2.uniform(22, 50)
            d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
    pm = mask(plant, 18)
    a = comp(a, pm * 0.96, (24, 38, 28))
    a += np.random.default_rng(5).normal(0, 2.2, (H, W))[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    scene().save(os.path.join(out, "room-before.jpg"), quality=88)
    scene(sys.argv[2:]).save(os.path.join(out, "room-after.jpg"), quality=88)
    print("ok")
