#!/usr/bin/env python3
"""
ONELINE - "WANTED" collection film  (vertical 1080x1920, 30 fps, ~29.3 s, 90 BPM)

Story:  "how much is your wall worth?"  ->  wanted posters slam onto the wall in rising
        bounty order while a slot-machine counter adds every bounty
        (B 30,000,000 -> B 20,729,900,000), each cut with a transition matched to the
        character (burn, sword slash, whip, punch, sun-god flash, haki shockwave,
        crows, lightning)  ->  strobe build  ->  "but the most wanted..."  ->  silence  ->
        DROP: the screen burns open on the real wall ("...is your wall.")  ->  total bounty
        ->  ONELINE end card with a Darija question + CTA.

Picture, original epic/hybrid score and all sound design are generated here.
    python3 render.py               # full film -> out/oneline_wanted.mp4 (+ no-audio copy)
    python3 render.py --preview     # contact sheet
    python3 render.py --frame 9.4   # single frame
    python3 render.py --audio       # audio only
"""
import functools
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

# ============================================================================ CONFIG
BRAND = "ONELINE"
COLLECTION = "WANTED COLLECTION — 8 POSTERS"
HOOK = ("how much is", "your wall worth?")
HOOK_AR = "شحال كيسوا الحيط ديالك؟"            # how much is your wall worth?
SCENES = [  # file, epithet, bounty
    ("01_luffy_30m.jpg", "WHERE IT ALL BEGAN", 30_000_000),
    ("02_zoro_daily_world.jpg", "THE PIRATE HUNTER", 320_000_000),
    ("03_nami.jpg", "THE NAVIGATOR", 366_000_000),
    ("04_crocodile.jpg", "THE WARLORD", 1_965_000_000),
    ("05_luffy_gear5.jpg", "THE SUN GOD", 3_000_000_000),
    ("06_shanks.jpg", "THE EMPEROR", 4_048_900_000),
    ("07_itachi.jpg", "THE UCHIHA", 5_000_000_000),
    ("08_dragon.jpg", "THE MOST WANTED MAN", 6_000_000_000),
]
JOLLY = "jolly_roger.jpg"
TRANS = ["slash", "whip_h", "zoom_punch", "sun_flash", "haki", "crows", "lightning"]  # into scenes 2..8
BUILD_TXT = "but the most\nwanted..."
DROP_TXT = "...is your wall."
TAG = "wanted: on your wall."
AR_Q = "شكون فيهم غادي تعلق؟"                  # which one will you hang?
AR_CTA = "صيفط لينا ميساج باش تطلب"            # send us a message to order
EN_CTA = 'DM "WANTED" TO ORDER'
GRID = [5, 4, 7, 1, "J", 6, 3, 0, 2]            # wall slots (J = Jolly Roger sticker)
STROBE = [7, 5, 4, 6, 3, 1]
ACCENT = (255, 59, 48)
CREAM = (238, 224, 198)
GOLD = (226, 178, 98)
# ============================================================================

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
BPM = 90
BEAT = 60 / BPM
BAR = 4 * BEAT
DUR = 11 * BAR
NF = int(round(DUR * FPS))
A4 = 297 / 210
RAQM = ImageFont.Layout.RAQM
rng = np.random.default_rng(21)

T_BURN = 3 * BEAT
CUTS = [BAR + k * 2 * BEAT for k in range(9)]
T_STROBE = CUTS[8]
FLASHES = [T_STROBE, T_STROBE + 0.5 * BEAT] + [T_STROBE + BEAT + k * 0.25 * BEAT for k in range(4)]
T_BUT = T_STROBE + 2 * BEAT
T_FADE = T_STROBE + 3 * BEAT
T_SIL = T_STROBE + 3.5 * BEAT
T_DROP = 6 * BAR
T_OPEN = T_DROP + 0.55
T_FRONT = T_DROP + 5 * BEAT
T_TOTAL = T_DROP + 8 * BEAT
T_TAG = T_DROP + 9 * BEAT
T_END = 9 * BAR
HW = {"slash": 6, "whip_h": 4, "zoom_punch": 4, "sun_flash": 6, "haki": 6, "crows": 8, "lightning": 5}
CUM = list(np.cumsum([s[2] for s in SCENES]).astype(float))
TOTAL = CUM[-1]


def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", name), size, layout_engine=RAQM)


F_FELL = lambda s: font("IMFell.ttf", s)
F_FELL_I = lambda s: font("IMFell-Italic.ttf", s)
F_FELL_SC = lambda s: font("IMFell-SC.ttf", s)
F_DISP = lambda s: font("Anton.ttf", s)
F_UI = lambda s: font("Inter-SemiBold.otf", s)
F_AR = lambda s: font("Cairo-Arabic-700.ttf", s)
F_AR5 = lambda s: font("Cairo-Arabic-500.ttf", s)


# ============================================================================ helpers
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


def to_pil(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def from_pil(im):
    return np.asarray(im.convert("RGB")).astype(np.float32) / 255


def edge_color(im, sides):
    a = np.asarray(im).astype(np.float32)
    e = (np.concatenate([a[:, :4].reshape(-1, 3), a[:, -4:].reshape(-1, 3)]) if sides == "lr"
         else np.concatenate([a[:4].reshape(-1, 3), a[-4:].reshape(-1, 3)]))
    return tuple(int(v) for v in np.median(e, axis=0))


def fit_a4(im):
    """Pad to A4 proportions with the poster's own edge colour."""
    im = im.convert("RGB")
    w, h = im.size
    r = h / w
    if abs(r - A4) < 0.012:
        return im
    if r > A4:
        nw = int(round(h / A4))
        c = Image.new("RGB", (nw, h), edge_color(im, "lr"))
        c.paste(im, ((nw - w) // 2, 0))
        return c
    nh = int(round(w * A4))
    c = Image.new("RGB", (w, nh), edge_color(im, "tb"))
    c.paste(im, (0, (nh - h) // 2))
    return c


def blurred_noise(w, h, radius, seed):
    r = np.random.default_rng(seed)
    a = np.clip(128 + 60 * r.standard_normal((h, w)), 0, 255).astype(np.uint8)
    b = np.asarray(Image.fromarray(a, "L").filter(ImageFilter.GaussianBlur(radius))).astype(np.float32)
    return (b - b.mean()) / (b.std() + 1e-6)


def up_f(arr, size):
    return np.asarray(Image.fromarray(arr.astype(np.float32), "F").resize(size, Image.BILINEAR))


def norm01(a):
    return (a - a.min()) / (a.max() - a.min() + 1e-9)


def box_blur(x, L, axis):
    L = int(L)
    if L < 2:
        return x
    h = L // 2
    pad = [(0, 0)] * x.ndim
    pad[axis] = (h + 1, h + 1)
    c = np.cumsum(np.pad(x, pad, mode="edge"), axis=axis, dtype=np.float32)
    n = x.shape[axis]
    return (np.take(c, np.arange(2 * h + 1, 2 * h + 1 + n), axis=axis) - np.take(c, np.arange(n), axis=axis)) / (2 * h + 1)


def zscale(a, s, cx=W / 2, cy=H / 2):
    if abs(s - 1) < 1e-3:
        return a
    bw, bh = W / s, H / s
    return from_pil(to_pil(a).resize((W, H), Image.BILINEAR, box=(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2)))


def shift(a, dx, dy):
    dx, dy = int(round(dx)), int(round(dy))
    out = np.zeros_like(a)
    hh, ww = a.shape[:2]
    ys, yd = (slice(0, hh - dy), slice(dy, hh)) if dy >= 0 else (slice(-dy, hh), slice(0, hh + dy))
    xs, xd = (slice(0, ww - dx), slice(dx, ww)) if dx >= 0 else (slice(-dx, ww), slice(0, ww + dx))
    out[yd, xd] = a[ys, xs]
    return out


def jolt(a, dx, dy):
    return np.roll(np.roll(a, int(round(dy)), 0), int(round(dx)), 1)


def persp_coeffs(dst, src):
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        B.append(v)
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def quad3d(cx, cy, w, h, yaw, roll=0.0, f=2400):
    th, ro = math.radians(yaw), math.radians(roll)
    pts = []
    for x, y in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]:
        x, y = x * math.cos(ro) - y * math.sin(ro), x * math.sin(ro) + y * math.cos(ro)
        X, Z = x * math.cos(th), x * math.sin(th)
        s = f / (f + Z)
        pts.append((cx + X * s, cy + y * s))
    return pts


# ============================================================================ assets
A4P = [fit_a4(Image.open(os.path.join(HERE, "posters", f))) for f, _, _ in SCENES]


def load_jolly():
    im = Image.open(os.path.join(HERE, "posters", JOLLY)).convert("RGB")
    w, h = im.size
    tmp = im.copy()
    for c in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]:
        ImageDraw.floodfill(tmp, c, (255, 0, 255), thresh=12)
    a = np.asarray(tmp)
    m = ~((a[..., 0] == 255) & (a[..., 1] == 0) & (a[..., 2] == 255))
    out = im.convert("RGBA")
    out.putalpha(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0)))
    return out


JOLLY_IMG = load_jolly()


class Words:
    """Word-by-word 'rise from a slit' typography."""

    def __init__(self, text, fnt, color=(255, 255, 255), cy=960, x=None, tracking=0, red_dot=True,
                 rtl=False, lh=1.08, shadow=0.55, opacity=1.0, single=False, scale=1):
        self.items = []
        self.shadow = shadow
        asc, desc = fnt.getmetrics()
        p = int(30 * scale)
        lines = text.split("\n")
        line_h = (asc + desc) * lh
        top = cy - line_h * len(lines) / 2
        probe = ImageDraw.Draw(Image.new("L", (1, 1)))
        for li, line in enumerate(lines):
            words = [line] if (single or rtl) else line.split(" ")
            if rtl:
                widths = [probe.textlength(line, font=fnt, direction="rtl", language="ar")]
            else:
                widths = [sum(fnt.getlength(c) for c in w_) + tracking * (len(w_) - 1) for w_ in words]
            sp = fnt.getlength(" ") + tracking
            total = sum(widths) + sp * (len(words) - 1)
            xx = (W * scale - total) / 2 if x is None else x
            yy = top + li * line_h
            for w_, wd in zip(words, widths):
                iw, ih = int(wd + 2 * p + 4), int(asc + desc + 2 * p)
                al = Image.new("L", (iw, ih), 0)
                rgb = Image.new("RGB", (iw, ih), color)
                d = ImageDraw.Draw(al)
                if rtl:
                    d.text((p, p + asc), w_, font=fnt, fill=255, anchor="ls", direction="rtl", language="ar")
                else:
                    cx_ = p
                    for ci, ch in enumerate(w_):
                        d.text((cx_, p + asc), ch, font=fnt, fill=255, anchor="ls")
                        if red_dot and ch == "." and ci == len(w_) - 1:
                            m = Image.new("L", (iw, ih), 0)
                            ImageDraw.Draw(m).text((cx_, p + asc), ch, font=fnt, fill=255, anchor="ls")
                            rgb.paste(ACCENT, (0, 0), m)
                        cx_ += fnt.getlength(ch) + tracking
                a = np.asarray(al).astype(np.float32)[..., None] / 255 * opacity
                sh = np.asarray(al.filter(ImageFilter.GaussianBlur(9 * scale))).astype(np.float32)[..., None] / 255
                self.items.append((np.asarray(rgb).astype(np.float32) / 255, a, sh, int(xx - p), int(yy - p), p + asc + desc))
                xx += wd + sp

    def draw(self, a, t, t_in, stagger=0.06, rise=0.34, t_out=None, out=0.2, k_extra=1.0):
        if t < t_in:
            return a
        ko = 1.0 if t_out is None else 1 - seg(t, t_out, t_out + out)
        if ko <= 0:
            return a
        Hh, Ww = a.shape[:2]
        for j, (rgb, al, sh, x0, y0, clip_b) in enumerate(self.items):
            q = (t - t_in - j * stagger) / rise
            if q <= 0:
                continue
            e = ease_out(q)
            dy = int(round((1 - e) * clip_b * 0.85))
            k = min(1.0, q * 1.6) * ko * k_extra
            vis = clip_b + int(0.4 * (al.shape[0] - clip_b)) - dy
            if vis <= 0:
                continue
            ys, xs = y0 + dy, x0
            r1 = min(vis, al.shape[0])
            ya, yb = max(0, ys), min(Hh, ys + r1)
            xa, xb = max(0, xs), min(Ww, xs + al.shape[1])
            if ya >= yb or xa >= xb:
                continue
            sr, sc = slice(ya - ys, yb - ys), slice(xa - xs, xb - xs)
            reg = a[ya:yb, xa:xb]
            reg *= 1 - sh[sr, sc] * self.shadow * k
            al_ = al[sr, sc] * k
            reg[:] = reg * (1 - al_) + rgb[sr, sc] * al_
        return a


# ---------------------------------------------------------------------------- embers / smoke / grade
NE = 95
E_X, E_Y = rng.uniform(0, W, NE), rng.uniform(0, H + 200, NE)
E_S, E_PH = rng.uniform(70, 220, NE), rng.uniform(0, 6.28, NE)
E_I, E_K = rng.uniform(0.35, 1.1, NE), rng.integers(0, 4, NE)
E_C = [np.array(c, np.float32) for c in ((1.0, 0.55, 0.15), (1.0, 0.78, 0.35), (1.0, 0.38, 0.10), (1.0, 0.62, 0.22))]
E_COL = rng.integers(0, 4, NE)
ESPR = []
for sx, sy in ((1.0, 2.2), (1.4, 3.5), (1.8, 5.0), (2.4, 2.4)):
    rx, ry = int(math.ceil(3 * sx)), int(math.ceil(3 * sy))
    yy_, xx_ = np.mgrid[-ry:ry + 1, -rx:rx + 1]
    ESPR.append(np.exp(-(xx_ ** 2 / (2 * sx ** 2) + yy_ ** 2 / (2 * sy ** 2))).astype(np.float32)[..., None])


def embers(a, t, amt=1.0):
    if amt <= 0:
        return a
    for i in range(NE):
        s = ESPR[E_K[i]]
        ry, rx = s.shape[0] // 2, s.shape[1] // 2
        x = int((E_X[i] + 40 * math.sin(0.8 * t + E_PH[i])) % W)
        y = int((E_Y[i] - E_S[i] * t) % (H + 200)) - 100
        if rx <= x < W - rx and ry <= y < H - ry:
            fl = 0.55 + 0.45 * math.sin(9 * t + E_PH[i] * 3)
            a[y - ry:y + ry + 1, x - rx:x + rx + 1] += s * E_C[E_COL[i]] * E_I[i] * amt * fl
    return a


SMOKE = norm01(blurred_noise(W // 4, H // 2, 10, 33) + 0.6 * blurred_noise(W // 4, H // 2, 4, 34))
SMOKE_COL = np.array([0.85, 0.72, 0.58], np.float32)


def smoke(a, t, amt=1.0):
    off = int((t * 18) % (H // 4))
    win = SMOKE[off:off + H // 4]
    s = up_f(win, (W, H))[..., None]
    return a + (s ** 2) * SMOKE_COL * 0.10 * amt


yy_, xx_ = np.mgrid[0:H, 0:W].astype(np.float32)
_r = np.sqrt(((xx_ - W / 2) / (W * 0.62)) ** 2 + ((yy_ - H / 2) / (H * 0.62)) ** 2)
VIG = (1 - 0.55 * np.clip((_r - 0.40) / 0.70, 0, 1) ** 1.4)[..., None].astype(np.float32)
NZ = norm01(0.6 * up_f(blurred_noise(W // 8, H // 8, 2, 41), (W, H)) + 0.4 * up_f(blurred_noise(W // 3, H // 3, 2, 42), (W, H)))
BURN_UP = norm01(0.62 * (yy_ / H) + 0.38 * NZ)[..., None].astype(np.float32)
_rad = np.sqrt((xx_ - W / 2) ** 2 + (yy_ - H / 2) ** 2)
BURN_RAD = norm01(0.66 * _rad / _rad.max() + 0.34 * NZ)[..., None].astype(np.float32)
_ang = math.radians(-24)
SLASH_D = ((xx_ - W / 2) * math.sin(_ang) - (yy_ - H / 2) * math.cos(_ang))[..., None].astype(np.float32)
SLASH_S = ((xx_ - W / 2) * math.cos(_ang) + (yy_ - H / 2) * math.sin(_ang))[..., None].astype(np.float32)
_th = np.arctan2(yy_ - H / 2, xx_ - W / 2)
RAYS = (((0.5 + 0.5 * np.cos(18 * _th + 2 * np.sin(5 * _th))) ** 6) * np.exp(-_rad / 900) + np.exp(-_rad / 260))[..., None].astype(np.float32)
RR = _rad.astype(np.float32)
UX = ((xx_ - W / 2) / (_rad + 1e-6)).astype(np.float32)
UY = ((yy_ - H / 2) / (_rad + 1e-6)).astype(np.float32)
XX, YY = xx_.astype(np.float32), yy_.astype(np.float32)
del _r, _rad, _th
GRAIN = [(rng.standard_normal((H, W, 1)) * 0.024).astype(np.float32) for _ in range(8)]
SH_T = np.array([-0.012, 0.006, 0.018], np.float32)
HI_T = np.array([0.032, 0.010, -0.022], np.float32)


def bloom(a, strength):
    sm = to_pil(a).resize((W // 8, H // 8), Image.BILINEAR)
    b = np.clip(from_pil(sm) - 0.6, 0, 1)
    b = from_pil(to_pil(b * 2.5).filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BILINEAR)) / 2.5
    return a + b * strength


def grade(a):
    a = a * 0.95 + 0.02
    a = 0.5 + (a - 0.5) * 1.08
    l = a.mean(axis=2, keepdims=True)
    a = a + (1 - l) * SH_T + l * HI_T
    return a * VIG


# ============================================================================ wood
def wood(wu, hu, scale, plank=150, seed=3, dark=1.0):
    w, h = wu * scale, hu * scale
    r = np.random.default_rng(seed)
    g = up_f(blurred_noise(max(8, wu // 3), max(8, hu // 40), 1, seed), (w, h))
    fine = up_f(blurred_noise(wu // 2, hu // 6, 0.6, seed + 1), (w, h))
    xs = np.arange(w) / scale
    pidx = (xs // plank).astype(int)
    pf = r.uniform(0.78, 1.12, pidx.max() + 2)[pidx]
    gap = 1 - 0.7 * np.exp(-((xs % plank) / 2.2) ** 2) - 0.7 * np.exp(-((plank - xs % plank) / 2.2) ** 2)
    base = np.array([96, 62, 40], np.float32) * dark
    a = base[None, None, :] * ((1 + 0.16 * g + 0.06 * fine) * (pf * gap)[None, :])[..., None]
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(int(wu * hu / 260000)):
        kx, ky = r.uniform(0, w), r.uniform(0, h)
        rx, ry = r.uniform(8, 18) * scale, r.uniform(16, 40) * scale
        d.ellipse((kx - rx, ky - ry, kx + rx, ky + ry), fill=(20, 10, 5, 110))
    return img.filter(ImageFilter.GaussianBlur(0.6 * scale))


HOOK_BG = None


def hook_bg():
    global HOOK_BG
    if HOOK_BG is None:
        a = from_pil(wood(W, H, 1, seed=7, dark=0.8))
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        L = 0.12 + 0.75 * np.exp(-((xx - 540) ** 2 + (yy - 820) ** 2) / (2 * 620 ** 2))
        HOOK_BG = a * L[..., None] * np.array([1.05, 0.9, 0.75], np.float32)
    return HOOK_BG


# ============================================================================ counter (odometer)
CF = F_DISP(84)
CW_ = int(max(CF.getlength(str(d)) for d in range(10))) + 4
CH_ = 104


def digit_strip(fnt, cw, ch):
    s = Image.new("L", (cw, ch * 11), 0)
    d = ImageDraw.Draw(s)
    for i, dg in enumerate("01234567890"):
        d.text((cw / 2, i * ch + ch / 2), dg, font=fnt, fill=255, anchor="mm")
    return s


STRIP = digit_strip(CF, CW_, CH_)


def counter_img(V, scale=1.0, rand_seed=None):
    """Render 'B 00,000,000,000' odometer -> (rgb float, alpha float)."""
    comma_w = int(CW_ * 0.42)
    sym_w = int(CW_ * 1.25)
    width = sym_w + 11 * CW_ + 3 * comma_w + 10
    al = Image.new("L", (width, CH_), 0)
    dim = Image.new("L", (width, CH_), 0)
    d = ImageDraw.Draw(al)
    # berry symbol
    d.text((sym_w * 0.45, CH_ / 2), "B", font=CF, fill=255, anchor="mm")
    bw = max(3, int(CW_ * 0.09))
    for fx in (0.32, 0.52):
        x = int(sym_w * 0.45 - CW_ * 0.5 + CW_ * fx + CW_ * 0.08)
        d.rectangle((x, int(CH_ * 0.08), x + bw, int(CH_ * 0.92)), fill=255)
    r = np.random.default_rng(rand_seed) if rand_seed is not None else None
    pos = [V % 10]  # true odometer: each digit turns only while the digit below it passes 9 -> 0
    for k in range(1, 11):
        pos.append((math.floor(V / 10 ** k) % 10 + max(0.0, pos[k - 1] - 9)) % 10)
    x = sym_w + 10
    for k in range(10, -1, -1):
        p = r.uniform(0, 10) if r is not None else pos[k]
        crop = STRIP.crop((0, int(p * CH_), CW_, int(p * CH_) + CH_))
        lead = (r is None) and (k > 0) and (V < 10 ** k - 0.5)
        (dim if lead else al).paste(crop, (x, 0), crop)
        x += CW_
        if k in (9, 6, 3):
            ImageDraw.Draw(dim if lead else al).text((x + comma_w / 2, CH_ / 2), ",", font=CF, fill=255, anchor="mm")
            x += comma_w
    alpha = np.maximum(np.asarray(al).astype(np.float32), np.asarray(dim).astype(np.float32) * 0.2) / 255
    if scale != 1.0:
        im = Image.fromarray((alpha * 255).astype(np.uint8)).resize((int(width * scale), int(CH_ * scale)), Image.BICUBIC)
        alpha = np.asarray(im).astype(np.float32) / 255
    return alpha[..., None]


def draw_alpha(a, alpha, cx, cy, color, k=1.0, shadow=0.6):
    h, w = alpha.shape[:2]
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    xa, xb, ya, yb = max(0, x0), min(W, x0 + w), max(0, y0), min(H, y0 + h)
    if xa >= xb or ya >= yb:
        return a
    al = alpha[ya - y0:yb - y0, xa - x0:xb - x0] * k
    reg = a[ya:yb, xa:xb]
    if shadow:
        sh = from_pil(to_pil(np.repeat(al, 3, 2)).filter(ImageFilter.GaussianBlur(8)))[..., :1]
        reg *= 1 - sh * shadow
    reg[:] = reg * (1 - al) + np.array(color, np.float32) / 255 * al
    return a


def counter_value(t):
    if t < CUTS[0] + 0.15:
        return 0.0
    k = min(7, sum(1 for c in CUTS[:8] if t >= c + 0.15) - 1)
    prev = CUM[k - 1] if k > 0 else 0.0
    q = ease_out(seg(t, CUTS[k] + 0.15, CUTS[k] + 1.0))
    return prev + (CUM[k] - prev) * q


LBL = Words("YOUR WALL'S BOUNTY", F_UI(19), CREAM, cy=1478, tracking=6, red_dot=False, shadow=0.5, single=True, opacity=0.6)
HDR_L = Words(BRAND, F_DISP(34), (255, 255, 255), cy=150, x=70, shadow=0.4, red_dot=False, single=True, opacity=0.92)
HDR_R = [Words(f"WANTED  {i + 1:02d}/08", F_UI(20), CREAM, cy=150, x=800, tracking=4, shadow=0.4, red_dot=False,
               single=True, opacity=0.8) for i in range(8)]


def hud(a, t):
    """Persistent overlay (not affected by transitions): header + bounty counter."""
    if t < 2 * BEAT or t >= T_BUT:
        return a
    k_in = seg(t, 2 * BEAT, 2 * BEAT + 0.25)
    if t >= CUTS[0]:
        sc = max(0, min(7, sum(1 for c in CUTS[1:8] if t >= c)))
        HDR_L.draw(a, t, -1, rise=0.01)
        HDR_R[sc].draw(a, t, -1, rise=0.01)
    LBL.draw(a, t, 2 * BEAT, rise=0.3)
    if t >= T_STROBE:
        fr = int(t * FPS)
        al = counter_img(0, rand_seed=fr) if t < FLASHES[-1] + 0.1 else counter_img(TOTAL)
    else:
        al = counter_img(counter_value(t))
    pop = 1.0
    for c in CUTS[:8]:
        if c + 0.9 <= t < c + 1.15:
            pop = 1 + 0.06 * math.sin(math.pi * (t - c - 0.9) / 0.25)
    if pop != 1.0:
        al = np.asarray(to_pil(np.repeat(al, 3, 2)).resize((int(al.shape[1] * pop), int(al.shape[0] * pop)), Image.BICUBIC)).astype(np.float32)[..., :1] / 255
    return draw_alpha(a, al, W / 2, 1545, CREAM, k_in)


# ============================================================================ montage
def make_bg(p):
    tw, th = int(W * 1.25), int(H * 1.25)
    s = max(tw / p.width, th / p.height)
    im = p.resize((int(p.width * s) + 2, int(p.height * s) + 2), Image.BILINEAR)
    im = im.crop(((im.width - tw) // 2, (im.height - th) // 2, (im.width - tw) // 2 + tw, (im.height - th) // 2 + th))
    im = im.resize((tw // 5, th // 5), Image.BILINEAR).filter(ImageFilter.GaussianBlur(9)).resize((tw, th), Image.BILINEAR)
    return ImageEnhance.Color(ImageEnhance.Brightness(im).enhance(0.30)).enhance(1.1)


BGS = [make_bg(p) for p in A4P]
EPI = [Words(e, F_FELL_SC(54), GOLD, cy=1405, tracking=3, red_dot=False, shadow=0.7) for _, e, _ in SCENES]
CARD_MOVES = [(-8, 3, -1.2, 0.4), (7, -3, 1.0, -0.4), (-6, 4, 0.8, -0.8), (7, -4, -0.8, 0.5),
              (-7, 3, 1.0, -0.6), (6, -5, -0.6, 0.8), (-7, 4, 1.2, 0.0), (6, -3, -1.0, 0.4)]


def card(a, p, cx, cy, hh, yaw, roll, sweep, nail=True):
    pw, ph = p.size
    tex = np.asarray(p).astype(np.float32)
    yy, xx = np.mgrid[0:ph, 0:pw].astype(np.float32)
    band = (xx / pw + 0.6 * yy / ph) - sweep
    tex = tex + 255 * 0.13 * np.exp(-band ** 2 / (2 * 0.08 ** 2))[..., None]
    tex = Image.fromarray(np.clip(tex, 0, 255).astype(np.uint8)).convert("RGBA")
    q = quad3d(cx, cy, hh / A4, hh, yaw, roll)
    sm = Image.new("L", (W // 2, H // 2), 0)
    ImageDraw.Draw(sm).polygon([((x + 24) / 2, (y + 44) / 2) for x, y in q], fill=200)
    sm = np.asarray(sm.filter(ImageFilter.GaussianBlur(20)).resize((W, H), Image.BILINEAR)).astype(np.float32)[..., None] / 255
    a *= 1 - sm
    co = persp_coeffs(q, [(0, 0), (pw, 0), (pw, ph), (0, ph)])
    wp = tex.transform((W, H), Image.Transform.PERSPECTIVE, co, Image.BICUBIC)
    wa = np.asarray(wp).astype(np.float32) / 255
    al = wa[..., 3:4]
    a[:] = a * (1 - al) + wa[..., :3] * al
    if nail:
        nx, ny = (q[0][0] + q[1][0]) / 2, (q[0][1] + q[1][1]) / 2 + 26
        yy2, xx2 = np.mgrid[-16:17, -16:17].astype(np.float32)
        d2 = np.sqrt(xx2 ** 2 + yy2 ** 2)
        disc = np.clip(10.5 - d2, 0, 1)[..., None]
        shade = (0.25 + 0.55 * np.clip(1 - np.sqrt((xx2 + 4) ** 2 + (yy2 + 4) ** 2) / 9, 0, 1))[..., None]
        sh = np.clip(12 - np.sqrt((xx2 - 3) ** 2 + (yy2 - 4) ** 2), 0, 1)[..., None] * 0.5
        x0, y0 = int(nx) - 16, int(ny) - 16
        if 0 <= x0 and x0 + 33 <= W and 0 <= y0 and y0 + 33 <= H:
            reg = a[y0:y0 + 33, x0:x0 + 33]
            reg *= 1 - sh
            reg[:] = reg * (1 - disc) + shade * np.array([0.78, 0.76, 0.72], np.float32) * disc
    return a


def bg_view(i, u, dx=0.0, dy=0.0):
    im = BGS[i]
    z = 1.18 + 0.06 * u
    bw, bh = im.width / z, im.height / z
    cx, cy = im.width / 2 + dx, im.height / 2 + dy
    return from_pil(im.resize((W, H), Image.BILINEAR, box=(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2)))


def montage_frame(k, t):
    c = CUTS[k]
    u = max(-0.6, min(1.6, (t - c) / (2 * BEAT)))
    a = bg_view(k, u, 20 * math.sin(k + u), 30 * u)
    a = smoke(a, t, 0.8)
    y0, y1, r0, r1 = CARD_MOVES[k]
    q = (t - c) / 0.16
    slam = 1.10 if q < 0 else 1 + 0.10 * (1 - ease_out(q))
    card(a, A4P[k], 540, 800, 1080 * (1 + 0.045 * u) * slam, lerp(y0, y1, u), lerp(r0, r1, u), lerp(-0.5, 1.9, u))
    embers(a, t, 0.7)
    EPI[k].draw(a, t, c + 0.12, stagger=0.06, rise=0.36)
    if c + 0.1 <= t < c + 0.32:
        amp = 9 * (1 - (t - c - 0.1) / 0.22)
        a = jolt(a, amp * math.sin(t * 95), amp * math.cos(t * 81))
    return a


def strobe_frame(f, t):
    i = STROBE[f]
    r = np.random.default_rng(700 + f)
    u = (t - FLASHES[f]) / 0.33
    a = bg_view(i, u, r.uniform(-40, 40), r.uniform(-40, 40))
    card(a, A4P[i], 540 + r.uniform(-15, 15), 820 + r.uniform(-20, 20), 1230 * (1 + 0.06 * u),
         r.uniform(-12, 12), r.uniform(-5, 5), lerp(-0.4, 1.6, u))
    embers(a, t, 1.0)
    fr = int((t - FLASHES[f]) * FPS + 1e-6)
    return a * (1.6 if fr == 0 else 1.2 if fr == 1 else 1.0)


# ============================================================================ hook / build texts
HOOK_W = [Words(HOOK[0], F_FELL_I(146), CREAM, cy=730, shadow=0.7, red_dot=False),
          Words(HOOK[1], F_FELL_I(146), CREAM, cy=895, shadow=0.7, red_dot=False)]
HOOK_A = Words(HOOK_AR, F_AR5(52), CREAM, cy=1050, rtl=True, shadow=0.7, opacity=0.85)
BUILD_W = Words(BUILD_TXT, F_FELL_I(140), CREAM, cy=900, shadow=0.7, red_dot=False)
DROP_W = Words(DROP_TXT, F_FELL_I(118), CREAM, cy=1480, shadow=0.85)


def hook_frame(t):
    a = hook_bg().copy()
    a = smoke(a, t, 1.0)
    embers(a, t, 0.8)
    HOOK_W[0].draw(a, t, 0.10, stagger=0.12, rise=0.4)
    HOOK_W[1].draw(a, t, 0.45, stagger=0.12, rise=0.4)
    HOOK_A.draw(a, t, 1.0, rise=0.4)
    for tb in (0.0, BEAT, 2 * BEAT):  # taiko pulses -> light pulses
        if 0 <= t - tb < 0.25:
            a = a * (1 + 0.18 * (1 - (t - tb) / 0.25))
    return a


def build_frame(t):
    a = hook_bg().copy() * 0.8
    a = smoke(a, t, 1.2)
    z = 1 + 0.05 * seg(t, T_BUT, T_SIL)
    a = zscale(a, z)
    embers(a, t, 1.0 * (1 - seg(t, T_FADE, T_SIL)))
    BUILD_W.draw(a, t, T_BUT + 0.05, stagger=0.1, rise=0.4)
    return a * (1 - ease_in(seg(t, T_FADE, T_SIL)))


# ============================================================================ transitions
def tr_whip(A, B, p, axis):
    e = ease_io(p)
    de = (ease_io(min(1, p + 0.02)) - ease_io(max(0, p - 0.02))) / 0.04
    n = W if axis == 1 else H
    canvas = np.concatenate([A, B], axis=axis)
    off = int(e * n)
    L = int(de * n / 7)
    lo, hi = max(0, off - L), min(2 * n, off + n + L)
    reg = box_blur(np.take(canvas, np.arange(lo, hi), axis=axis), L, axis)
    return np.take(reg, np.arange(off - lo, off - lo + n), axis=axis)


def radial(a, s, amount):
    acc = np.zeros_like(a)
    for i in range(4):
        acc += zscale(a, s * (1 + amount * i))
    return acc / 4


def rgb_split(a, d):
    d = int(d)
    if d == 0:
        return a
    out = a.copy()
    out[..., 0] = np.roll(a[..., 0], d, 1)
    out[..., 2] = np.roll(a[..., 2], -d, 1)
    return out


def tr_zoom(A, B, p):
    if p < 0.5:
        q = p * 2
        return rgb_split(radial(A, 1 + 0.7 * ease_in(q), 0.03 * q), 16 * q) * (1 + 0.45 * ease_in(q))
    q = p * 2 - 1
    return rgb_split(radial(B, 1 + 0.3 * (1 - ease_out(q)), 0.03 * (1 - q)), 16 * (1 - q)) * (1 + 0.45 * (1 - q))


FIRE = np.array([1.35, 0.62, 0.16], np.float32)


def tr_burn(A, B, p, field):
    e = lerp(-0.06, 1.06, p)
    mb = np.clip((e - field) / 0.01 + 0.5, 0, 1)
    edge = np.exp(-((field - e) / 0.016) ** 2)
    char = np.clip(1 - (field - e) / 0.07, 0, 1) * (field > e)
    out = A * (1 - 0.8 * char) * (1 - mb) + B * mb
    return out + edge * FIRE * 1.3


def tr_slash(A, B, p):
    if p < 0.4:
        q = ease_out(p / 0.4)
        front = lerp(-1200, 1200, q)
        on = (SLASH_S < front).astype(np.float32)
        core = np.exp(-(SLASH_D / 2.5) ** 2) * on
        glow = np.exp(-(SLASH_D / 20) ** 2) * on * 0.55
        return A + (core * 1.6 + glow) * np.array([1.0, 0.97, 0.92], np.float32)
    q = (p - 0.4) / 0.6
    off = ease_in(q) * 760
    nx, ny = math.sin(_ang), -math.cos(_ang)
    ml = np.clip(SLASH_D / 1.5 + 0.5, 0, 1)
    mu = 1 - ml
    out = B.copy()
    for m, sgn in ((ml, 1), (mu, -1)):
        dx, dy = sgn * off * nx, sgn * off * ny
        out = out * (1 - shift(m, dx, dy)) + shift(A * m, dx, dy)
    return out + max(0, 1 - q / 0.15) * 0.7


def tr_sun(A, B, p):
    if p < 0.5:
        q = p * 2
        base, w = zscale(A, 1 + 0.25 * ease_in(q)), ease_in(q)
    else:
        q = p * 2 - 1
        base, w = zscale(B, 1 + 0.25 * (1 - ease_out(q))), 1 - ease_out(q)
    light = (0.85 + 0.5 * RAYS) * np.array([1.0, 0.96, 0.88], np.float32)
    return base * (1 - 0.92 * w) + light * w


def bolt_img(seed, w=6, col=(1.0, 0.95, 1.0), glow_col=(0.6, 0.7, 1.0), branches=3):
    r = np.random.default_rng(seed)
    core = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(core)

    def path(x, y, length, ang, width, depth):
        pts = [(x, y)]
        n = int(length / 40)
        for _ in range(n):
            ang += r.uniform(-0.5, 0.5)
            x += 40 * math.sin(ang)
            y += 40 * math.cos(ang)
            pts.append((x, y))
            if depth < 2 and r.random() < 0.08:
                path(x, y, length * 0.35, ang + r.choice([-1, 1]) * r.uniform(0.5, 1.0), max(2, width // 2), depth + 1)
        d.line(pts, fill=255, width=width)

    path(r.uniform(300, 780), -20, 2100, r.uniform(-0.2, 0.2), w, 0)
    c = np.asarray(core.filter(ImageFilter.GaussianBlur(1))).astype(np.float32)[..., None] / 255
    g = np.asarray(core.filter(ImageFilter.GaussianBlur(22))).astype(np.float32)[..., None] / 255 * 3
    return c * np.array(col, np.float32) * 1.6 + np.clip(g, 0, 1) * np.array(glow_col, np.float32)


BOLT_A = bolt_img(5)
BOLT_B = bolt_img(9)
HAKI_A = bolt_img(13, 8, (0.05, 0.0, 0.0), (1.0, 0.1, 0.08))
HAKI_B = bolt_img(17, 7, (0.05, 0.0, 0.0), (1.0, 0.12, 0.1))


def tr_lightning(A, B, p):
    if p < 0.3:
        return A * (1 - 0.4 * p / 0.3) * np.array([0.9, 0.95, 1.08], np.float32)
    if p < 0.38:
        return np.clip(A * 0.4 + 0.75, 0, 2) + BOLT_A
    if p < 0.5:
        return A * 0.28 + BOLT_A * 0.25
    if p < 0.6:
        return np.clip(B * 0.5 + 0.8, 0, 2) + BOLT_B
    q = (p - 0.6) / 0.4
    return B * (1 + 0.5 * (1 - q)) + BOLT_B * (1 - q) * 0.8


def ripple(a, R, amp):
    disp = amp * np.exp(-((RR - R) / 110) ** 2) * np.sin((RR - R) / 24)
    sx = np.clip(XX - UX * disp, 0, W - 1).astype(np.int32)
    sy = np.clip(YY - UY * disp, 0, H - 1).astype(np.int32)
    return a[sy, sx]


def tr_haki(A, B, p):
    if p < 0.42:
        q = p / 0.42
        amp = 16 * q
        out = jolt(A, amp * math.sin(q * 70), amp * math.cos(q * 53))
        l = out.mean(axis=2, keepdims=True)
        out = (out * (1 - 0.6 * q) + l * 0.6 * q) * (1 - 0.45 * q) * np.array([1.1, 0.9, 0.9], np.float32)
        return out
    if p < 0.6:
        return np.zeros((H, W, 3), np.float32) + (HAKI_A if p < 0.51 else HAKI_B)
    q = (p - 0.6) / 0.4
    out = ripple(B, lerp(0, 1500, ease_out(q)), 34 * (1 - q))
    amp = 12 * (1 - q)
    return jolt(out, amp * math.sin(q * 60), amp * math.cos(q * 47)) + HAKI_B * (1 - q) * 0.4


FEATH = [(rng.uniform(-200, H + 200), rng.uniform(0.0, 0.5), rng.uniform(70, 190), rng.uniform(-0.6, 0.6),
          rng.uniform(0, 6.28)) for _ in range(85)]


def tr_crows(A, B, p):
    m = Image.new("L", (W // 2, H // 2), 0)
    d = ImageDraw.Draw(m)
    for y0, s0, size, ang, ph in FEATH:
        u = (p - s0) / 0.5
        if not 0 <= u <= 1:
            continue
        x = lerp(W + 300, -300, u)
        y = y0 + 60 * math.sin(u * 6 + ph)
        rx, ry = size, size * 0.3
        pts = [((x + rx * math.cos(th) * math.cos(ang) - ry * math.sin(th) * math.sin(ang)) / 2,
                (y + rx * math.cos(th) * math.sin(ang) + ry * math.sin(th) * math.cos(ang)) / 2)
               for th in np.linspace(0, 2 * math.pi, 18)]
        d.polygon(pts, fill=255)
    M = np.asarray(m.filter(ImageFilter.GaussianBlur(2.5)).resize((W, H), Image.BILINEAR)).astype(np.float32)[..., None] / 255
    M = np.maximum(M, clamp01(1 - abs(p - 0.5) / 0.1))
    return (A if p < 0.5 else B) * (1 - M) + 0.015 * M


# ============================================================================ the room (wood wall)
RS = 2
RWU, RHU = 2600, 2300
PWr, PHr, GXr, GYr = 280, 396, 34, 40
GCX, GCY = 1300, 1150


def rslot(i):
    r, c = divmod(i, 3)
    return GCX - (3 * PWr + 2 * GXr) / 2 + c * (PWr + GXr), GCY - (3 * PHr + 2 * GYr) / 2 + r * (PHr + GYr)


def build_room():
    cw, ch = RWU * RS, RHU * RS
    alb = wood(RWU, RHU, RS, seed=11)
    for s in range(9):
        x, y = rslot(s)
        x, y, pw, ph = int(x * RS), int(y * RS), PWr * RS, PHr * RS
        m = 40 * RS
        if GRID[s] == "J":
            jw = int(pw * 1.12)
            jh = int(jw * JOLLY_IMG.height / JOLLY_IMG.width)
            j = JOLLY_IMG.resize((jw, jh), Image.LANCZOS)
            jx, jy = x + (pw - jw) // 2, y + (ph - jh) // 2
            sh = j.getchannel("A").point(lambda v: int(v * 0.55)).filter(ImageFilter.GaussianBlur(6 * RS))
            alb.paste((0, 0, 0), (jx + 5 * RS, jy + 8 * RS), sh)
            alb.paste(j, (jx, jy), j)
            continue
        sh = Image.new("L", (pw + 2 * m, ph + 2 * m), 0)
        ImageDraw.Draw(sh).rectangle((m, m, m + pw, m + ph), fill=170)
        sh = sh.filter(ImageFilter.GaussianBlur(10 * RS))
        alb.paste((0, 0, 0), (x - m + 6 * RS, y - m + 11 * RS), sh)
        alb.paste(ImageEnhance.Brightness(A4P[GRID[s]].resize((pw, ph), Image.LANCZOS)).enhance(0.97), (x, y))
        d = ImageDraw.Draw(alb)
        nx, ny, r_ = x + pw // 2, y + 13 * RS, 6 * RS
        d.ellipse((nx - r_ + 2 * RS, ny - r_ + 3 * RS, nx + r_ + 2 * RS, ny + r_ + 3 * RS), fill=(30, 20, 15))
        d.ellipse((nx - r_, ny - r_, nx + r_, ny + r_), fill=(150, 145, 138))
        d.ellipse((nx - r_ // 2 - 2, ny - r_ // 2 - 2, nx + 1, ny + 1), fill=(215, 210, 200))
    yy, xx = np.mgrid[0:RHU // 4, 0:RWU // 4].astype(np.float32) * 4
    pools = sum(np.exp(-((xx - px) ** 2 + (yy - py) ** 2) / (2 * 820 ** 2)) for px, py in ((820, 420), (1780, 420)))
    L = (0.16 + 0.95 * pools)[..., None] * np.array([1.10, 0.86, 0.60])
    L *= (1 - 0.45 * np.clip((yy - 1750) / 550, 0, 1))[..., None]
    a = np.asarray(alb).astype(np.float32)
    for c in range(3):
        a[..., c] *= up_f(L[..., c], (cw, ch))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def room_front(t, cx, cy, z):
    j = 4 * math.sin(1.7 * t), 3 * math.sin(1.3 * t + 1)
    bw, bh = W / z, H / z
    cx = min(max(cx + j[0], bw / 2), RWU - bw / 2)
    cy = min(max(cy + j[1], bh / 2), RHU - bh / 2)
    box = (RS * (cx - bw / 2), RS * (cy - bh / 2), RS * (cx + bw / 2), RS * (cy + bh / 2))
    return from_pil(ROOM.resize((W, H), Image.BICUBIC, box=box, reducing_gap=2.0))


def room_angled(t):
    q = seg(t, T_DROP, T_FRONT)
    th = math.radians(30 + 0.3 * math.sin(1.3 * t))
    f, dist = 1600.0, 1150.0
    tx = lerp(860, 1720, ease_io(q) * 0.85 + q * 0.15) + 4 * math.sin(1.7 * t)
    py = 1150 + 6 * math.sin(0.9 * t + 1)
    px = tx - dist * math.tan(th)

    def proj(x, y):
        vx, vy, vz = x - px, y - py, dist
        xc = vx * math.cos(th) - vz * math.sin(th)
        zc = vx * math.sin(th) + vz * math.cos(th)
        return W / 2 + f * xc / zc, H / 2 + f * vy / zc

    corners = [(0, 0), (RWU, 0), (RWU, RHU), (0, RHU)]
    co = persp_coeffs([proj(x, y) for x, y in corners], [(x * RS, y * RS) for x, y in corners])
    img = ROOM.transform((W, H), Image.Transform.PERSPECTIVE, co, Image.BICUBIC)
    a = from_pil(img)
    xn = (np.arange(W, dtype=np.float32) - W / 2) / f
    zc = dist / (math.cos(th) - xn * math.sin(th))
    uf = lerp(260, 560, ease_io(seg(t, T_DROP + 0.4, T_DROP + 1.8)))
    zf = dist / (math.cos(th) - (uf - W / 2) / f * math.sin(th))
    r = np.clip(62000 * np.abs(1 / zc - 1 / zf), 0, 12)[None, :, None]
    b1 = from_pil(img.filter(ImageFilter.GaussianBlur(4)))
    b2 = from_pil(img.filter(ImageFilter.GaussianBlur(10)))
    w1 = np.clip(r / 4, 0, 1)
    w2 = np.clip((r - 4) / 8, 0, 1)
    a = (a * (1 - w1) + b1 * w1) * (1 - w2) + b2 * w2
    embers(a, t, 1.0)
    DROP_W.draw(a, t, T_DROP + 0.3, stagger=0.1, rise=0.4, t_out=T_FRONT - 0.45, out=0.3)
    return a


TOT_LBL = Words("YOUR WALL'S BOUNTY", F_UI(24), CREAM, cy=820, tracking=8, red_dot=False, shadow=0.6, single=True, opacity=0.8)
TAG_W = Words(TAG, F_FELL_I(92), CREAM, cy=1085, shadow=0.8)


def front_frame(t):
    q = ease_out(seg(t, T_FRONT, T_FRONT + 2.8))
    z = lerp(2.6, 1.0, q) - 0.08 * seg(t, T_FRONT + 2.8, T_END)
    cx, cy = rslot(4)[0] + PWr / 2, rslot(4)[1] + PHr / 2
    a = room_front(t, cx, lerp(cy, 1110, q), z)
    embers(a, t, 0.8)
    a *= 1 - 0.6 * ease_io(seg(t, T_TOTAL - 0.3, T_TOTAL + 0.1))
    if t >= T_TOTAL:
        TOT_LBL.draw(a, t, T_TOTAL, rise=0.3)
        v = TOTAL * ease_out(seg(t, T_TOTAL + 0.05, T_TOTAL + 0.85))
        draw_alpha(a, counter_img(v, 1.25), W / 2, 930, CREAM, seg(t, T_TOTAL, T_TOTAL + 0.15))
        TAG_W.draw(a, t, T_TAG, stagger=0.08)
    return a


# ============================================================================ end card
END_LOGO = Words(BRAND, F_DISP(210), cy=690, tracking=6, red_dot=False, shadow=0)
END_COL = Words(COLLECTION, F_UI(24), CREAM, cy=845, tracking=7, red_dot=False, shadow=0, single=True, opacity=0.8)
END_Q = Words(AR_Q, F_AR(62), cy=1185, rtl=True, shadow=0)
END_CTA = Words(AR_CTA, F_AR5(46), cy=1270, rtl=True, shadow=0, opacity=0.9)
END_EN = Words(EN_CTA, F_UI(24), ACCENT, cy=1340, tracking=6, red_dot=False, shadow=0, single=True)
THUMBS = []
for i in [0, 1, 2, 3, "J", 4, 5, 6, 7]:
    if i == "J":
        th_ = Image.new("RGB", (96, 136), (40, 26, 18))
        j = JOLLY_IMG.resize((88, int(88 * JOLLY_IMG.height / JOLLY_IMG.width)), Image.LANCZOS)
        th_.paste(j, (4, (136 - j.height) // 2), j)
    else:
        th_ = A4P[i].resize((96, 136), Image.LANCZOS)
    THUMBS.append(th_)
END_BG = None


def end_frame(t):
    global END_BG
    if END_BG is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - 540) / 800) ** 2 + ((yy - 900) / 1200) ** 2)
        END_BG = (np.array([12, 10, 9], np.float32) / 255 + np.clip(1 - r, 0, 1)[..., None] ** 2 * np.array([0.09, 0.05, 0.03], np.float32))
    a = END_BG.copy()
    embers(a, t, 0.45)
    END_LOGO.draw(a, t, T_END + 0.02, stagger=0.045, rise=0.4)
    lw = int(160 * ease_out(seg(t, T_END + 0.45, T_END + 0.85)))
    if lw:
        a[792:797, 540 - lw:540 + lw] = np.array(ACCENT, np.float32) / 255
    END_COL.draw(a, t, T_END + 0.6)
    img = to_pil(a)
    for j, th_ in enumerate(THUMBS):
        kq = ease_out(seg(t, T_END + 0.85 + j * 0.05, T_END + 1.25 + j * 0.05))
        if kq > 0:
            img.paste(th_, (int(60 + j * 108 + (1 - kq) * 140), 935), Image.new("L", th_.size, int(255 * kq)))
    a = from_pil(img)
    END_Q.draw(a, t, T_END + 1.6, rise=0.4)
    END_CTA.draw(a, t, T_END + 2.0, rise=0.4)
    END_EN.draw(a, t, T_END + 2.3)
    return a


# ============================================================================ timeline
print("building assets...", flush=True)
ROOM = build_room()


def montage_or_transition(t):
    k = max(0, min(7, sum(1 for c in CUTS[1:8] if t >= c)))
    for j in range(7):
        c = CUTS[j + 1]
        hw = HW[TRANS[j]] / FPS
        if c - hw <= t < c + hw:
            p = (t - (c - hw)) / (2 * hw)
            A, B = montage_frame(j, t), montage_frame(j + 1, t)
            kind = TRANS[j]
            if kind == "slash":
                return tr_slash(A, B, p)
            if kind == "whip_h":
                return tr_whip(A, B, p, 1)
            if kind == "zoom_punch":
                return tr_zoom(A, B, p)
            if kind == "sun_flash":
                return tr_sun(A, B, p)
            if kind == "haki":
                return tr_haki(A, B, p)
            if kind == "crows":
                return tr_crows(A, B, p)
            if kind == "lightning":
                return tr_lightning(A, B, p)
    return montage_frame(k, t)


def render(t):
    """-> (float image, bloom strength)"""
    if t < T_BURN:
        return hook_frame(t), 0.25
    if t < CUTS[0]:
        return tr_burn(hook_frame(t), montage_frame(0, t), seg(t, T_BURN, CUTS[0]), BURN_UP), 0.45
    if t < T_STROBE:
        return montage_or_transition(t), 0.25
    if t < T_BUT:
        f = max(i for i, ft in enumerate(FLASHES) if t >= ft)
        return strobe_frame(f, t), 0.3
    if t < T_SIL:
        return build_frame(t), 0.3
    if t < T_DROP:
        return np.zeros((H, W, 3), np.float32), 0.0
    if t < T_OPEN:
        return tr_burn(np.zeros((H, W, 3), np.float32), room_angled(t), seg(t, T_DROP, T_OPEN), BURN_RAD), 0.6
    hw = 4 / FPS
    if t < T_FRONT - hw:
        return room_angled(t), 0.45
    if t < T_FRONT + hw:
        return tr_whip(room_angled(t), front_frame(t), (t - (T_FRONT - hw)) / (2 * hw), 1), 0.4
    if t < T_END - 0.33:
        return front_frame(t), 0.4
    if t < T_END:
        return front_frame(t) * (1 - ease_in(seg(t, T_END - 0.33, T_END))), 0.3
    return end_frame(t) * (1 - seg(t, DUR - 0.5, DUR)), 0.3


def make_frame(fi):
    t = fi / FPS
    a, bl = render(t)
    a = hud(a, t)
    if bl > 0:
        a = bloom(a, bl)
    a = grade(a)
    a = a + GRAIN[rng.integers(len(GRAIN))]
    return (np.clip(a, 0, 1) * 255).astype(np.uint8)


# ============================================================================ audio
SR = 44100
NA = int(DUR * SR)


def tt(d):
    return np.arange(int(d * SR)) / SR


def noise(d, seed):
    return np.random.default_rng(seed).standard_normal(int(d * SR))


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def fft_filter(x, g_fn):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * g_fn(f), len(x))


def lp(x, fc, o=2):
    return fft_filter(x, lambda f: 1 / np.sqrt(1 + (f / fc) ** (2 * o)))


def hp(x, fc, o=2):
    return fft_filter(x, lambda f: (f / fc) ** o / np.sqrt(1 + (f / fc) ** (2 * o)))


def bp(x, lo, hi):
    return hp(lp(x, hi), lo)


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


class Bus:
    def __init__(self):
        self.x = np.zeros((2, NA))

    def add(self, sig, t, g=1.0, pan=0.0):
        i = int(round(t * SR))
        if sig.ndim == 1:
            l, r = math.cos((pan + 1) * math.pi / 4) * 1.414, math.sin((pan + 1) * math.pi / 4) * 1.414
            sig = np.stack([sig * l, sig * r])
        n = min(sig.shape[1], NA - i)
        if n > 0 and i >= 0:
            self.x[:, i:i + n] += sig[:, :n] * g


# --- instruments
@functools.lru_cache(maxsize=None)
def taiko(size=1.0, seed=1):
    d = 1.2
    t = tt(d)
    f = 52 + 55 * np.exp(-t / 0.04)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (0.32 * size))
    skin = bp(noise(d, seed), 120, 900) * np.exp(-t / 0.05) * 0.8
    slap = hp(noise(d, seed + 1), 1500) * np.exp(-t / 0.008) * 0.25
    return np.tanh(1.8 * (body + skin + slap)) * size


def kick():
    t = tt(0.5)
    f = 46 + 120 * np.exp(-t / 0.032)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.30)
    return np.tanh(2.2 * (body + 0.25 * noise(0.5, 1) * np.exp(-t / 0.003)))


def clap(seed=2):
    t = tt(0.45)
    nz = hp(lp(noise(0.45, seed), 3800), 900)
    env = np.zeros_like(t)
    for o in (0.0, 0.011, 0.022):
        env += np.where(t >= o, np.exp(-(t - o) / 0.008), 0)
    env += np.where(t >= 0.03, 0.55 * np.exp(-(t - 0.03) / 0.13), 0)
    return nz * env * 0.9 + np.sin(2 * np.pi * 185 * t) * np.exp(-t / 0.05) * 0.35


def hat(open_=False, seed=3):
    d = 0.3 if open_ else 0.08
    t = tt(d)
    return hp(noise(d, seed), 7500) * np.exp(-t / (0.16 if open_ else 0.022)) * 0.8


@functools.lru_cache(maxsize=None)
def e808(m, dur):
    t = tt(dur + 0.2)
    f0 = mtof(m)
    f = f0 * (1 + 0.9 * np.exp(-t / 0.025))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.exp(-t / 1.1) * np.clip((dur + 0.2 - t) / 0.2, 0, 1)
    return np.tanh(3.6 * s) * 0.7


def saw_stack(ms, dur, cutoff_env, det=(-0.006, 0.0, 0.006), kmax=40, fmax=6000):
    t = tt(dur)
    s = np.zeros_like(t)
    for m in ms:
        f0 = mtof(m)
        for dv in det:
            for k in range(1, kmax + 1):
                fk = k * f0 * (1 + dv)
                if fk > fmax:
                    break
                s += np.sin(2 * np.pi * fk * t + k * 0.7) / k * np.exp(-fk / cutoff_env)
    return s / (len(ms) * len(det))


@functools.lru_cache(maxsize=None)
def braam(ms, dur=3.0, power=1.0):
    t = tt(dur)
    cut = 250 + 2400 * np.exp(-t / 0.25) * (1 - np.exp(-t / 0.03)) + 350 * np.exp(-t / 1.5)
    s = saw_stack(ms, dur, cut, det=(-0.006, 0.006), kmax=40, fmax=4000)
    env = np.minimum(1, t / 0.05) * np.exp(-t / (1.4 * power)) * np.clip((dur - t) / 0.4, 0, 1)
    return np.tanh(3.0 * s * env) * 0.9


@functools.lru_cache(maxsize=None)
def strings_ost(m, dur=0.16, vel=0.6):
    t = tt(dur + 0.12)
    s = saw_stack([m], dur + 0.12, 2200.0, det=(-0.004, 0.004), kmax=24, fmax=7000)
    env = np.minimum(1, t / 0.008) * np.exp(-t / 0.09)
    return s * env * vel


@functools.lru_cache(maxsize=None)
def choir(ms, dur, att=0.6):
    t = tt(dur + 0.8)
    s = np.zeros_like(t)
    formants = ((800, 120, 1.0), (1150, 140, 0.55), (2900, 220, 0.25))
    for m in ms:
        f0 = mtof(m)
        for dv in (-0.005, 0.0, 0.005):
            vib = 1 + 0.004 * np.sin(2 * np.pi * 5.3 * t + m + dv * 900)
            for k in range(1, 40):
                fk = k * f0 * (1 + dv)
                if fk > 5000:
                    break
                wk = sum(g * math.exp(-((fk - fc) / bw) ** 2) for fc, bw, g in formants) + 0.05 / k
                s += np.sin(2 * np.pi * fk * t * vib + k) * wk
    env = np.minimum(1, t / att) ** 2 * np.clip((dur + 0.8 - t) / 0.8, 0, 1)
    return s * env / (len(ms) * 3) * 0.6


@functools.lru_cache(maxsize=None)
def lead(m, dur, vel=0.7):
    t = tt(dur + 0.5)
    cut = 900 + 1800 * np.minimum(1, t / 0.12) * np.exp(-t / 0.8)
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t / 0.35)
    f0 = mtof(m)
    s = np.zeros_like(t)
    for dv in (-0.003, 0.003):
        for k in range(1, 30):
            fk = k * f0 * (1 + dv)
            if fk > 7000:
                break
            s += np.sin(2 * np.pi * fk * t * vib + k) / k * np.exp(-fk / cut)
    env = np.minimum(1, t / 0.06) * np.clip((dur + 0.5 - t) / 0.5, 0, 1) ** 1.5
    return np.tanh(1.5 * s * env) * vel * 0.5


@functools.lru_cache(maxsize=None)
def piano(m, dur, vel=0.7):
    f0 = mtof(m)
    d = dur + 1.6
    t = tt(d)
    s = np.zeros_like(t)
    for n in range(1, 11):
        fn = n * f0 * math.sqrt(1 + 0.00035 * n * n)
        if fn > 9000:
            break
        tau = 1.9 / (1 + 0.45 * (n - 1)) * (260 / f0) ** 0.25
        for det in (-0.0005, 0.0005):
            s += np.sin(2 * np.pi * fn * (1 + det) * t) * (1 / n ** 1.15) * np.exp(-t / tau)
    s *= np.minimum(1, t / 0.004) * np.clip((dur + 0.35 - t) / 0.35, 0, 1) ** 2
    return s * vel * 0.18


def impact(size=1.0, dur=2.6, seed=7):
    t = tt(dur)
    f = 34 + 75 * np.exp(-t / 0.09)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (0.55 * size))
    crack = lp(noise(dur, seed), 3000) * np.exp(-t / 0.025)
    sub = np.sin(2 * np.pi * 30 * t) * np.exp(-t / (0.9 * size)) * 0.25 * max(0, size - 0.8)
    return np.tanh(1.7 * (body + 0.5 * crack + sub))


def whoosh(dur, peak=0.85, seed=2, hi=5000, pan=(-0.7, 0.7)):
    n = int(dur * SR)
    u = np.linspace(0, 1, n)
    env = np.where(u < peak, (u / peak) ** 2, np.clip((1 - u) / (1 - peak), 0, 1) ** 1.5)
    sig = hp(lp_sweep(noise(dur, seed), 250 + hi * env), 180) * env
    ang = (np.linspace(pan[0], pan[1], n) + 1) * np.pi / 4
    return np.stack([sig * np.cos(ang), sig * np.sin(ang)]) * 1.4


def riser(dur, seed=31):
    t = tt(dur)
    u = t / dur
    nz = hp(lp_sweep(noise(dur, seed), 200 * (35 ** u)), 150)
    return (nz + np.sin(2 * np.pi * np.cumsum(150 * 4 ** u) / SR) * 0.2) * u ** 2


def rev_cym(dur, seed=41):
    t = tt(dur)
    return hp(noise(dur, seed), 4000) * (t / dur) ** 3


def thunk(seed=51):
    t = tt(0.4)
    f = 110 + 70 * np.exp(-t / 0.01)
    knock = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.07)
    tock = bp(noise(0.4, seed), 700, 2600) * np.exp(-t / 0.025) * 0.9
    body = np.sin(2 * np.pi * 68 * t) * np.exp(-t / 0.12) * 0.6
    return np.tanh(1.6 * (knock + tock + body))


def ching(seed=61):
    t = tt(1.6)
    cha = hp(noise(1.6, seed), 2500) * np.exp(-t / 0.03) * 0.5
    s = np.zeros_like(t)
    t2 = np.clip(t - 0.07, 0, None)
    on = (t >= 0.07)
    for f, d_ in ((2793, 0.9), (4105, 0.7), (5290, 0.6), (6910, 0.45), (8230, 0.35)):
        s += np.sin(2 * np.pi * f * t2) * np.exp(-t2 / d_) * on
    return cha + s / 4


def slot_ticks(dur, seed=71):
    out = np.zeros(int(dur * SR))
    t, k = 0.0, 0
    while t < dur:
        i = int(t * SR)
        n = min(int(0.006 * SR), len(out) - i)
        tk = np.arange(n) / SR
        out[i:i + n] += (np.sin(2 * np.pi * 3200 * tk) * 0.6 + np.random.default_rng(seed + k).standard_normal(n) * 0.4) * np.exp(-tk / 0.0015)
        t += lerp(1 / 32, 1 / 5, (t / dur) ** 1.5)
        k += 1
    return out


def shing(seed=81):
    t = tt(1.4)
    sw = hp(lp_sweep(noise(1.4, seed), 2000 + 9000 * np.exp(-t / 0.08)), 2500) * np.exp(-t / 0.12)
    ring = sum(np.sin(2 * np.pi * f * t) * np.exp(-t / d_) for f, d_ in ((3150, 0.5), (4720, 0.4), (6230, 0.3), (7890, 0.25)))
    return sw * 0.8 + ring * 0.18


def burn_sfx(dur, seed=91):
    t = tt(dur)
    u = t / dur
    roar = lp_sweep(noise(dur, seed), 400 + 2500 * u) * np.sin(np.pi * u) ** 0.7
    r = np.random.default_rng(seed)
    cr = np.zeros_like(t)
    for _ in range(int(dur * 45)):
        i = int(r.uniform(0, len(t) - 400))
        cr[i:i + 300] += hp(r.standard_normal(300), 1500) * np.exp(-np.arange(300) / 40) * r.uniform(0.2, 1.0)
    return roar * 0.9 + cr * 0.5


def thunder(seed=101):
    d = 3.5
    t = tt(d)
    crack = hp(noise(d, seed), 1200) * np.exp(-t / 0.05)
    r = np.random.default_rng(seed)
    mod = np.interp(t, np.linspace(0, d, 40), r.uniform(0.3, 1.0, 40))
    rumble = lp(noise(d, seed + 1), 160) * np.exp(-t / 1.2) * mod * 3
    return np.tanh(crack + rumble)


def flutter(dur=0.7, seed=111):
    t = tt(dur)
    r = np.random.default_rng(seed)
    s = np.zeros_like(t)
    for j in range(4):
        rate = r.uniform(11, 17)
        s += bp(noise(dur, seed + j), 300, 2200) * (0.5 + 0.5 * np.sin(2 * np.pi * rate * t + j)) ** 3
    return s * np.sin(np.pi * t / dur) * 0.6


def shimmer(dur=2.0):
    t = tt(dur)
    s = sum(np.sin(2 * np.pi * f * t * (1 + 0.002 * np.sin(2 * np.pi * 5 * t))) for f in (1174.7, 1396.9, 1760.0, 2349.3))
    return s / 4 * np.exp(-t / 0.7)


def reverb_ir(d=2.8, seed=81):
    t = tt(d)
    r = np.random.default_rng(seed)
    ir = np.zeros((2, len(t)))
    for c in range(2):
        nz = r.standard_normal(len(t))
        ir[c] = lp(nz, 6000) * np.exp(-t / 0.12) * 0.5 + lp(nz, 2000) * np.exp(-t / 0.65)
    ir[:, :int(0.02 * SR)] = 0
    return ir / np.sqrt((ir ** 2).sum(axis=1, keepdims=True))


def convolve(x, ir):
    n = x.shape[1] + ir.shape[1]
    N = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(ir, N), N)[:, :x.shape[1]]


def _up(x, k):
    n = x.shape[1]
    X = np.fft.rfft(x, axis=1)
    Y = np.zeros((x.shape[0], n * k // 2 + 1), complex)
    Y[:, :X.shape[1]] = X
    return np.fft.irfft(Y, n * k, axis=1) * k


def _down(y, k, n):
    Y = np.fft.rfft(y, axis=1)[:, :n // 2 + 1]
    f = np.fft.rfftfreq(n, 1 / SR)
    Y *= 1 / np.sqrt(1 + (f / 18000) ** 8)
    return np.fft.irfft(Y, n, axis=1) / k


def true_peak_limit(x, tp_db):
    n = x.shape[1]
    y = _down(np.tanh(_up(x, 4)), 4, n)
    return y * (10 ** (tp_db / 20) / np.abs(_up(y, 4)).max())


def master_eq(x):
    def g(f):
        sm = lambda a, b: np.clip((f - a) / (b - a), 0, 1) ** 2 * (3 - 2 * np.clip((f - a) / (b - a), 0, 1))
        hp2 = (f / 28) ** 2 / np.sqrt(1 + (f / 28) ** 4)
        return hp2 * (0.5 + 0.5 * sm(45, 140)) * (1 + 0.4 * sm(2500, 7000)) * (1 + 0.45 * np.exp(-((f - 2600) / 1400) ** 2))
    return np.stack([fft_filter(x[c], g) for c in range(2)])


CH = {"Dm": [50, 53, 57], "Bb": [46, 50, 53], "F": [53, 57, 60], "C": [48, 52, 55], "A": [45, 49, 52]}
ROOT = {"Dm": 26, "Bb": 34, "F": 29, "C": 36, "A": 33}
PROG = ["Dm", "Dm", "Bb", "F", "C", "Bb", "Dm", "Bb", "F", "Dm", "Dm"]
MEL = {"Dm": [(0, 62, 1.5), (1.5, 65, 0.5), (2, 69, 2)], "Bb": [(0, 70, 1.5), (1.5, 69, 0.5), (2, 65, 2)],
       "F": [(0, 69, 2)], "C": [(0, 67, 2)]}


def ostinato(bus, send, ch, t0, length_beats, vel=0.55):
    r_, f_, o_ = CH[ch][0] - 12, CH[ch][2] - 12, CH[ch][0]
    pat = [r_, o_, f_, o_]
    for i in range(int(length_beats * 4)):
        m = pat[i % 4]
        v = vel * (1.15 if i % 4 == 0 else 0.85)
        bus.add(strings_ost(m, 0.15, v), t0 + i * BEAT / 4, pan=0.3 if i % 2 else -0.3)


def build_audio():
    drums, bass, mus, sfx = Bus(), Bus(), Bus(), Bus()
    send_m, send_s = Bus(), Bus()
    K, C, HC, HO = kick(), clap(), hat(False), hat(True)
    kicks = []
    bt = lambda b: b * BAR
    # ---- hook (bar 0): braam, taiko pulses, choir
    mus.add(braam((26, 38, 45), 2.6), 0.0, 0.9)
    send_m.add(braam((26, 38, 45), 2.6), 0.0, 0.3)
    for i, tb in enumerate((0.0, BEAT, 2 * BEAT)):
        drums.add(taiko(1.0 if i != 1 else 0.7, 1 + i), tb, 0.9)
        send_m.add(taiko(1.0, 1 + i), tb, 0.35)
    mus.add(choir((50, 57), BAR - 0.2, 1.0), 0.0, 0.7)
    for i, m in enumerate([62, 65, 69]):
        mus.add(piano(m - 12, 0.5, 0.7), (0.5 + i) * BEAT)
    # ---- montage (bars 1-4)
    for b in range(1, 5):
        t0 = bt(b)
        ch = PROG[b]
        mus.add(braam((ROOT[ch] + 12, ROOT[ch] + 24), 2.4, 0.8), t0, 0.45)
        ostinato(mus, send_m, ch, t0, 4, 0.5)
        mus.add(choir(tuple(CH[ch]), BAR - 0.3, 0.5), t0, 0.55)
        for kb, sz in ((0, 1.0), (1.5, 0.6), (2, 0.9), (3, 0.6), (3.5, 0.5)):
            drums.add(taiko(sz, 10 + b), t0 + kb * BEAT, 0.8)
            send_m.add(taiko(sz, 10 + b), t0 + kb * BEAT, 0.3)
        for kb in (0, 2):
            drums.add(K, t0 + kb * BEAT, 0.6)
        bass.add(e808(ROOT[ch], 1.2), t0, 0.55)
        for cb in (1, 3):
            drums.add(C, t0 + cb * BEAT, 0.5)
            send_m.add(C, t0 + cb * BEAT, 0.2)
        for i in range(8):
            drums.add(HC, t0 + i * BEAT / 2, 0.35 if i % 2 else 0.45, pan=0.25)
    # ---- build (bar 5)
    t0 = bt(5)
    drums.add(taiko(1.2, 30), t0, 1.0)
    mus.add(choir(tuple(CH["Bb"] + [62]), 2 * BEAT, 0.3), t0, 0.7)
    ostinato(mus, send_m, "Bb", t0, 2, 0.55)
    for ft in FLASHES:
        drums.add(taiko(0.7, int(ft * 50)), ft, 0.8)
        drums.add(clap(int(ft * 100)), ft, 0.45)
    mus.add(braam((33, 45, 52), 2.2, 0.9), T_BUT, 0.85)
    send_m.add(braam((33, 45, 52), 2.2, 0.9), T_BUT, 0.35)
    mus.add(choir(tuple(CH["A"] + [61, 64]), 1.0, 0.25), T_BUT, 0.8)
    sfx.add(riser(2.0), t0, 0.35)
    # ---- drop (bars 6-8)
    mus.add(braam((26, 38, 45, 50), 3.2, 1.3), T_DROP, 1.0)
    send_m.add(braam((26, 38, 45, 50), 3.2, 1.3), T_DROP, 0.4)
    for b in range(6, 9):
        t0 = bt(b)
        chs = [PROG[b]] if b != 8 else ["F", "C"]
        for ci, ch in enumerate(chs):
            span = BAR / len(chs)
            ts = t0 + ci * span
            mus.add(choir(tuple(CH[ch] + [CH[ch][0] + 12]), span, 0.25), ts, 0.95)
            ostinato(mus, send_m, ch, ts, 4 / len(chs), 0.55)
            for off, m, dl in MEL[ch]:
                if off * BEAT < span:
                    mus.add(lead(m, dl * BEAT * 0.95, 0.8), ts + off * BEAT)
                    send_m.add(lead(m, dl * BEAT * 0.95, 0.8), ts + off * BEAT, 0.35)
            if b != 6 or ci > 0:
                mus.add(braam((ROOT[ch] + 12, ROOT[ch] + 24), span, 0.9), ts, 0.5)
        ch = chs[0]
        for kb in [0, 0.75, 1.5, 2.75]:
            drums.add(K, t0 + kb * BEAT, 1.0)
            kicks.append(t0 + kb * BEAT)
        for kb, sz in ((0, 1.2), (2, 1.0), (3.5, 0.7)):
            drums.add(taiko(sz, 40 + b), t0 + kb * BEAT, 0.8)
            send_m.add(taiko(sz, 40 + b), t0 + kb * BEAT, 0.3)
        bass.add(e808(ROOT[ch], 0.7), t0, 1.0)
        bass.add(e808(ROOT[ch], 0.5), t0 + 0.75 * BEAT, 0.8)
        bass.add(e808(ROOT[ch], 1.0), t0 + 1.5 * BEAT, 0.9)
        bass.add(e808(ROOT[chs[-1]], 0.8), t0 + 2.75 * BEAT, 0.85)
        for cb in (1, 3):
            drums.add(C, t0 + cb * BEAT, 0.9)
            send_m.add(C, t0 + cb * BEAT, 0.3)
        for i in range(16):
            drums.add(HC, t0 + i * BEAT / 4, 0.4 if i % 2 else 0.52, pan=0.3)
        for i in range(6):
            drums.add(HC, t0 + 3 * BEAT + i * BEAT / 6, 0.25 + 0.03 * i, pan=-0.3)
        drums.add(HO, t0 + 1.5 * BEAT, 0.3, pan=-0.2)
        if b == 8:
            for i in range(4):
                drums.add(taiko(0.6 + 0.15 * i, 60 + i), t0 + 3 * BEAT + i * BEAT / 4, 0.8)
    # ---- end (bars 9-10)
    t0 = bt(9)
    mus.add(braam((26, 38, 45), 3.5, 1.4), t0, 0.9)
    send_m.add(braam((26, 38, 45), 3.5, 1.4), t0, 0.4)
    mus.add(choir(tuple(CH["Dm"] + [62, 69]), 2 * BAR - 0.6, 0.8), t0, 0.85)
    drums.add(taiko(1.3, 70), t0, 1.0)
    send_m.add(taiko(1.3, 70), t0, 0.4)
    for i, m in enumerate([74, 72, 69, 65, 62]):
        mus.add(piano(m, 0.9, 0.55), t0 + (2 + i) * BEAT)
        send_m.add(piano(m, 0.9, 0.55), t0 + (2 + i) * BEAT, 0.5)
    bass.add(e808(26, 2.6), t0, 0.9)
    send_m.x += mus.x * 0.3
    sc = np.ones(NA)
    tl = np.arange(NA) / SR
    for kt in kicks:
        i = int(kt * SR)
        n = min(int(0.4 * SR), NA - i)
        sc[i:i + n] = np.minimum(sc[i:i + n], 1 - 0.45 * np.exp(-tl[:n] / 0.12))
    music = drums.x * 1.0 + bass.x * 0.75 + mus.x * 1.0 * sc
    music += convolve(send_m.x, reverb_ir()) * 0.32
    # ---- sound design
    sfx.add(burn_sfx(0.75), T_BURN, 1.15)
    for k in range(8):
        c = CUTS[k]
        sfx.add(thunk(51 + k), c, 0.9)
        sfx.add(slot_ticks(0.85, 70 + k), c + 0.15, 0.22, pan=0.2)
        sfx.add(ching(61 + k), c + 0.9, 0.28 + 0.03 * k)
        send_s.add(ching(61 + k), c + 0.9, 0.15)
    for j, kind in enumerate(TRANS):
        c = CUTS[j + 1]
        hw = HW[kind] / FPS
        if kind == "slash":
            sfx.add(shing(82), c - hw, 0.7)
            send_s.add(shing(82), c - hw, 0.3)
        elif kind == "whip_h":
            sfx.add(whoosh(0.32, 0.6, 12, 5000, (-0.8, 0.8)), c - 0.19, 0.6)
        elif kind == "zoom_punch":
            sfx.add(whoosh(0.3, 0.9, 20, 4000), c - 0.25, 0.5)
            sfx.add(impact(0.7, 1.4, 21), c, 0.55)
        elif kind == "sun_flash":
            sfx.add(whoosh(0.45, 0.8, 22, 7000), c - 0.3, 0.45)
            sfx.add(shimmer(1.6), c, 0.14)
        elif kind == "haki":
            sfx.add(rev_cym(0.4, 23), c - 0.38, 0.3)
            sfx.add(impact(1.4, 2.4, 24), c - 0.03, 0.8)
            send_s.add(impact(1.4, 2.4, 24), c - 0.03, 0.3)
        elif kind == "crows":
            sfx.add(flutter(0.65, 25), c - 0.3, 0.6, pan=0.4)
            sfx.add(flutter(0.65, 26), c - 0.22, 0.5, pan=-0.4)
        elif kind == "lightning":
            sfx.add(thunder(27), c - hw + 0.3 * 2 * hw, 0.85)
            send_s.add(thunder(27), c - hw + 0.3 * 2 * hw, 0.25)
    for ft in FLASHES:
        sfx.add(thunk(int(ft * 30)), ft, 0.5)
    sfx.add(ching(99), FLASHES[-1] + 0.1, 0.35)
    sfx.add(rev_cym(T_DROP - T_BUT - 0.02, 28), T_BUT, 0.22)
    sfx.add(impact(1.6, 3.0, 29), T_DROP, 1.15)
    send_s.add(impact(1.6, 3.0, 29), T_DROP, 0.35)
    sfx.add(burn_sfx(0.8, 30), T_DROP, 0.9)
    sfx.add(whoosh(0.3, 0.6, 32, 5000, (-0.8, 0.8)), T_FRONT - 0.18, 0.55)
    sfx.add(slot_ticks(0.8, 33), T_TOTAL + 0.05, 0.3)
    sfx.add(ching(34), T_TOTAL + 0.85, 0.5)
    send_s.add(ching(34), T_TOTAL + 0.85, 0.25)
    sfx.add(impact(0.8, 2.0, 35), T_TAG, 0.5)
    sfx.add(whoosh(0.4, 0.9, 36, 4000), T_END - 0.38, 0.45)
    sfx.add(impact(1.3, 3.0, 37), T_END, 0.95)
    send_s.add(impact(1.3, 3.0, 37), T_END, 0.35)
    sfx.add(shimmer(2.4), T_END, 0.1)
    sfxt = sfx.x + convolve(send_s.x, reverb_ir(2.2, 82)) * 0.3
    mix = music * 0.85 + sfxt * 0.8
    mix = master_eq(mix)
    pts = [(0, 1.0), (13.3, 1.0), (14.6, 0.9), (14.66, 0.8), (15.3, 0.8), (15.99, 1.45), (23.95, 1.45),
           (24.0, 1.1), (DUR, 1.1)]
    mix *= np.interp(tl, [a for a, _ in pts], [b for _, b in pts])[None, :]
    fade = np.ones(NA)
    i_f0, i_f1 = int(T_FADE * SR), int(T_SIL * SR)
    fade[i_f0:i_f1] = np.linspace(1, 0, i_f1 - i_f0) ** 2
    fade[i_f1:int(T_DROP * SR)] = 0
    i0 = int((DUR - 0.6) * SR)
    fade[i0:] = np.linspace(1, 0, NA - i0)
    mix *= fade[None, :]
    mix = true_peak_limit(mix / (np.abs(mix).max() + 1e-9) * 3.2, -3.2)
    mix[:, i_f1:int(T_DROP * SR)] = 0
    return mix


def write_wav(path, st):
    st = np.clip(st, -1, 1).T
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())


# ============================================================================ main
def preview():
    times = [0.6, 1.5, 2.3, 3.4, 4.0, 4.6, 5.33, 6.67,
             7.7, 8.0, 9.33, 10.6, 10.73, 12.0, 12.4, 13.6,
             15.0, 16.25, 17.3, 19.0, 20.6, 22.5, 25.0, 27.5]
    tw, th = 216, 384
    cols = 8
    sheet = Image.new("RGB", (cols * tw, math.ceil(len(times) / cols) * th), (30, 30, 30))
    for n, t in enumerate(times):
        fr = Image.fromarray(make_frame(int(round(t * FPS))))
        sheet.paste(fr.resize((tw, th), Image.LANCZOS), ((n % cols) * tw, (n // cols) * th))
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
        Image.fromarray(make_frame(int(round(t * FPS)))).save(p)
        print(p)
        return
    print("rendering audio...", flush=True)
    wav = os.path.join(OUT, "audio.wav")
    write_wav(wav, build_audio())
    if "--audio" in sys.argv:
        print("audio ->", wav)
        return
    out = os.path.join(OUT, "oneline_wanted.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-maxrate", "10M", "-bufsize", "20M",
           "-tune", "film", "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "256k", "-shortest",
           "-movflags", "+faststart", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(NF):
        proc.stdin.write(make_frame(fi).tobytes())
        if fi % 60 == 0:
            print(f"  frame {fi}/{NF}", flush=True)
    proc.stdin.close()
    proc.wait()
    silent = os.path.join(OUT, "oneline_wanted_no_audio.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-an", "-c:v", "copy", silent], check=True)
    print("done ->", out)


if __name__ == "__main__":
    main()
