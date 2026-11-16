"""MOTIF 297 brand film — rendering engine.

Virtual camera over flat artwork: every poster (and the wall) is a plane in
3D space, viewed through a pinhole camera. Depth of field is derived from the
real per-pixel depth of that plane, motion blur from sub-frame camera samples.
Everything is procedural so the film can be re-rendered or re-timed exactly.
"""
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

W, H, FPS = 1080, 1920, 30
FOCAL = 1500.0
K = np.array([[FOCAL, 0, W / 2], [0, FOCAL, H / 2], [0, 0, 1.0]])

cv2.setNumThreads(1)


def hexrgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255.0


OBSIDIAN = hexrgb("#171717")
PAPER = hexrgb("#F4F0E8")
CONCRETE = hexrgb("#B7B2AA")
RUST = hexrgb("#B64A3A")

# ----------------------------------------------------------------- easing ---


def c01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def e_lin(t):
    return t


def e_out_expo(t):
    return 1.0 if t >= 1 else 1 - 2 ** (-10 * t)


def e_in_expo(t):
    return 0.0 if t <= 0 else 2 ** (10 * t - 10)


def e_inout_expo(t):
    if t <= 0:
        return 0.0
    if t >= 1:
        return 1.0
    return 2 ** (20 * t - 10) / 2 if t < .5 else (2 - 2 ** (-20 * t + 10)) / 2


def e_out_cubic(t):
    return 1 - (1 - t) ** 3


def e_in_cubic(t):
    return t ** 3


def e_inout_cubic(t):
    return 4 * t ** 3 if t < .5 else 1 - (-2 * t + 2) ** 3 / 2


def e_out_quint(t):
    return 1 - (1 - t) ** 5


def e_inout_sine(t):
    return -(math.cos(math.pi * t) - 1) / 2


def key(f, keys):
    """Keyframe track. keys = [(frame, value), (frame, value, ease), ...]."""
    def val(v):
        return np.asarray(v, float) if isinstance(v, (tuple, list)) else float(v)
    if f <= keys[0][0]:
        return val(keys[0][1])
    for i in range(1, len(keys)):
        f1 = keys[i][0]
        if f <= f1:
            f0 = keys[i - 1][0]
            v0, v1 = val(keys[i - 1][1]), val(keys[i][1])
            ease = keys[i][2] if len(keys[i]) > 2 else e_inout_cubic
            t = ease(c01((f - f0) / (f1 - f0))) if f1 > f0 else 1.0
            return v0 * (1 - t) + v1 * t
    return val(keys[-1][1])


def ramp(f, f0, f1, ease=e_out_expo):
    return ease(c01((f - f0) / max(1e-6, f1 - f0)))

# ----------------------------------------------------------------- camera ---


def rotm(yaw, pitch, roll):
    y, p, r = map(math.radians, (yaw, pitch, roll))
    Ry = np.array([[math.cos(y), 0, math.sin(y)], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])
    Rx = np.array([[1, 0, 0], [0, math.cos(p), -math.sin(p)], [0, math.sin(p), math.cos(p)]])
    Rz = np.array([[math.cos(r), -math.sin(r), 0], [math.sin(r), math.cos(r), 0], [0, 0, 1]])
    return Rz @ Rx @ Ry


class Cam:
    """Pinhole camera aimed at `target` (a point on the Z=0 plane) from `dist`."""

    def __init__(self, target, dist, yaw=0.0, pitch=0.0, roll=0.0):
        self.R = rotm(yaw, pitch, roll)
        fwd = self.R.T @ np.array([0, 0, 1.0])
        t = np.array([target[0], target[1], 0.0])
        self.C = t - dist * fwd
        self.dist = dist

    def plane_H(self, O, a, b):
        """Homography (u, v) -> image for the 3D plane P = O + a*u + b*v."""
        M = np.stack([self.R @ np.asarray(a, float), self.R @ np.asarray(b, float),
                      self.R @ (np.asarray(O, float) - self.C)], axis=1)
        return K @ M

    def wall_H(self):
        return self.plane_H((0, 0, 0), (1, 0, 0), (0, 1, 0))

    def project(self, P):
        p = self.R @ (np.asarray(P, float) - self.C)
        return np.array([FOCAL * p[0] / p[2] + W / 2, FOCAL * p[1] / p[2] + H / 2]), p[2]

    def invz_map(self):
        """Per-pixel 1/depth of the Z=0 plane (affine in screen space)."""
        n = self.R @ np.array([0, 0, 1.0])
        d0 = n @ (self.R @ (-self.C))
        xs = (np.arange(W, dtype=np.float32) - W / 2) / FOCAL
        ys = (np.arange(H, dtype=np.float32) - H / 2) / FOCAL
        return (n[0] * xs[None, :] + n[1] * ys[:, None] + n[2]) / d0


def dof_map(cam, strength, focus=None, cap=40.0):
    """Blur sigma (px) per pixel from thin-lens circle of confusion."""
    if strength <= 0.05:
        return None
    zf = cam.dist if focus is None else focus
    invz = cam.invz_map()
    return np.minimum(strength * np.abs(1.0 - zf * invz), cap).astype(np.float32)

# ---------------------------------------------------------------- imaging ---


def blur_fast(img, sigma):
    if sigma < 0.4:
        return img
    d = 1
    while sigma / d > 5 and d < 16:
        d *= 2
    if d == 1:
        return cv2.GaussianBlur(img, (0, 0), sigma)
    h, w = img.shape[:2]
    small = cv2.resize(img, (max(1, w // d), max(1, h // d)), interpolation=cv2.INTER_AREA)
    small = cv2.GaussianBlur(small, (0, 0), sigma / d)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_LINEAR)


SIG_LEVELS = [0.0, 1.5, 3.0, 6.0, 12.0, 24.0, 48.0]


def variable_blur(img, bmap):
    if bmap is None:
        return img
    mx = float(bmap.max())
    if mx < 0.5:
        return img
    n = 1
    while n < len(SIG_LEVELS) and SIG_LEVELS[n - 1] < mx:
        n += 1
    lv = SIG_LEVELS[:n]
    out = np.zeros_like(img)
    for i, s in enumerate(lv):
        lo = lv[i - 1] if i > 0 else None
        hi = lv[i + 1] if i + 1 < len(lv) else None
        wgt = np.zeros_like(bmap)
        if lo is not None:
            m = (bmap >= lo) & (bmap <= s)
            wgt[m] = (bmap[m] - lo) / (s - lo)
        else:
            wgt[bmap <= s] = 1.0
        if hi is not None:
            m = (bmap > s) & (bmap < hi)
            wgt[m] = (hi - bmap[m]) / (hi - s)
        else:
            wgt[bmap > s] = 1.0
        if wgt.max() <= 0:
            continue
        b = img if s == 0 else blur_fast(img, s)
        out += b * wgt[..., None]
    return out


def bloom(img, thresh=0.72, sigma=36, strength=0.5):
    lum = img.max(axis=2)
    m = np.clip((lum - thresh) / (1 - thresh + 1e-6), 0, 1)[..., None]
    return img + strength * blur_fast(img * m, sigma)


def over(dst, rgb_premul, alpha):
    """Composite premultiplied rgb with alpha (H,W) over dst."""
    return rgb_premul + dst * (1 - alpha[..., None])


# ---------------------------------------------------------------- posters ---

class Poster:
    def __init__(self, name, path):
        self.name = name
        img = cv2.cvtColor(cv2.imread(path, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0
        self.h, self.w = img.shape[:2]
        self.img = img
        self.levels, self.full = [], []
        cur = img
        for _ in range(6):
            pad = cv2.copyMakeBorder(cur, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=0)
            a = np.zeros(pad.shape[:2], np.float32)
            a[2:-2, 2:-2] = 1.0
            self.levels.append((np.dstack([pad, a]), cur.shape[1] / self.w, cur.shape[0] / self.h))
            self.full.append((cur, cur.shape[1] / self.w, cur.shape[0] / self.h))
            cur = cv2.resize(cur, (max(2, cur.shape[1] // 2), max(2, cur.shape[0] // 2)),
                             interpolation=cv2.INTER_AREA)

    @staticmethod
    def _scale_at(Hm, u, v):
        p = Hm @ np.array([u, v, 1.0])
        x, y = p[0] / p[2], p[1] / p[2]
        p2 = Hm @ np.array([u + 1, v, 1.0])
        p3 = Hm @ np.array([u, v + 1, 1.0])
        dx = np.hypot(p2[0] / p2[2] - x, p2[1] / p2[2] - y)
        dy = np.hypot(p3[0] / p3[2] - x, p3[1] / p3[2] - y)
        return math.sqrt(max(1e-9, dx * dy))

    def _level(self, Hm):
        s = self._scale_at(Hm, self.w / 2, self.h / 2)
        L = int(np.clip(math.floor(math.log2(1.0 / s) + 0.35), 0, 5)) if s < 1 else 0
        return L, s

    def warp_rgba(self, Hm):
        """Premultiplied RGBA warp with antialiased edges (for posters on a wall)."""
        L, s = self._level(Hm)
        img, sx, sy = self.levels[L]
        S = np.array([[1 / sx, 0, -2 / sx], [0, 1 / sy, -2 / sy], [0, 0, 1.0]])
        interp = cv2.INTER_CUBIC if s > 0.9 else cv2.INTER_LINEAR
        out = cv2.warpPerspective(img, Hm @ S, (W, H), flags=interp,
                                  borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        a = np.clip(out[..., 3], 0, 1)
        return np.clip(out[..., :3], 0, None), a

    def warp_full(self, Hm):
        """Full-frame warp for macro shots (edges reflected, never meant to be seen)."""
        L, s = self._level(Hm)
        img, sx, sy = self.full[L]
        S = np.array([[1 / sx, 0, 0], [0, 1 / sy, 0], [0, 0, 1.0]])
        interp = cv2.INTER_CUBIC if s > 0.9 else cv2.INTER_LINEAR
        out = cv2.warpPerspective(img, Hm @ S, (W, H), flags=interp,
                                  borderMode=cv2.BORDER_REFLECT_101)
        return np.clip(out, 0, 1)


def load_posters():
    d = os.path.join(ASSETS, "posters")
    files = {
        "clock": "clock_dont_waste_time.jpg",
        "gt3black": "porsche_gt3rs_black.jpg",
        "gt3blue": "porsche_911gt3_blue.jpg",
        "rsblue": "porsche_gt3rs_blue_rear.jpg",
        "supra": "toyota_supra_mk5.jpg",
        "peaky": "peaky_blinders.jpg",
        "cr7": "cr7.jpg",
    }
    return {k: Poster(k, os.path.join(d, v)) for k, v in files.items()}


def macro_cam(target, scale, yaw=0.0, pitch=0.0, roll=0.0):
    """Camera over a poster whose world units are source pixels."""
    return Cam(target, FOCAL / scale, yaw, pitch, roll)


def render_macro(poster, cam, dof=0.0, focus=None):
    img = poster.warp_full(cam.wall_H())
    return variable_blur(img, dof_map(cam, dof, focus))


def motion_samples(cam_a, cam_b, cap=14):
    """How many sub-frame samples are needed between two camera states."""
    pts = [(W * x, H * y) for x in (0.1, 0.5, 0.9) for y in (0.1, 0.5, 0.9)]
    Ha, Hb = cam_a.wall_H(), cam_b.wall_H()
    Hai = np.linalg.inv(Ha)
    m = 0.0
    for (x, y) in pts:
        w = Hai @ np.array([x, y, 1.0])
        p = Hb @ w
        m = max(m, math.hypot(p[0] / p[2] - x, p[1] / p[2] - y))
    return int(np.clip(math.ceil(m / 2.5), 1, cap))


# ------------------------------------------------------------------- type ---

FONT_FILES = {w: os.path.join(ASSETS, "fonts", f"jost-{w}.ttf") for w in (300, 400, 500, 600, 700)}
_fonts, _masks = {}, {}


def font(weight, size):
    k = (weight, size)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(FONT_FILES[weight], size)
    return _fonts[k]


def text_mask(text, size, weight=500, track=0.0):
    """Alpha mask of a tracked, kerned single line. Returns (mask, cap_center_y, width)."""
    k = (text, size, weight, track)
    if k in _masks:
        return _masks[k]
    f = font(weight, size)
    asc, desc = f.getmetrics()
    xs, x = [], 0.0
    for i, ch in enumerate(text):
        xs.append(x)
        adv = f.getlength(ch)
        kern = 0.0
        if i + 1 < len(text):
            kern = f.getlength(ch + text[i + 1]) - adv - f.getlength(text[i + 1])
        x += adv + kern + (track * size if i + 1 < len(text) else 0)
    width = x
    pad = int(size * 0.35) + 4
    ss = 2  # supersample for crisp, even edges
    img = Image.new("L", (int((width + 2 * pad) * ss), int((asc + desc + 2 * pad) * ss)), 0)
    d = ImageDraw.Draw(img)
    fs = font(weight, size * ss)
    for ch, x0 in zip(text, xs):
        d.text(((pad + x0) * ss, pad * ss), ch, font=fs, fill=255)
    img = img.resize((int(width + 2 * pad), int(asc + desc + 2 * pad)), Image.LANCZOS)
    a = np.asarray(img, np.float32) / 255.0
    bb = f.getbbox("H")
    cap_c = pad + (bb[1] + bb[3]) / 2.0
    _masks[k] = (a, cap_c, width, pad)
    return _masks[k]


def text_width(text, size, weight=500, track=0.0):
    return text_mask(text, size, weight, track)[2]


def draw_mask(frame, mask, x0, y0, color, opacity=1.0, clip=None):
    """Composite alpha mask with top-left at (x0, y0)."""
    if opacity <= 0.002:
        return frame
    mh, mw = mask.shape
    xi, yi = int(math.floor(x0)), int(math.floor(y0))
    fx, fy = x0 - xi, y0 - yi
    if abs(fx) > 1e-3 or abs(fy) > 1e-3:
        M = np.float32([[1, 0, fx], [0, 1, fy]])
        mask = cv2.warpAffine(mask, M, (mw + 1, mh + 1), flags=cv2.INTER_LINEAR)
        mh, mw = mask.shape
    X0, Y0 = max(0, xi), max(0, yi)
    X1, Y1 = min(W, xi + mw), min(H, yi + mh)
    if clip is not None:
        Y0, Y1 = max(Y0, int(clip[0])), min(Y1, int(clip[1]))
    if X1 <= X0 or Y1 <= Y0:
        return frame
    a = mask[Y0 - yi:Y1 - yi, X0 - xi:X1 - xi][..., None] * opacity
    reg = frame[Y0:Y1, X0:X1]
    frame[Y0:Y1, X0:X1] = reg * (1 - a) + np.asarray(color, np.float32) * a
    return frame


def draw_text(frame, text, size, weight, track, color, x, cy, anchor="left",
              opacity=1.0, blur=0.0, dy=0.0, clip=None, scale=1.0):
    mask, cap_c, width, pad = text_mask(text, size, weight, track)
    if scale != 1.0:
        mask = cv2.resize(mask, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        cap_c, width, pad = cap_c * scale, width * scale, pad * scale
    if blur > 0.3:
        b = int(blur * 3) + 2
        mask = cv2.GaussianBlur(cv2.copyMakeBorder(mask, b, b, b, b, cv2.BORDER_CONSTANT, 0),
                                (0, 0), blur)
        pad += b
        cap_c += b
    if anchor == "center":
        left = x - width / 2
    elif anchor == "right":
        left = x - width
    else:
        left = x
    return draw_mask(frame, mask, left - pad, cy - cap_c + dy, color, opacity, clip)


def rect(frame, x0, y0, x1, y1, color, opacity=1.0):
    """Antialiased axis-aligned filled rectangle (sub-pixel edges)."""
    if opacity <= 0 or x1 <= x0 or y1 <= y0:
        return frame
    X0, X1 = max(0, int(math.floor(x0))), min(W, int(math.ceil(x1)))
    Y0, Y1 = max(0, int(math.floor(y0))), min(H, int(math.ceil(y1)))
    if X1 <= X0 or Y1 <= Y0:
        return frame
    xs = np.arange(X0, X1) + 0.5
    ys = np.arange(Y0, Y1) + 0.5
    ax = np.clip(np.minimum(xs - x0 + 0.5, x1 - xs + 0.5), 0, 1)
    ay = np.clip(np.minimum(ys - y0 + 0.5, y1 - ys + 0.5), 0, 1)
    a = (ay[:, None] * ax[None, :])[..., None] * opacity
    frame[Y0:Y1, X0:X1] = frame[Y0:Y1, X0:X1] * (1 - a) + np.asarray(color, np.float32) * a
    return frame

# -------------------------------------------------------------- finishing ---


def _sig(x):
    return 1 / (1 + np.exp(-6 * (x - 0.5)))


_S0, _S1 = _sig(0.0), _sig(1.0)


def grade(img):
    x = np.maximum(img, 0)
    knee = 0.82
    x = np.where(x > knee, knee + (1 - knee) * np.tanh((x - knee) / (1 - knee)), x)
    s = (_sig(x) - _S0) / (_S1 - _S0)
    x = 0.8 * x + 0.2 * s
    return (0.022 + x * (0.982 - 0.022)).astype(np.float32)


_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
_r = np.sqrt(((_xx - W / 2) / (W * 0.62)) ** 2 + ((_yy - H / 2) / (H * 0.62)) ** 2)
VIGNETTE = (1.0 - 0.16 * np.clip(_r - 0.35, 0, None) ** 1.6).astype(np.float32)[..., None]
del _yy, _xx, _r

_rng = np.random.default_rng(297)
GRAIN = []
for _ in range(6):
    g = _rng.standard_normal((H, W)).astype(np.float32)
    g = cv2.GaussianBlur(g, (0, 0), 0.65)
    GRAIN.append(g / g.std())


def finish(img, f, grain=0.014, vignette=True):
    x = img * VIGNETTE if vignette else img
    g = np.roll(GRAIN[f % 6], ((f * 373) % H, (f * 197) % W), axis=(0, 1))
    lum = x.mean(axis=2, keepdims=True)
    amp = grain * (0.35 + 2.6 * lum * (1 - lum))
    x = x + g[..., None] * amp
    return np.clip(x * 255 + 0.5, 0, 255).astype(np.uint8)
