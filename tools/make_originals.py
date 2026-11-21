#!/usr/bin/env python3
"""Original ONELINE typographic poster designs (A4). python3 tools/make_originals.py OUT_DIR [--scale 2]"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = {
    "anton": os.path.join(ROOT, "oneline-video/fonts/Anton.ttf"),
    "inter": os.path.join(ROOT, "oneline-video/fonts/Inter-SemiBold.otf"),
    "serif": os.path.join(ROOT, "oneline-video/fonts/Playfair-Italic.ttf"),
    "ar": os.path.join(ROOT, "oneline-video/fonts/Cairo-Arabic-700.ttf"),
}
RED, CREAM, INK, SILVER, GREEN = (255, 59, 48), (242, 239, 233), (14, 14, 16), (167, 169, 172), (22, 110, 70)


def F(name, size):
    return ImageFont.truetype(FONTS[name], int(size), layout_engine=ImageFont.Layout.RAQM)


class Poster:
    def __init__(self, bg, s=1.0):
        self.s = s
        self.W, self.H = int(1240 * s), int(1754 * s)
        self.im = Image.new("RGB", (self.W, self.H), bg)
        self.d = ImageDraw.Draw(self.im)

    def u(self, v):
        return v * self.s

    def text(self, xy, txt, font, size, fill, anchor="la", track=0, stroke=None, rtl=False):
        f = F(font, self.u(size))
        x, y = self.u(xy[0]), self.u(xy[1])
        kw = dict(direction="rtl", language="ar") if rtl else {}
        sk = dict(stroke_width=int(self.u(stroke[0])), stroke_fill=stroke[1]) if stroke else {}
        if not track:
            self.d.text((x, y), txt, font=f, fill=fill, anchor=anchor, **kw, **sk)
            return
        w = sum(f.getlength(c) for c in txt) + self.u(track) * (len(txt) - 1)
        if anchor[0] == "m":
            x -= w / 2
        elif anchor[0] == "r":
            x -= w
        for c in txt:
            self.d.text((x, y), c, font=f, fill=fill, anchor="l" + anchor[1], **sk)
            x += f.getlength(c) + self.u(track)

    def fit(self, txt, font, max_w, size=400):
        f = F(font, self.u(size))
        return size * self.u(max_w) / f.getlength(txt)

    def footer(self, series, color, no):
        self.d.line((self.u(80), self.u(1610), self.u(1160), self.u(1610)), fill=color, width=max(1, int(self.u(2))))
        self.text((80, 1650), "ONELINE", "anton", 34, color, "lm")
        self.text((620, 1650), series, "inter", 18, color, "mm", track=5)
        self.text((1160, 1650), f"N°{no:03d}", "inter", 18, color, "rm", track=3)

    def grain(self, amt=6):
        a = np.asarray(self.im).astype(np.float32)
        a += np.random.default_rng(3).normal(0, amt, a.shape[:2])[..., None]
        self.im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
        return self.im


def star(d, cx, cy, r, color, width):
    pts = [(cx + r * math.sin(2 * math.pi * k * 2 / 5), cy - r * math.cos(2 * math.pi * k * 2 / 5)) for k in range(6)]
    d.line(pts, fill=color, width=width, joint="curve")


def dima_maghrib(s):
    p = Poster((170, 18, 30), s)
    for i, r in enumerate((760, 640, 520)):
        star(p.d, p.u(620), p.u(760), p.u(r), (20, 110, 70) if i == 0 else (200, 40, 50), int(p.u(10 if i == 0 else 3)))
    sz = p.fit("MAGHRIB", "anton", 1080)
    p.text((620, 760), "DIMA", "anton", sz, CREAM, "ms")
    p.text((620, 760 + sz * 0.98), "MAGHRIB", "anton", sz, CREAM, "ms")
    p.text((620, 1380), "ديما مغرب", "ar", 92, CREAM, "mm", rtl=True)
    p.text((620, 1500), "FOR THE COUNTRY · FOR THE STREETS", "inter", 20, CREAM, "mm", track=6)
    p.footer("FOOTBALL SERIES", CREAM, 101)
    return p.grain()


def ninety_plus(s):
    p = Poster(CREAM, s)
    g, w = (40, 120, 80), int(p.u(4))
    p.d.rectangle((p.u(120), p.u(140), p.u(1120), p.u(1500)), outline=g, width=w)
    p.d.line((p.u(120), p.u(820), p.u(1120), p.u(820)), fill=g, width=w)
    p.d.ellipse((p.u(470), p.u(670), p.u(770), p.u(970)), outline=g, width=w)
    p.d.rectangle((p.u(370), p.u(140), p.u(870), p.u(380)), outline=g, width=w)
    p.d.rectangle((p.u(370), p.u(1260), p.u(870), p.u(1500)), outline=g, width=w)
    sz = p.fit("90+4'", "anton", 900)
    p.text((620, 900), "90+4'", "anton", sz, INK, "mm")
    p.text((620, 1180), "it's never over.", "serif", 96, RED, "mm")
    p.footer("FOOTBALL SERIES", INK, 102)
    return p.grain(5)


def no_days_off(s):
    p = Poster(INK, s)
    sz = min(p.fit("DAYS", "anton", 1000), 1240 / 3.1)
    for i, w in enumerate(("NO", "DAYS", "OFF")):
        y = 150 + i * sz * 1.0
        if i == 1:
            p.text((620, y), w, "anton", sz, RED, "mt")
        else:
            p.text((620, y), w, "anton", sz, INK, "mt", stroke=(3, CREAM))
    p.text((620, 1510), "TRAIN · RECOVER · REPEAT", "inter", 24, SILVER, "mm", track=8)
    p.footer("SPORT SERIES", SILVER, 103)
    return p.grain(5)


def discipline(s):
    p = Poster(CREAM, s)
    sz = p.fit("DISCIPLINE", "anton", 1080)
    p.text((620, 520), "DISCIPLINE", "anton", sz, INK, "ms")
    p.text((620, 780), ">", "anton", 260, RED, "mm")
    sz2 = p.fit("MOTIVATION", "anton", 820)
    p.text((620, 1060), "MOTIVATION", "anton", sz2, CREAM, "ms", stroke=(3, INK))
    p.text((620, 1290), "show up when you don't feel like it.", "serif", 62, INK, "mm")
    p.footer("MINDSET SERIES", INK, 201)
    return p.grain(5)


def work_in_silence(s):
    p = Poster((10, 10, 12), s)
    p.text((620, 470), "خدم وسكت", "ar", 190, RED, "mm", rtl=True)
    sz = p.fit("SILENCE.", "anton", 980)
    p.text((620, 760), "WORK IN", "anton", sz * 0.62, CREAM, "mt")
    p.text((620, 760 + sz * 0.62), "SILENCE.", "anton", sz, CREAM, "mt")
    p.text((620, 1460), "let success make the noise.", "serif", 64, SILVER, "mm")
    p.footer("MINDSET SERIES", SILVER, 202)
    return p.grain(5)


def day_one(s):
    p = Poster((205, 206, 208), s)
    a = np.asarray(p.im).astype(np.float32)
    yy = np.linspace(0, 1, p.H)[:, None, None]
    a = a * (1.08 - 0.25 * yy)
    p.im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    p.d = ImageDraw.Draw(p.im)
    sz = p.fit("ONE DAY", "anton", 900)
    p.text((620, 520), "ONE DAY", "anton", sz, (110, 112, 116), "ms")
    p.d.line((p.u(150), p.u(520 - sz * 0.36), p.u(1090), p.u(520 - sz * 0.36)), fill=RED, width=int(p.u(14)))
    sz2 = p.fit("DAY ONE.", "anton", 1000)
    p.text((620, 520 + sz2 * 1.05), "DAY ONE.", "anton", sz2, INK, "ms")
    p.text((620, 1330), "your choice. starting now.", "serif", 64, INK, "mm")
    p.footer("MINDSET SERIES", INK, 203)
    return p.grain(4)


def now_playing(s):
    p = Poster(INK, s)
    cx, cy, R = p.u(620), p.u(700), p.u(470)
    p.d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(22, 22, 25))
    for r in np.arange(R * 0.36, R * 0.98, p.u(9)):
        p.d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(36, 36, 40), width=max(1, int(p.u(2))))
    p.d.ellipse((cx - R * 0.33, cy - R * 0.33, cx + R * 0.33, cy + R * 0.33), fill=RED)
    p.d.ellipse((cx - p.u(14), cy - p.u(14), cx + p.u(14), cy + p.u(14)), fill=INK)
    sheen = Image.new("L", (p.W, p.H), 0)
    ImageDraw.Draw(sheen).pieslice((cx - R, cy - R, cx + R, cy + R), 200, 235, fill=60)
    p.im.paste((255, 255, 255), (0, 0), sheen.filter(ImageFilter.GaussianBlur(p.u(30))))
    p.d = ImageDraw.Draw(p.im)
    p.text((120, 1270), "NOW PLAYING", "inter", 24, SILVER, "lm", track=8)
    p.text((120, 1360), "Your Walls, Your World", "serif", 86, CREAM, "lm")
    y = p.u(1460)
    p.d.line((p.u(120), y, p.u(1120), y), fill=(70, 70, 76), width=int(p.u(6)))
    p.d.line((p.u(120), y, p.u(760), y), fill=CREAM, width=int(p.u(6)))
    p.d.ellipse((p.u(745), y - p.u(14), p.u(775), y + p.u(14)), fill=CREAM)
    p.text((120, 1510), "2:41", "inter", 22, SILVER, "lm")
    p.text((1120, 1510), "3:58", "inter", 22, SILVER, "rm")
    p.footer("MUSIC SERIES", SILVER, 301)
    return p.grain(4)


def sound_of_city(s):
    p = Poster(CREAM, s)
    r = np.random.default_rng(12)
    n = 64
    amps = np.abs(np.convolve(r.normal(0, 1, n + 6), np.ones(4) / 4, mode="valid"))[:n]
    amps = 0.15 + amps / amps.max() * 0.85 * np.sin(np.linspace(0.1, math.pi - 0.1, n)) ** 0.5
    bw = 1000 / n
    for i, a in enumerate(amps):
        x = p.u(120 + i * bw)
        h = p.u(420 * a)
        p.d.rounded_rectangle((x, p.u(560) - h, x + p.u(bw * 0.55), p.u(560) + h), radius=int(p.u(4)),
                              fill=RED if i == 37 else INK)
    sz = p.fit("SOUND OF", "anton", 1000)
    p.text((620, 1080), "SOUND OF", "anton", sz, INK, "mt")
    p.text((620, 1080 + sz), "THE CITY", "anton", sz, INK, "mt") if False else None
    p.text((620, 1080 + sz * 0.98), "THE CITY.", "anton", sz * 0.82, INK, "mt")
    p.text((620, 1080 - 60), "CASABLANCA — 33.5731° N, 7.5898° W", "inter", 22, (90, 90, 96), "mm", track=5)
    p.footer("MUSIC SERIES", INK, 302)
    return p.grain(5)


DESIGNS = {
    "dima-maghrib": dima_maghrib, "ninety-plus-four": ninety_plus, "no-days-off": no_days_off,
    "discipline-over-motivation": discipline, "work-in-silence": work_in_silence, "day-one": day_one,
    "now-playing": now_playing, "sound-of-the-city": sound_of_city,
}

if __name__ == "__main__":
    out = sys.argv[1]
    scale = float(sys.argv[sys.argv.index("--scale") + 1]) if "--scale" in sys.argv else 1.0
    os.makedirs(out, exist_ok=True)
    for name, fn in DESIGNS.items():
        im = fn(scale)
        im.save(os.path.join(out, f"{name}.jpg"), quality=92)
        print(name, im.size)
