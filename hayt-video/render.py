#!/usr/bin/env python3
"""
HAYT - Drop 01 teaser  ("From the phone... to the wall")

Renders a ~26.5 s vertical (1080x1920, 30 fps) cinematic promo from 6 poster images,
with Darija + English text and a synthesized sound design (no copyrighted music).

To use your own designs: replace the files in posters/ (keep the same names), then run
    python3 render.py            # full video  -> out/hayt_drop01.mp4 (+ a no-audio copy)
    python3 render.py --preview  # contact sheet of key frames -> out/preview.png
Change BRAND / texts in the CONFIG block below.
"""
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

# ----------------------------------------------------------------------------- CONFIG
BRAND = "HAYT"
BRAND_AR = "حيط"
ACCENT = (200, 169, 126)  # warm sand
POSTERS = [  # file, number, name  (grid order: top row 1-3, bottom row 4-6)
    ("01_911_gt3.jpg", "N° 001", "911 GT3"),
    ("02_992_gt3rs.jpg", "N° 002", "992 GT3 RS"),
    ("03_911_gt3_blue.jpg", "N° 003", "911 GT3 · 992.2"),
    ("04_lucy.jpg", "N° 004", "LUCY"),
    ("05_baby_driver.jpg", "N° 005", "BABY DRIVER"),
    ("06_venom.jpg", "N° 006", "VENOM"),
]
TXT_1_AR, TXT_1_EN = "كل ليلة كنشوفهم غير فالتيليفون", "EVERY NIGHT — ONLY ON MY PHONE"
TXT_2_AR, TXT_2_EN = "وحيطي خاوي", "AND MY WALL IS EMPTY"
TXT_3_AR_A, TXT_3_AR_B, TXT_3_EN = "من التيليفون", "للحيط", "FROM THE PHONE — TO THE WALL"
END_DROP = "DROP 01 · 20 PIECES ONLY"
END_CTA_AR, END_CTA_EN = "صيفط لينا ميساج باش تطلب", 'DM "DROP" TO ORDER'
# -----------------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
DUR = 26.5
NF = int(round(DUR * FPS))
S = 2  # supersampling of the wall canvas
A4 = 297 / 210
RAQM = ImageFont.Layout.RAQM
rng = np.random.default_rng(7)


def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", name), size, layout_engine=RAQM)


F_AR = lambda s: font("Cairo-Arabic-700.ttf", s)
F_AR5 = lambda s: font("Cairo-Arabic-500.ttf", s)
F_LAT = lambda s: font("Michroma.ttf", s)
F_UI = lambda s: font("Inter-SemiBold.otf", s)


# ----------------------------------------------------------------------------- helpers
def clamp01(x):
    return max(0.0, min(1.0, x))


def seg(t, a, b):
    return clamp01((t - a) / (b - a))


def ease_out(x):
    x = clamp01(x)
    return 1 - (1 - x) ** 3


def ease_in(x):
    x = clamp01(x)
    return x ** 3


def ease_io(x):
    x = clamp01(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def lerp(a, b, x):
    return a + (b - a) * x


def edge_color(im):
    a = np.asarray(im).astype(np.float32)
    e = np.concatenate([a[:, :4].reshape(-1, 3), a[:, -4:].reshape(-1, 3)])
    return tuple(int(v) for v in np.median(e, axis=0))


def to_a4(im):
    """Fit any poster to A4 proportions: pad sides if too tall, crop sides if too wide."""
    im = im.convert("RGB")
    w, h = im.size
    r = h / w
    if r > A4 + 0.01:
        nw = int(round(h / A4))
        c = Image.new("RGB", (nw, h), edge_color(im))
        c.paste(im, ((nw - w) // 2, 0))
        return c
    if r < A4 - 0.01:
        nw = int(round(h / A4))
        x0 = (w - nw) // 2
        return im.crop((x0, 0, x0 + nw, h))
    return im


def rounded_mask(w, h, r):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    return m


def blurred_noise(w, h, radius, seed):
    r = np.random.default_rng(seed)
    a = np.clip(128 + 60 * r.standard_normal((h, w)), 0, 255).astype(np.uint8)
    b = np.asarray(Image.fromarray(a, "L").filter(ImageFilter.GaussianBlur(radius))).astype(np.float32)
    return (b - b.mean()) / (b.std() + 1e-6)


def up_f(arr, size):
    return np.asarray(Image.fromarray(arr.astype(np.float32), "F").resize(size, Image.BILINEAR))


A4P = [to_a4(Image.open(os.path.join(HERE, "posters", f))) for f, _, _ in POSTERS]

# ----------------------------------------------------------------------------- wall scene
CW, CH = W * S, H * S
PW, PH, GAP, RGAP = 300, 424, 36, 44
X0 = (W - (3 * PW + 2 * GAP)) // 2
Y0 = 420


def slot(i):
    r, c = divmod(i, 3)
    return X0 + c * (PW + GAP), Y0 + r * (PH + RGAP)


def slot_center(i):
    x, y = slot(i)
    return x + PW / 2, y + PH / 2


def build_albedo():
    coarse = up_f(blurred_noise(W // 2, H // 2, 5, 1), (CW, CH))
    fine = rng.standard_normal((CH, CW)).astype(np.float32)
    base = np.array([226, 221, 212], np.float32)
    a = base[None, None, :] * (1 + 0.011 * coarse + 0.008 * fine)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def place_poster(img, i):
    x, y = slot(i)
    x, y, pw, ph = x * S, y * S, PW * S, PH * S
    m = 40 * S
    sh = Image.new("L", (pw + 2 * m, ph + 2 * m), 0)
    ImageDraw.Draw(sh).rectangle((m, m, m + pw, m + ph), fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(9 * S))
    img.paste((0, 0, 0), (x - m + 5 * S, y - m + 9 * S), sh)
    p = A4P[i].resize((pw, ph), Image.LANCZOS)
    p = ImageEnhance.Brightness(p).enhance(0.97)
    img.paste(p, (x, y))


def light_maps():
    yy, xx = np.mgrid[0:H // 2, 0:W // 2].astype(np.float32)
    xx *= 2
    yy *= 2
    # night: cool ambient + moonlight window patch
    amb = 0.23 + 0.10 * np.exp(-((xx - 540) ** 2 + (yy - 800) ** 2) / (2 * 700 ** 2))
    m = Image.new("L", (W // 2, H // 2), 0)
    d = ImageDraw.Draw(m)
    q = [(560, 170), (1120, 40), (1120, 1010), (650, 1160)]
    d.polygon([(x / 2, y / 2) for x, y in q], fill=255)
    mid = lambda a, b: ((a[0] + b[0]) / 4, (a[1] + b[1]) / 4)
    d.line([mid(q[0], q[1]), mid(q[3], q[2])], fill=0, width=8)
    d.line([mid(q[0], q[3]), mid(q[1], q[2])], fill=0, width=8)
    win = np.asarray(m.filter(ImageFilter.GaussianBlur(12))).astype(np.float32) / 255
    night = amb[..., None] * np.array([0.70, 0.80, 1.0]) + win[..., None] * 0.55 * np.array([0.80, 0.90, 1.05])
    # warm: lamp top-left, falloff towards bottom-right
    key = np.exp(-((xx - 120) ** 2 + (yy + 250) ** 2) / (2 * 1250 ** 2))
    warm = (0.22 + 0.80 * key)[..., None] * np.array([1.06, 0.98, 0.86])
    warm *= (1 - 0.35 * np.clip((yy - 1350) / 570, 0, 1))[..., None]
    return night, warm


def lit(albedo, L):
    a = np.asarray(albedo).astype(np.float32)
    for c in range(3):
        a[..., c] *= up_f(L[..., c], (CW, CH))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def view(canvas, cx, cy, z):
    cw, ch = W / z * S, H / z * S
    x0 = min(max(0.0, cx * S - cw / 2), CW - cw)
    y0 = min(max(0.0, cy * S - ch / 2), CH - ch)
    return canvas.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch), reducing_gap=2.0)


print("building wall canvases...")
L_NIGHT, L_WARM = light_maps()
ALB = build_albedo()
ORDER = [1, 0, 2, 3, 4, 5]  # 992 first (match cut), then the rest go up
NIGHT = [lit(ALB, L_NIGHT)]
work = ALB.copy()
for i in ORDER:
    place_poster(work, i)
    NIGHT.append(lit(work, L_NIGHT))
WARM = lit(work, L_WARM)
del work, ALB

# ----------------------------------------------------------------------------- phone scene
WW, WH = 2 * W, 2 * H
PW2, PH2, BZ, R_OUT, R_IN = 1120, 2320, 36, 150, 118
SW2, SH2 = PW2 - 2 * BZ, PH2 - 2 * BZ
PCX, PCY = 1080, 2080  # phone centre in world coords
PX, PY = PCX - PW2 // 2, PCY - PH2 // 2


def build_phone():
    fr = Image.new("RGBA", (PW2, PH2), (0, 0, 0, 0))
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle((0, 0, PW2 - 1, PH2 - 1), R_OUT, fill=(16, 16, 18, 255))
    d.rounded_rectangle((3, 3, PW2 - 4, PH2 - 4), R_OUT - 3, outline=(62, 62, 68, 255), width=4)
    hole = rounded_mask(SW2, SH2, R_IN)
    a = np.array(fr)
    hm = np.zeros((PH2, PW2), bool)
    hm[BZ:BZ + SH2, BZ:BZ + SW2] = np.asarray(hole) > 0
    a[..., 3][hm] = 0
    fr = Image.fromarray(a)
    d = ImageDraw.Draw(fr)
    iw, ih = 250, 72
    d.rounded_rectangle((PW2 / 2 - iw / 2, BZ + 26, PW2 / 2 + iw / 2, BZ + 26 + ih), ih // 2, fill=(0, 0, 0, 255))
    return fr


PHONE = build_phone()
SCREEN_MASK = rounded_mask(SW2, SH2, R_IN)
F_STATUS = F_UI(34)


def status_bar(img):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, SW2, 130), fill=(14, 14, 16))
    d.text((110, 62), "23:47", font=F_STATUS, fill=(240, 240, 240), anchor="lm")
    x1 = SW2 - 100
    d.rounded_rectangle((x1 - 62, 47, x1, 77), 9, outline=(230, 230, 230), width=3)
    d.rounded_rectangle((x1 - 56, 53, x1 - 24, 71), 4, fill=(230, 230, 230))
    d.rectangle((x1 + 3, 56, x1 + 8, 68), fill=(230, 230, 230))
    d.rounded_rectangle((SW2 / 2 - 140, SH2 - 32, SW2 / 2 + 140, SH2 - 22), 5, fill=(215, 215, 215))
    return img


COLW = (SW2 - 3 * 28) // 2
THH = int(COLW * A4)


def build_feed():
    seqs = [([1, 3, 0, 4, 2, 5, 1, 3, 0, 4, 2], 150), ([4, 0, 5, 2, 3, 1, 4, 0, 5, 2, 3], 150 - 300)]
    hf = 150 + 11 * (THH + 28) + 200
    feed = Image.new("RGB", (SW2, hf), (14, 14, 16))
    thumbs = [p.resize((COLW, THH), Image.LANCZOS) for p in A4P]
    m = rounded_mask(COLW, THH, 26)
    for col, (seq, y) in enumerate(seqs):
        x = 28 + col * (COLW + 28)
        for k in seq:
            feed.paste(thumbs[k], (x, y), m)
            y += THH + 28
    return feed


FEED = build_feed()


def feed_offset(t):
    return 3600 * ease_out(seg(t, 0.3, 3.1))


def screen_feed(t):
    off = int(feed_offset(t))
    return status_bar(FEED.crop((0, off, SW2, off + SH2)))


def build_open_992():
    sc = Image.new("RGB", (SW2, SH2), (10, 10, 12))
    ph = int(SW2 * A4)
    sc.paste(A4P[1].resize((SW2, ph), Image.LANCZOS), (0, (SH2 - ph) // 2))
    return status_bar(sc)


SCREEN_992 = build_open_992()


def phone_frame(screen, z, cy):
    world = Image.new("RGB", (WW, WH), (7, 7, 9))
    g = screen.resize((40, 86), Image.BILINEAR).filter(ImageFilter.GaussianBlur(5)).resize((1800, 3600), Image.BILINEAR)
    gl = Image.new("RGB", (WW, WH), (0, 0, 0))
    gl.paste(g, (PCX - 900, PCY - 1800))
    world = ImageChops.add(world, ImageEnhance.Brightness(gl).enhance(0.28))
    world.paste(screen, (PX + BZ, PY + BZ), SCREEN_MASK)
    world.paste(PHONE, (PX, PY), PHONE)
    cw, ch = W / z * 2, H / z * 2
    x0, y0 = PCX - cw / 2, cy - ch / 2
    return world.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch), reducing_gap=2.0)


# ----------------------------------------------------------------------------- product shots
def build_studio_bg():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - 540) / 900) ** 2 + ((yy - 900) / 1300) ** 2)
    v = np.clip(1 - r, 0, 1) ** 1.6
    a = np.array([6, 6, 8], np.float32) + v[..., None] * np.array([40, 38, 42], np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


STUDIO = build_studio_bg()


def persp_coeffs(dst, src):
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        B.append(v)
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def quad3d(cx, cy, w, h, theta, f=2400):
    th = math.radians(theta)
    pts = []
    for x, y in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]:
        X, Z = x * math.cos(th), x * math.sin(th)
        s = f / (f + Z)
        pts.append((cx + X * s, cy + y * s))
    return pts


def product_shot(idx, u, rot0, rot1):
    p = A4P[idx]
    pw, ph = p.size
    a = np.asarray(p).astype(np.float32)
    yy, xx = np.mgrid[0:ph, 0:pw].astype(np.float32)
    band = (xx / pw + 0.6 * yy / ph) - lerp(-0.5, 1.9, u)
    a += 255 * 0.20 * np.exp(-band ** 2 / (2 * 0.07 ** 2))[..., None]
    tex = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    sc = lerp(1.0, 1.07, ease_io(u))
    th = lerp(rot0, rot1, ease_io(u))
    hh = 1240 * sc
    q = quad3d(540, 960, hh / A4, hh, th)
    frame = STUDIO.copy()
    sm = Image.new("L", (W // 2, H // 2), 0)
    ImageDraw.Draw(sm).polygon([((x + 26) / 2, (y + 46) / 2) for x, y in q], fill=170)
    sm = sm.filter(ImageFilter.GaussianBlur(18)).resize((W, H), Image.BILINEAR)
    frame.paste((0, 0, 0), (0, 0), sm)
    co = persp_coeffs(q, [(0, 0), (pw, 0), (pw, ph), (0, ph)])
    warped = tex.transform((W, H), Image.Transform.PERSPECTIVE, co, Image.BICUBIC)
    frame.paste(warped, (0, 0), warped)
    return frame


# ----------------------------------------------------------------------------- silhouette
def build_silhouette():
    """Out-of-focus person seen from behind (foreground, shallow depth of field)."""
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    d.ellipse((540 - 78, 1500, 540 + 78, 1690), fill=255)                      # head
    d.polygon([(500, 1650), (580, 1650), (600, 1770), (480, 1770)], fill=255)  # neck
    d.polygon([(480, 1745), (600, 1745), (860, 1830), (960, 1960), (120, 1960), (220, 1830)], fill=255)
    d.ellipse((150, 1790, 330, 1990), fill=255)                                # shoulders
    d.ellipse((750, 1790, 930, 1990), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(11))
    a = np.asarray(m).astype(np.float32) / 255
    sh = np.zeros_like(a)
    sh[9:, 8:] = a[:-9, :-8]
    rim = np.clip(a - sh, 0, 1)
    rim = np.asarray(Image.fromarray((rim * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))).astype(np.float32) / 255
    return a[..., None], rim[..., None]


SIL, RIM = build_silhouette()


def add_silhouette(a, dy):
    dy = int(dy)
    if dy >= H:
        return a
    m = np.zeros_like(SIL)
    r = np.zeros_like(RIM)
    m[dy:] = SIL[:H - dy]
    r[dy:] = RIM[:H - dy]
    a = a * (1 - m) + np.array([0.03, 0.03, 0.035]) * m
    return a + r * 0.9 * np.array([1.0, 0.78, 0.55])


# ----------------------------------------------------------------------------- text
def text_block(lines, cy, gap=18):
    """lines: (text, font, rgb, opacity, tracking, rtl). Returns (rgb, alpha, y0)."""
    probe = ImageDraw.Draw(Image.new("L", (1, 1)))
    items = []
    for text, f, col, op, trk, rtl in lines:
        if rtl:
            bb = probe.textbbox((0, 0), text, font=f, direction="rtl", language="ar")
            w, h = bb[2] - bb[0], bb[3] - bb[1]
        else:
            w = sum(f.getlength(ch) for ch in text) + trk * (len(text) - 1)
            bb = probe.textbbox((0, 0), text, font=f)
            h = bb[3] - bb[1]
        items.append((text, f, col, op, trk, rtl, w, h, bb))
    total = sum(it[7] for it in items) + gap * (len(items) - 1)
    pad = 50
    bh = int(total + 2 * pad)
    tm = Image.new("L", (W, bh), 0)
    rgb = Image.new("RGB", (W, bh), (0, 0, 0))
    y = pad
    for text, f, col, op, trk, rtl, w, h, bb in items:
        x = (W - w) / 2
        lm = Image.new("L", (W, bh), 0)
        dl = ImageDraw.Draw(lm)
        if rtl:
            dl.text((x - bb[0], y - bb[1]), text, font=f, fill=255, direction="rtl", language="ar")
        else:
            cx = x
            for ch in text:
                dl.text((cx, y - bb[1]), ch, font=f, fill=255)
                cx += f.getlength(ch) + trk
        lm = lm.point(lambda v, op=op: int(v * op))
        rgb.paste(col, (0, 0), lm)
        tm = ImageChops.lighter(tm, lm)
        y += h + gap
    shadow = np.asarray(tm.filter(ImageFilter.GaussianBlur(10))).astype(np.float32)[..., None] / 255 * 0.55
    alpha = np.asarray(tm).astype(np.float32)[..., None] / 255
    return np.asarray(rgb).astype(np.float32) / 255, alpha, shadow, int(cy - bh / 2)


def comp_text(a, blk, k, slide=14):
    if k <= 0:
        return a
    rgb, al, sh, y0 = blk
    y0 += int(round(slide * (1 - ease_out(k))))
    h = rgb.shape[0]
    ya, yb = max(0, y0), min(H, y0 + h)
    if ya >= yb:
        return a
    s = slice(ya - y0, yb - y0)
    reg = a[ya:yb]
    reg = reg * (1 - sh[s] * k)
    reg = reg * (1 - al[s] * k) + rgb[s] * al[s] * k
    a[ya:yb] = reg
    return a


T1 = text_block([(TXT_1_AR, F_AR(60), (255, 255, 255), 1, 0, True), (TXT_1_EN, F_LAT(21), (255, 255, 255), 0.72, 4, False)], 300)
T2 = text_block([(TXT_2_AR, F_AR(88), (255, 255, 255), 1, 0, True), (TXT_2_EN, F_LAT(24), (255, 255, 255), 0.75, 5, False)], 960)
T3A = text_block([(TXT_3_AR_A, F_AR(92), (255, 255, 255), 1, 0, True)], 800)
T3B = text_block([(TXT_3_AR_B, F_AR(132), ACCENT, 1, 0, True)], 950, 0)
T3C = text_block([(TXT_3_EN, F_LAT(25), (255, 255, 255), 0.8, 5, False)], 1100)
E_LOGO = text_block([(BRAND, F_LAT(150), (255, 255, 255), 1, 34, False)], 800)
E_AR = text_block([(BRAND_AR, F_AR(74), ACCENT, 1, 0, True)], 945)
E_DROP = text_block([(END_DROP, F_LAT(30), (255, 255, 255), 1, 6, False)], 1095)
E_CTA_AR = text_block([(END_CTA_AR, F_AR5(52), (255, 255, 255), 0.95, 0, True)], 1205)
E_CTA_EN = text_block([(END_CTA_EN, F_LAT(23), (255, 255, 255), 0.7, 5, False)], 1278)
LABELS = [text_block([(n, F_LAT(24), ACCENT, 1, 4, False), (name, F_LAT(34), (255, 255, 255), 1, 3, False)], 0, 10)
          for _, n, name in POSTERS]


def label_at(blk, y):
    rgb, al, sh, _ = blk
    return rgb, al, sh, y


def left_align(blk, x=74):
    """Shift a centred label block to start at x."""
    rgb, al, sh, y0 = blk
    cols = np.where(al[..., 0].max(axis=0) > 0.02)[0]
    dx = x - cols.min()
    return np.roll(rgb, dx, 1), np.roll(al, dx, 1), np.roll(sh, dx, 1), y0


LABELS = [left_align(label_at(b, 160)) for b in LABELS]

# ----------------------------------------------------------------------------- grade
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
_r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
VIG = (1 - 0.42 * np.clip((_r - 0.45) / 0.65, 0, 1) ** 1.5)[..., None].astype(np.float32)
del yy, xx, _r
GRAIN = [(rng.standard_normal((H, W, 1)) * 0.020).astype(np.float32) for _ in range(8)]
SH_T, HI_T = np.array([-0.012, 0.002, 0.020], np.float32), np.array([0.020, 0.007, -0.012], np.float32)


def grade(a, warm):
    a = 0.5 + (a - 0.5) * 1.07
    l = a.mean(axis=2, keepdims=True)
    a = a + (1 - l) * SH_T * (1.2 - warm) + l * HI_T * (0.4 + warm)
    return a * VIG


# ----------------------------------------------------------------------------- timeline
SHOTS = [(0, -10, 4), (3, 9, -3), (2, -7, 5), (5, 8, -4)]  # poster idx, rot start, rot end
SHOT_T0, SHOT_LEN = 7.6, 0.85
PLACE_T = [11.25, 11.70, 12.10, 12.45, 12.75]
FLICK = [0.85, 0.15, 0.0, 0.7, 0.05, 0.0]
BD = slot_center(4)
C992 = slot_center(1)


def wall_reveal_cam(t):
    k = ease_io(seg(t, 14.5, 19.3))
    z = lerp(2.4, 1.03, k)
    cx = lerp(BD[0], 540, k) - 8 * seg(t, 19.3, 23.0)
    cy = lerp(BD[1], 960, k)
    return cx, cy, z


def render(t, fi):
    """Return (float image 0..1, warm, [(text_block, k)], post_multiplier)."""
    texts, mult, warm = [], 1.0, 0.0
    if t < 3.6:  # S1 phone scroll
        k = ease_io(seg(t, 0, 3.6))
        img = phone_frame(screen_feed(t), 1 + 0.06 * k, 1920 + 70 * k)
        texts.append((T1, seg(t, 0.5, 0.9) * (1 - seg(t, 3.1, 3.5))))
        mult = seg(t, 0, 0.4)
    elif t < 5.6:  # S2 empty wall
        img = view(NIGHT[0], 540, 900, 1.0 + 0.06 * seg(t, 3.6, 5.6))
        texts.append((T2, seg(t, 3.8, 4.2) * (1 - seg(t, 5.2, 5.55))))
    elif t < 6.5:  # S3a phone push-in (match cut)
        k = ease_in(seg(t, 5.6, 6.5))
        img = phone_frame(SCREEN_992, lerp(1.06, 1.718, k), lerp(1990, PCY, k))
    elif t < 7.6:  # S3b on the wall, pull back
        k = ease_out(seg(t, 6.5, 7.6))
        img = view(NIGHT[1], 540, lerp(C992[1], 820, k), lerp(3.0, 1.45, k))
        mult = 1 + 0.35 * (1 - seg(t, 6.5, 6.65))
    elif t < 11.0:  # S4 product shots
        n = min(3, int((t - SHOT_T0) / SHOT_LEN))
        u = (t - SHOT_T0 - n * SHOT_LEN) / SHOT_LEN
        idx, r0, r1 = SHOTS[n]
        img = product_shot(idx, u, r0, r1)
        texts.append((LABELS[idx], seg(u, 0.08, 0.3)))
    elif t < 13.6:  # S5 posters go up
        placed = sum(1 for p in PLACE_T if t >= p)
        z = lerp(1.02, 1.05, seg(t, 11.0, 13.6))
        cx, cy = 540, 880
        if placed and t - PLACE_T[placed - 1] < 0.07:
            cx, cy = cx + 3, cy - 2
        img = view(NIGHT[1 + placed], cx, cy, z)
        if placed:
            f = seg(t, PLACE_T[placed - 1], PLACE_T[placed - 1] + 0.1)
            if f < 1:
                img = Image.blend(view(NIGHT[placed], cx, cy, z), img, f)
    elif t < 14.2:  # blackout
        return np.zeros((H, W, 3), np.float32), 0.0, [], 0.0
    elif t < 23.0:  # S7 reveal + S8 text
        warm = 0.6
        cx, cy, z = wall_reveal_cam(t)
        img = view(WARM, cx, cy, z)
        fl = int((t - 14.2) * FPS + 1e-6)
        if fl < len(FLICK):
            mult = FLICK[fl]
        a = np.asarray(img).astype(np.float32) / 255
        a = add_silhouette(a, 700 * (1 - ease_io(seg(t, 14.5, 19.3))))
        if t >= 20.5:
            a *= 1 - 0.62 * ease_io(seg(t, 20.5, 21.0))
            out_k = 1 - seg(t, 22.75, 23.0)
            texts += [(T3A, seg(t, 20.6, 20.9) * out_k), (T3B, seg(t, 21.3, 21.5) * out_k), (T3C, seg(t, 21.6, 21.9) * out_k)]
            mult = 1 - seg(t, 22.8, 23.0)
        return a, warm, texts, mult
    else:  # S9 end card
        img = None
        a = np.asarray(STUDIO).astype(np.float32) / 255 * 0.55
        texts += [(E_LOGO, seg(t, 23.2, 23.55)), (E_AR, seg(t, 23.4, 23.7)), (E_DROP, seg(t, 23.75, 24.05)),
                  (E_CTA_AR, seg(t, 24.0, 24.3)), (E_CTA_EN, seg(t, 24.2, 24.5))]
        lw = int(110 * ease_out(seg(t, 23.5, 23.95)))
        if lw > 0:
            a[1018:1021, 540 - lw:540 + lw] = np.array(ACCENT, np.float32) / 255
        mult = seg(t, 23.0, 23.2) * (1 - seg(t, 26.0, 26.5))
        return a, 0.3, texts, mult
    return np.asarray(img).astype(np.float32) / 255, warm, texts, mult


def make_frame(fi):
    t = fi / FPS
    a, warm, texts, mult = render(t, fi)
    if mult <= 0:
        return np.zeros((H, W, 3), np.uint8)
    a = grade(a, warm)
    for blk, k in texts:
        a = comp_text(a, blk, k)
    a = a * mult + GRAIN[rng.integers(len(GRAIN))] * (0.5 + 0.5 * mult)
    return (np.clip(a, 0, 1) * 255).astype(np.uint8)


# ----------------------------------------------------------------------------- audio
SR = 48000
NA = int(DUR * SR)


def tt(d):
    return np.arange(int(d * SR)) / SR


def noise(d, seed):
    return np.random.default_rng(seed).standard_normal(int(d * SR))


def lp_fft(x, fc, order=2):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** (2 * order)), len(x))


def hp_fft(x, fc, order=2):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    r = (f / fc) ** order
    return np.fft.irfft(X * r / np.sqrt(1 + r ** 2), len(x))


def lp_sweep(x, fc):
    a = np.exp(-2 * np.pi * np.asarray(fc) / SR).tolist()
    xs = x.tolist()
    y = [0.0] * len(xs)
    s1 = s2 = 0.0
    for n in range(len(xs)):
        an = a[n]
        s1 = (1 - an) * xs[n] + an * s1
        s2 = (1 - an) * s1 + an * s2
        y[n] = s2
    return np.array(y)


def impact(size=1.0, dur=2.2, seed=1):
    t = tt(dur)
    f = 36 + 70 * np.exp(-t / 0.09)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (0.5 * size))
    click = lp_fft(noise(dur, seed), 2500) * np.exp(-t / 0.02)
    sub = np.sin(2 * np.pi * 31 * t) * np.exp(-t / (0.8 * size)) * 0.5 * max(0, size - 0.8)
    return np.tanh(1.6 * (body + 0.45 * click + sub))


def whoosh(dur, peak=0.85, seed=2, hi=5000):
    n = int(dur * SR)
    u = np.linspace(0, 1, n)
    env = np.where(u < peak, (u / peak) ** 2, np.clip((1 - u) / (1 - peak), 0, 1) ** 1.5)
    sig = hp_fft(lp_sweep(noise(dur, seed), 250 + hi * env), 180) * env
    pan = np.linspace(-0.7, 0.7, n)
    ang = (pan + 1) * np.pi / 4
    return sig * np.cos(ang) * 1.4, sig * np.sin(ang) * 1.4


def tick(f=1800):
    t = tt(0.06)
    return np.sin(2 * np.pi * f * t) * np.exp(-t / 0.012) + 0.35 * noise(0.06, 5) * np.exp(-t / 0.004)


def switch_click():
    t = tt(0.05)
    one = hp_fft(noise(0.05, 9), 1500) * np.exp(-t / 0.003) + np.sin(2 * np.pi * 3200 * t) * np.exp(-t / 0.006)
    out = np.zeros(int(0.07 * SR))
    out[:len(one)] += one
    out[int(0.013 * SR):int(0.013 * SR) + len(one)] += 0.6 * one[:len(out) - int(0.013 * SR)]
    return out


def thud():
    t = tt(0.25)
    return lp_fft(noise(0.25, 11), 600) * np.exp(-t / 0.04) * 2 + np.sin(2 * np.pi * 110 * t) * np.exp(-t / 0.06)


def thump():
    t = tt(0.35)
    f = 48 + 42 * np.exp(-t / 0.03)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.11)


def drone(dur):
    t = tt(dur)
    s = (np.sin(2 * np.pi * 55 * t) + 0.8 * np.sin(2 * np.pi * 55.4 * t) + 0.5 * np.sin(2 * np.pi * 82.41 * t)
         + 0.3 * np.sin(2 * np.pi * 110.2 * t)) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.21 * t))
    wind = lp_fft(noise(dur, 21), 380) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.13 * t + 1))
    return s * 0.18 + wind * 0.5


def riser(dur):
    t = tt(dur)
    u = t / dur
    nz = hp_fft(lp_sweep(noise(dur, 31), 200 * (30 ** u)), 150)
    tone = np.sin(2 * np.pi * np.cumsum(180 * 4 ** u) / SR) * 0.25
    return (nz + tone) * u ** 2


def buzz(dur):
    t = tt(dur)
    return (np.sin(2 * np.pi * 100 * t) + 0.5 * np.sin(2 * np.pi * 200 * t) + 0.3 * np.sin(2 * np.pi * 300 * t)
            + 0.2 * np.sin(2 * np.pi * 400 * t)) * 0.25


def pad(dur, att=2.5, rel=1.0):
    t = tt(dur)
    s = np.zeros_like(t)
    for f in (110.0, 164.81, 246.94, 261.63, 329.63):
        for d in (-0.35, 0.35):
            s += np.sin(2 * np.pi * (f + d) * t) + 0.15 * np.sin(4 * np.pi * (f + d) * t)
    s /= 10
    env = np.minimum(1, t / att) ** 2 * (1 + 0.08 * np.sin(2 * np.pi * 0.25 * t))
    env *= np.clip((dur - t) / rel, 0, 1)
    return s * env


def shimmer(dur=2.0):
    t = tt(dur)
    s = sum(np.sin(2 * np.pi * f * t * (1 + 0.002 * np.sin(2 * np.pi * 5 * t))) for f in (1318.5, 1760.0, 2637.0))
    return s / 3 * np.exp(-t / 0.6)


def build_audio():
    Lc, Rc = np.zeros(NA), np.zeros(NA)

    def add(sig, t0, g=1.0, sig_r=None):
        i = int(t0 * SR)
        n = min(len(sig), NA - i)
        if n <= 0:
            return
        Lc[i:i + n] += sig[:n] * g
        Rc[i:i + n] += (sig if sig_r is None else sig_r)[:n] * g

    # bed: drone 0 -> 13.6
    d = drone(13.6)
    tdd = tt(13.6)
    d *= np.minimum(1, tdd / 1.2) * (1 + 0.5 * np.exp(-((tdd - 6.3) / 0.5) ** 2))
    add(d, 0, 0.55)
    # scroll ticks
    prev = 0
    for k in range(int(3.2 * 1000)):
        tk = k / 1000
        o = int(feed_offset(tk) // 420)
        if o != prev:
            add(tick(2600) * 0.5, tk, 0.18)
            prev = o
    add(impact(0.4), 3.6, 0.30)
    wl, wr = whoosh(0.75, 0.92, 3)
    add(wl, 5.75, 0.55, wr)
    add(impact(1.0, seed=4), 6.5, 0.9)
    for n in range(4):
        tc = SHOT_T0 + n * SHOT_LEN
        wl, wr = whoosh(0.32, 0.8, 40 + n, 4000)
        add(wl, tc - 0.25, 0.35, wr)
        add(impact(0.35, 1.0, 50 + n), tc, 0.28)
    wl, wr = whoosh(0.32, 0.8, 60, 4000)
    add(wl, 10.75, 0.3, wr)
    add(impact(0.35, 1.0, 61), 11.0, 0.25)
    for p in PLACE_T:
        add(tick(1500), p, 0.35)
        add(thud(), p, 0.45)
    add(riser(2.6), 11.0, 0.5)
    # silence before the light
    Lc[int(13.6 * SR):int(14.2 * SR)] = 0
    Rc[int(13.6 * SR):int(14.2 * SR)] = 0
    add(switch_click(), 13.6, 0.7)
    add(switch_click(), 14.2, 0.8)
    for fl, v in enumerate(FLICK):
        if v > 0.5:
            add(buzz(1 / FPS), 14.2 + fl / FPS, 0.25)
    b = buzz(0.35) * np.linspace(1, 0, int(0.35 * SR))
    add(b, 14.4, 0.2)
    # reveal
    add(impact(1.5, 3.0, 7), 14.5, 1.0)
    add(pad(12.0, 2.5, 0.9), 14.5, 0.55)
    tb = 15.6
    while tb < 22.2:
        add(thump(), tb, 0.55)
        add(thump(), tb + 0.22, 0.38)
        tb += 1.15
    add(impact(0.3, 1.0, 70), 20.6, 0.25)
    add(impact(0.8, 2.0, 71), 21.3, 0.55)
    wl, wr = whoosh(0.45, 0.9, 80)
    add(wl, 22.75, 0.4, wr)
    add(impact(1.1, 2.5, 81), 23.2, 0.85)
    add(shimmer(2.2), 23.2, 0.12)
    add(shimmer(1.6), 23.75, 0.07)
    fade = np.ones(NA)
    i0, i1 = int(26.0 * SR), NA
    fade[i0:i1] = np.linspace(1, 0, i1 - i0)
    Lc *= fade
    Rc *= fade
    st = np.stack([Lc, Rc], 1)
    st = st / (np.abs(st).max() + 1e-9) * 1.15
    st = np.tanh(st) / np.tanh(1.15) * 0.89
    path = os.path.join(OUT, "audio.wav")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())
    return path


# ----------------------------------------------------------------------------- main
def preview():
    times = [1.5, 3.3, 4.6, 6.2, 6.6, 7.4, 8.0, 8.9, 9.7, 10.6, 12.2, 13.4, 14.3, 15.5, 17.5, 20.2, 21.8, 24.6]
    th_w, th_h = 270, 480
    cols = 6
    sheet = Image.new("RGB", (cols * th_w, math.ceil(len(times) / cols) * th_h), (40, 40, 40))
    for n, t in enumerate(times):
        fr = Image.fromarray(make_frame(int(t * FPS)))
        sheet.paste(fr.resize((th_w, th_h), Image.LANCZOS), ((n % cols) * th_w, (n // cols) * th_h))
    p = os.path.join(OUT, "preview.png")
    sheet.save(p)
    print("preview ->", p)


def main():
    if "--preview" in sys.argv:
        preview()
        return
    if "--frame" in sys.argv:
        t = float(sys.argv[sys.argv.index("--frame") + 1])
        p = os.path.join(OUT, f"frame_{t:05.2f}.png")
        Image.fromarray(make_frame(int(t * FPS))).save(p)
        print(p)
        return
    print("rendering audio...")
    wav = build_audio()
    out = os.path.join(OUT, "hayt_drop01.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-maxrate", "9M", "-bufsize", "18M", "-tune", "film",
           "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "192k", "-shortest",
           "-movflags", "+faststart", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(NF):
        proc.stdin.write(make_frame(fi).tobytes())
        if fi % 60 == 0:
            print(f"  frame {fi}/{NF}", flush=True)
    proc.stdin.close()
    proc.wait()
    silent = os.path.join(OUT, "hayt_drop01_no_audio.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-an", "-c:v", "copy", silent], check=True)
    print("done ->", out)


if __name__ == "__main__":
    main()
