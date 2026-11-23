"""Animatic (timing previz) for the commercial "PEEL" - 9:16, 24 fps, 18 s, with a synthesised temp sound design.

It uses the REAL poster file (Great Wave, Collection 01) so framing and timing can be judged, but it is a
storyboard in motion, not the final film: shapes stand in for hands, room and logo.

Usage: python3 make_animatic.py <repo_root> <out_dir>
"""
import math, os, subprocess, sys, textwrap, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT, OUT = sys.argv[1], sys.argv[2]
W, H, FPS, DUR = 1080, 1920, 24, 18.0
N = int(FPS * DUR)
FONT_DIR = os.path.join(ROOT, "business/tools/fonts")
POSTER_PDF = os.path.join(ROOT, "business/poster-collection/04 A4 PRINT READY PDF/GREAT-WAVE_A4_300DPI_PRINT.pdf")
ART = os.path.join(ROOT, "business/poster-collection/02 ENHANCED IMAGES/GREAT-WAVE_ARTWORK_A3_300DPI_sRGB.jpg")
os.makedirs(OUT, exist_ok=True)

F_BOLD = lambda s: ImageFont.truetype(os.path.join(FONT_DIR, "InterDisplay-Bold.ttf"), s)
F_MED = lambda s: ImageFont.truetype(os.path.join(FONT_DIR, "Inter-Medium.ttf"), s)

# ------------------------------------------------------------------ shot list (frames @24 fps)
SHOTS = [  # code, start, end, title, camera
    ("S1", 0, 24, "HOOK - extreme macro, light sweep over the ink", "100mm macro · lateral slide · hard raking light"),
    ("S2", 24, 48, "Fingertip lifts the backing corner", "100mm macro · locked off · 120 fps slow-mo"),
    ("S3", 48, 96, "The peel - liner slides away, rack focus to the art", "35mm · side angle · rack focus · slow-mo"),
    ("S4", 96, 120, "Match cut - the poster travels to the wall", "35mm · tracking dolly"),
    ("S5", 120, 144, "Contact - top edge meets the wall (speed ramp)", "100mm macro · ramp 100% to 35%"),
    ("S6", 144, 168, "Palm smooths the surface, light follows the hand", "35mm · parallel tracking"),
    ("S7", 168, 192, "Silence - lights die, the room holds its breath", "35mm · locked off · black"),
    ("S8", 192, 240, "REVEAL - lamp clicks on, slow dolly back", "35mm · dolly back · single spotlight"),
    ("S9", 240, 288, "Arc around the poster, rack focus from foreground", "35mm · 15° arc · highlight sweep"),
    ("S10", 288, 336, "Desire - owner sits back, looks at the wall", "35mm · slow push-in"),
    ("S11", 336, 432, "BRAND - logo peel reveal, tagline, CTA", "motion graphics on black"),
]
COPY = [  # start s, end s, text
    (2.2, 3.9, "Chaque détail."),
    (6.0, 7.4, "Décollez. Posez."),   # runs into the silent black of S7
    (12.2, 13.9, "Votre mur. Votre histoire."),
]


def sstep(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def eout(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def lerp(a, b, t):
    return a + (b - a) * t


# ------------------------------------------------------------------ assets
tmp_png = os.path.join(OUT, "_poster")
subprocess.run(["pdftoppm", "-r", "150", "-png", "-singlefile", POSTER_PDF, tmp_png], check=True)
POSTER = Image.open(tmp_png + ".png").convert("RGB")
os.remove(tmp_png + ".png")
ARTIMG = Image.open(ART).convert("RGB")
PW, PH = POSTER.size

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
xn, yn = xx / W, yy / H
rng = np.random.default_rng(7)
noise = Image.fromarray((rng.normal(0, 1, (120, 68)) * 18 + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
noise = (np.asarray(noise, np.float32) - 128) / 128
WALL = np.stack([30 + 6 * (1 - yn) + 3 * noise] * 3, -1) * np.array([1.0, 0.97, 0.94], np.float32)


def poster_scaled(width):
    return POSTER.resize((int(width), int(width * PH / PW)), Image.LANCZOS)


def paste_center(canvas, img, cx, cy):
    canvas.paste(img, (int(cx - img.width / 2), int(cy - img.height / 2)))


def shadow(canvas, box, blur, alpha):
    sh = Image.new("L", (W // 4, H // 4), 0)
    x0, y0, x1, y1 = [v / 4 for v in box]
    ImageDraw.Draw(sh).rectangle((x0, y0, x1, y1), fill=int(255 * alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(max(1, blur / 4))).resize((W, H), Image.BILINEAR)
    canvas.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), sh)


def to_img(a):
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


# pre-scaled posters and blur stacks
P_S3 = poster_scaled(0.64 * W)
P_S3_BLUR = {r: P_S3.filter(ImageFilter.GaussianBlur(r)) if r else P_S3 for r in (0, 2, 4, 7, 10)}
P_WALL = poster_scaled(0.70 * W)
P_ROOM = poster_scaled(0.46 * W)
P_S9 = poster_scaled(0.66 * W)
P_S9_BLUR = {r: P_S9.filter(ImageFilter.GaussianBlur(r)) if r else P_S9 for r in (0, 2, 4, 7)}


def nearest(d, r):
    return d[min(d, key=lambda k: abs(k - r))]


# ------------------------------------------------------------------ shots
def s1(t):
    aw, ah = ARTIMG.size
    ch = int(0.56 * ah); cw = int(ch * 9 / 16)
    cx = int(lerp(0.33, 0.35, t) * aw); cy = int(0.34 * ah)
    crop = ARTIMG.crop((cx - cw // 2, cy - ch // 2, cx + cw // 2, cy + ch // 2)).resize((W, H), Image.BICUBIC)
    a = np.asarray(crop, np.float32)
    pos = lerp(-0.45, 1.55, sstep(t))
    band = np.exp(-(((xn * 0.8 + yn * 0.6) - pos) / 0.20) ** 2)
    return to_img(a * (0.10 + 1.05 * band)[..., None])


def s2(t):
    c = Image.new("RGB", (W, H), (13, 13, 15))
    big = poster_scaled(1.7 * W)
    cx, cy = int(0.64 * W), int(0.56 * H)       # poster bottom-right corner position
    a = lerp(0, 230, eout(t))
    d = ImageDraw.Draw(c)
    if a > 2:
        tip = (cx + a * 0.55, cy + a * 0.55)
        d.polygon([(cx - a, cy), tip, (cx, cy - a)], fill=(222, 219, 212))
        d.line([(cx - a, cy), tip, (cx, cy - a)], fill=(170, 168, 162), width=2)
    c.paste(big, (cx - big.width, cy - big.height))
    arr = np.asarray(c, np.float32)
    light = 0.35 + 0.75 * np.exp(-(((xn - 0.62) ** 2) / 0.05 + ((yn - 0.54) ** 2) / 0.03))
    return to_img(arr * light[..., None])


def s3(t):
    c = Image.new("RGB", (W, H), (12, 12, 14))
    dx, dy = lerp(0, 0.55 * W, sstep(t)), lerp(0, -0.08 * H, sstep(t))
    liner = Image.new("RGB", P_S3.size, (226, 223, 216)).rotate(lerp(0, 9, t), expand=True, fillcolor=(12, 12, 14))
    liner = liner.filter(ImageFilter.GaussianBlur(lerp(0, 8, sstep(t / 0.7))))
    paste_center(c, liner, W / 2 + dx + 18, 0.40 * H + dy + 14)
    rf = sstep((t - 0.15) / 0.5)
    poster = nearest(P_S3_BLUR, lerp(10, 0, rf)).rotate(lerp(-3, 0, t), expand=True, fillcolor=(12, 12, 14))
    paste_center(c, poster, W / 2, 0.40 * H)
    arr = np.asarray(c, np.float32)
    return to_img(arr * (0.45 + 0.65 * np.exp(-((xn - 0.35) ** 2) / 0.12))[..., None])


def wall_canvas(light=1.0):
    return to_img(WALL * light)


def s4(t):
    c = wall_canvas(0.9)
    e = sstep(t)
    p = poster_scaled(lerp(0.55, 0.66, e) * W).rotate(lerp(-8, 0, e), expand=True, fillcolor=(30, 29, 28))
    x, y = lerp(0.80 * W, 0.50 * W, e), lerp(1.05 * H, 0.46 * H, e)
    shadow(c, (x - p.width / 2 + lerp(70, 14, e), y - p.height / 2 + lerp(90, 16, e),
               x + p.width / 2 + lerp(70, 14, e), y + p.height / 2 + lerp(90, 16, e)), lerp(60, 14, e), lerp(0.25, 0.55, e))
    paste_center(c, p, x, y)
    return c


def s5(t):
    c = wall_canvas(0.95)
    big = poster_scaled(1.9 * W)
    top = lerp(860, 760, eout(t / 0.6))
    x0 = int(W / 2 - big.width / 2)
    shadow(c, (x0, top - 6, x0 + big.width, top + lerp(30, 4, eout(t / 0.6))), lerp(40, 6, eout(t / 0.6)), 0.6)
    c.paste(big, (x0, int(top)))
    return c


def s6(t, light_on=True):
    c = wall_canvas(0.9)
    shadow(c, (W / 2 - P_WALL.width / 2 + 10, 0.43 * H - P_WALL.height / 2 + 12,
               W / 2 + P_WALL.width / 2 + 10, 0.43 * H + P_WALL.height / 2 + 12), 16, 0.5)
    paste_center(c, P_WALL, W / 2 + lerp(30, -30, t), 0.43 * H)
    arr = np.asarray(c, np.float32) * 0.72
    if light_on:
        lx = lerp(0.12, 0.88, sstep(t))
        arr = arr + 120 * np.exp(-(((xn - lx) ** 2) / 0.02 + ((yn - 0.43) ** 2) / 0.012))[..., None] * np.array([1.0, 0.92, 0.8])
    return to_img(arr)


def s7(t):
    base = np.asarray(s6(1.0, light_on=False), np.float32)
    return to_img(base * max(0.0, 1 - t * 3) * 0.9)


ROOM = None
SPOT = np.exp(-(((xn - 0.5) ** 2) / 0.09 + ((yn - 0.37) ** 2) / 0.05)).astype(np.float32)


def build_room():
    c = wall_canvas(1.0)
    d = ImageDraw.Draw(c)
    d.rectangle((0, 1500, W, H), fill=(15, 14, 14))                       # floor
    d.rectangle((540, 1330, W, 1356), fill=(36, 34, 32))                   # desk top
    d.rectangle((580, 1356, 600, 1500), fill=(26, 25, 24)); d.rectangle((1020, 1356, 1040, 1500), fill=(26, 25, 24))
    d.rectangle((930, 1120, 938, 1330), fill=(30, 29, 28))                 # lamp pole
    d.polygon([(890, 1120), (978, 1120), (960, 1060), (908, 1060)], fill=(40, 38, 36))
    d.rectangle((640, 1290, 820, 1330), fill=(22, 21, 21))                 # books / object
    shadow(c, (W / 2 - P_ROOM.width / 2 + 8, 0.40 * H - P_ROOM.height / 2 + 10,
               W / 2 + P_ROOM.width / 2 + 8, 0.40 * H + P_ROOM.height / 2 + 10), 12, 0.5)
    paste_center(c, P_ROOM, W / 2, 0.40 * H)
    return np.asarray(c, np.float32)


def zoom(img, z, cy=0.40):
    cw, ch = W / z, H / z
    x0, y0 = W / 2 - cw / 2, cy * H - ch * cy
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BICUBIC)


def s8(t):
    f = t * 48
    inten = 0.0 if f < 1 else min(1.08, (f - 1) / 8) if f < 9 else lerp(1.08, 1.0, min(1, (f - 9) / 10))
    lit = ROOM * (0.10 + 0.25 * min(1, f / 6) + SPOT * inten)[..., None]
    return zoom(to_img(lit), lerp(1.14, 1.0, sstep(t)))


def persp_coeffs(src, dst):
    m = []
    for (x, y), (u, v) in zip(dst, src):
        m.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); m.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    a = np.array(m, float); b = np.array(src, float).reshape(8)
    return np.linalg.solve(a, b).tolist()


def s9(t):
    base = WALL * (0.35 + SPOT * 1.0)[..., None]
    c = to_img(base)
    ang = math.radians(lerp(16, 5, sstep(t)))
    p = nearest(P_S9_BLUR, lerp(7, 0, sstep((t - 0.2) / 0.5)))
    w, h = p.size
    nw, k = w * math.cos(ang), h * 0.10 * math.sin(ang) / math.sin(math.radians(16))
    ox, oy = W / 2 - nw / 2, 0.42 * H - h / 2
    dst = [(ox, oy), (ox + nw, oy + k), (ox + nw, oy + h - k), (ox, oy + h)]
    warped = p.transform((W, H), Image.PERSPECTIVE, persp_coeffs([(0, 0), (w, 0), (w, h), (0, h)], dst), Image.BICUBIC)
    mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).polygon(dst, fill=255)
    shadow(c, (ox + 10, oy + 14, ox + nw + 10, oy + h + 8), 18, 0.5)
    c.paste(warped, (0, 0), mask)
    arr = np.asarray(c, np.float32)
    band = np.exp(-(((xn * 0.7 - yn * 0.4) - lerp(-0.5, 0.8, t)) / 0.06) ** 2)
    arr = arr + 55 * band[..., None] * (np.asarray(mask, np.float32) / 255)[..., None]
    fg = Image.new("L", (W, H), 0)
    ImageDraw.Draw(fg).ellipse((-180, 1380, 420, 1980), fill=255)
    fg = fg.filter(ImageFilter.GaussianBlur(lerp(4, 34, sstep(t))))
    arr = arr * (1 - 0.92 * (np.asarray(fg, np.float32) / 255))[..., None]
    return to_img(arr)


def s10(t):
    lit = ROOM * (0.35 + SPOT * 1.0)[..., None]
    c = zoom(to_img(lit), lerp(1.0, 1.05, t))
    d = ImageDraw.Draw(c)
    d.ellipse((215, 1480, 375, 1650), fill=(9, 9, 10), outline=(58, 56, 54), width=3)     # head (rim light)
    d.rounded_rectangle((120, 1630, 480, 1920), radius=120, fill=(9, 9, 10))               # shoulders
    return c


def s11(t, f):
    c = Image.new("RGB", (W, H), (11, 11, 12))
    d = ImageDraw.Draw(c)
    lf = f - 336
    box = (W / 2 - 280, 700, W / 2 + 280, 920)
    if lf >= 12:
        for x in range(int(box[0]), int(box[2]), 24):
            d.line((x, box[1], min(x + 12, box[2]), box[1]), fill=(150, 146, 140), width=2)
            d.line((x, box[3], min(x + 12, box[2]), box[3]), fill=(150, 146, 140), width=2)
        for y in range(int(box[1]), int(box[3]), 24):
            d.line((box[0], y, box[0], min(y + 12, box[3])), fill=(150, 146, 140), width=2)
            d.line((box[2], y, box[2], min(y + 12, box[3])), fill=(150, 146, 140), width=2)
        txt(d, "VOTRE LOGO", F_BOLD(64), 780, (237, 232, 223))
        txt(d, "(remplacer par le vrai logo)", F_MED(24), 860, (150, 146, 140))
        p = sstep((lf - 12) / 12)
        if p < 1:
            liner = Image.new("RGB", (600, 250), (226, 223, 216)).rotate(lerp(0, 12, p), expand=True, fillcolor=(11, 11, 12))
            c.paste(liner, (int(W / 2 - 300 + p * 900), int(685 + p * 120)))
    if lf >= 36:
        a = min(1, (lf - 36) / 8)
        txt(d, "STICK TO WHAT MOVES YOU.", F_BOLD(60), 1040, tuple(int(v * a + 11 * (1 - a)) for v in (237, 232, 223)))
    if lf >= 60:
        a = min(1, (lf - 60) / 8)
        col = tuple(int(v * a + 11 * (1 - a)) for v in (185, 178, 166))
        txt(d, "Posters adhésifs A4", F_MED(36), 1150, col)
        txt(d, "Commandez sur WhatsApp", F_MED(36), 1200, col)
    fade = 1 - max(0, (f - (N - 8)) / 8)
    return to_img(np.asarray(c, np.float32) * fade)


def txt(d, s, font, y, fill):
    w = d.textlength(s, font=font)
    d.text(((W - w) / 2, y), s, font=font, fill=fill)


def frame(f):
    code, f0, f1, title, cam = next(s for s in SHOTS if s[1] <= f < s[2])
    t = (f - f0) / (f1 - f0)
    img = {"S1": s1, "S2": s2, "S3": s3, "S4": s4, "S5": s5, "S6": s6, "S7": s7, "S8": s8, "S9": s9, "S10": s10}.get(code)
    img = img(t) if img else s11(t, f)
    d = ImageDraw.Draw(img)
    sec = f / FPS
    for a0, a1, s in COPY:
        if a0 <= sec <= a1:
            a = min(1, (sec - a0) / 0.25, (a1 - sec) / 0.25)
            txt(d, s, F_MED(50), 1400, tuple(int(240 * a + 20 * (1 - a)) for _ in range(3)))
    # previz labels (not part of the film)
    d.rectangle((0, 1780, W, H), fill=(0, 0, 0))
    d.text((36, 1796), f"{code}  ·  {int(sec):02d}:{f % FPS:02d}  ·  {title}", font=F_MED(28), fill=(230, 226, 218))
    d.text((36, 1840), cam, font=F_MED(24), fill=(150, 146, 140))
    d.text((36, 28), "ANIMATIC v1  ·  previz de timing, pas le film final", font=F_MED(24), fill=(120, 118, 114))
    return img, code


# ------------------------------------------------------------------ temp sound design
SR = 48000
NS = int(SR * DUR)


def band_noise(dur, lo, hi, seed=0):
    n = int(SR * dur); x = np.random.default_rng(seed).normal(0, 1, n)
    X = np.fft.rfft(x); fr = np.fft.rfftfreq(n, 1 / SR); X[(fr < lo) | (fr > hi)] = 0
    y = np.fft.irfft(X, n); return y / (np.abs(y).max() + 1e-9)


def tone(freq, dur, decay, harm=(1, .5, .25, .12), detune=0.0):
    t = np.arange(int(SR * dur)) / SR
    y = sum(a * np.sin(2 * np.pi * freq * (k + 1) * (1 + detune) * t) * np.exp(-t / (decay / (k + 1) ** .5)) for k, a in enumerate(harm))
    att = np.minimum(1, t / 0.006); return y * att / (sum(harm))


def env_ar(n, att, rel):
    t = np.arange(n) / SR; d = n / SR
    return np.minimum(1, t / max(att, 1e-4)) * np.minimum(1, (d - t) / max(rel, 1e-4)).clip(0, 1)


def add(bus, start, sig, db, pan=0.0):
    i = int(start * SR); sig = sig[: max(0, NS - i)]
    g = 10 ** (db / 20)
    p = np.full(len(sig), pan) if np.isscalar(pan) else np.interp(np.linspace(0, 1, len(sig)), [0, 1], pan)
    bus[i:i + len(sig), 0] += sig * g * np.cos((p + 1) * np.pi / 4)
    bus[i:i + len(sig), 1] += sig * g * np.sin((p + 1) * np.pi / 4)


def crackle(dur, rate0, rate1, seed):
    n = int(SR * dur); rng = np.random.default_rng(seed)
    rate = np.linspace(rate0, rate1, n) / SR
    imp = (rng.random(n) < rate) * rng.uniform(0.3, 1, n) * rng.choice([-1, 1], n)
    X = np.fft.rfft(imp); fr = np.fft.rfftfreq(n, 1 / SR); X[(fr < 1500) | (fr > 9000)] = 0
    y = np.fft.irfft(X, n); return y / (np.abs(y).max() + 1e-9)


def sound(path):
    sfx = np.zeros((NS, 2)); mus = np.zeros((NS, 2)); amb = np.zeros((NS, 2))
    t12 = np.arange(int(SR * 1.3)) / SR
    add(sfx, 0.0, (np.sin(2 * np.pi * 42 * t12) + .3 * np.sin(2 * np.pi * 84 * t12)) * env_ar(len(t12), .9, .5), -18)      # sub swell
    add(sfx, 0.0, band_noise(1.0, 6000, 12000, 1) * np.exp(-((np.arange(SR) / SR - .5) / .25) ** 2), -40, [-.6, .6])        # light shimmer
    add(sfx, 1.0, band_noise(.03, 2000, 7000, 2) * np.exp(-np.arange(int(SR * .03)) / (SR * .006)), -12, .2)              # nail tick
    add(sfx, 1.05, crackle(.3, 40, 20, 3) * env_ar(int(SR * .3), .01, .2), -24, .2)
    add(sfx, 2.0, crackle(1.8, 80, 420, 4) * env_ar(int(SR * 1.8), .05, .3), -14, [-.5, .5])                               # THE PEEL
    add(sfx, 2.0, band_noise(1.8, 800, 4000, 5) * env_ar(int(SR * 1.8), .2, .4), -28, [-.5, .5])
    add(sfx, 2.0, band_noise(1.8, 80, 300, 6) * env_ar(int(SR * 1.8), .3, .5), -24)
    w = np.concatenate([band_noise(.35, 300, 1200, 7) * np.linspace(0, 1, int(SR * .35)), band_noise(.35, 900, 3500, 8) * np.linspace(1, 0, int(SR * .35))])
    add(sfx, 3.65, w, -20, [-.7, .7])                                                                                         # whoosh to match cut
    tc = np.arange(int(SR * .4)) / SR
    add(sfx, 5.0, np.sin(2 * np.pi * 72 * tc) * np.exp(-tc / .12) + .4 * band_noise(.4, 200, 900, 9) * np.exp(-tc / .04), -10)  # contact
    add(sfx, 6.0, band_noise(1.0, 1000, 5000, 10) * env_ar(SR, .15, .25), -30, [-.4, .4])                                  # palm glide
    for k, st in enumerate((7.92, 7.955)):
        add(sfx, st, band_noise(.012, 3000, 9000, 11 + k) * np.exp(-np.arange(int(SR * .012)) / (SR * .002)), -8)        # lamp click
    ti = np.arange(int(SR * 2.2)) / SR
    sweep = np.sin(2 * np.pi * np.cumsum(np.linspace(90, 34, len(ti))) / SR) * np.exp(-ti / .9)
    add(sfx, 8.0, sweep, -4)                                                                                                  # REVEAL impact
    add(sfx, 8.0, band_noise(.3, 60, 2000, 13) * np.exp(-np.arange(int(SR * .3)) / (SR * .05)), -14)
    add(sfx, 10.0, band_noise(.6, 400, 2500, 14) * env_ar(int(SR * .6), .3, .3), -32, [.5, -.5])                          # arc air
    add(sfx, 10.4, tone(3520, .5, .25, (1,)), -42, .3)                                                                         # glint
    add(sfx, 14.5, crackle(.25, 300, 120, 15) * env_ar(int(SR * .25), .005, .15), -14)                                       # sonic logo peel
    tl = np.arange(int(SR * 1.4)) / SR
    add(sfx, 14.55, np.sin(2 * np.pi * 55 * tl) * np.exp(-tl / .6), -14)
    # music bus: felt-piano motif + pad (temp, to be replaced by the real score)
    for st, fq, db in ((2.0, 146.83, -18), (6.0, 220.0, -20), (8.0, 293.66, -17), (9.0, 349.23, -20), (10.0, 440.0, -21),
                       (12.0, 349.23, -20), (13.0, 329.63, -21), (14.55, 220.0, -15), (14.75, 293.66, -15), (14.95, 349.23, -14)):
        add(mus, st, tone(fq, 3.0, 1.6), db, (fq - 300) / 600)
    pad_d = 6.0; tp = np.arange(int(SR * pad_d)) / SR
    pad = sum(np.sin(2 * np.pi * f * (1 + dt) * tp) for f in (73.42, 110.0, 146.83, 174.61) for dt in (-.0015, 0, .0015))
    add(mus, 8.0, pad / 12 * env_ar(len(tp), 1.2, .35), -16)
    add(amb, 0.0, band_noise(DUR, 100, 800, 16), -58)
    # strategic silence 7.00-7.92: mute music + sfx (room tone stays), then the click and the reveal
    m = np.ones(NS); a, b = int(7.0 * SR), int(7.92 * SR)
    m[a - int(.08 * SR):a] = np.linspace(1, 0, int(.08 * SR)); m[a:b] = 0
    sfx[:b - 10] *= m[:b - 10, None]; mus *= m[:, None]
    mix = sfx + mus + amb
    mix[-int(.5 * SR):] *= np.linspace(1, 0, int(.5 * SR))[:, None]
    mix = np.tanh(mix * 1.2) / np.tanh(1.2)
    pcm = (mix / (np.abs(mix).max() + 1e-9) * 0.89 * 32767).astype(np.int16)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())


# ------------------------------------------------------------------ render
ROOM = build_room()
wav = os.path.join(OUT, "_temp_sound.wav")
sound(wav)
mp4 = os.path.join(OUT, "PEEL_animatic_v1_9x16_24fps.mp4")
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                       "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                       "-af", "loudnorm=I=-14:TP=-1.0:LRA=11", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
                       "-movflags", "+faststart", "-shortest", mp4], stdin=subprocess.PIPE)
keys = {}
for f in range(N):
    img, code = frame(f)
    s = next(s for s in SHOTS if s[0] == code)
    if f == (s[1] + s[2]) // 2 or (code == "S11" and f == 404):
        keys[code] = img.copy()
    ff.stdin.write(img.tobytes())
ff.stdin.close(); ff.wait()
os.remove(wav)
# storyboard sheet
cols, tw, th = 4, 270, 480
sheet = Image.new("RGB", (cols * (tw + 20) + 20, 3 * (th + 90) + 20), (18, 18, 20))
d = ImageDraw.Draw(sheet)
for i, (code, f0, f1, title, cam) in enumerate(SHOTS):
    x, y = 20 + (i % cols) * (tw + 20), 20 + (i // cols) * (th + 90)
    sheet.paste(keys[code].resize((tw, th), Image.LANCZOS), (x, y))
    d.text((x, y + th + 8), f"{code}  {f0 / FPS:.2f}-{f1 / FPS:.2f}s", font=F_BOLD(22), fill=(237, 232, 223))
    for j, line in enumerate(textwrap.wrap(title, 34)[:2]):
        d.text((x, y + th + 38 + 20 * j), line, font=F_MED(15), fill=(185, 178, 166))
sheet.save(os.path.join(OUT, "PEEL_storyboard_v1.png"))
print("done", mp4)
