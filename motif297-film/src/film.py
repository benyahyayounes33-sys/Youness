"""MOTIF 297 — "Walls With a Point of View" — shot timeline and render.

100 BPM -> one beat = 18 frames at 30 fps. Every cut and hit sits on that grid.
Run:  python3 film.py            (full render, 3 versions + audio mux)
      python3 film.py stills 0 18 72 ...   (QC stills)
"""
import json
import math
import os
import subprocess
import sys
from multiprocessing import get_context

import numpy as np
import cv2

from engine import (W, H, FPS, FOCAL, OBSIDIAN, PAPER, CONCRETE, RUST, Cam, key, ramp, c01,
                    e_lin, e_out_expo, e_in_expo, e_out_cubic, e_in_cubic, e_inout_cubic,
                    e_inout_sine, e_out_quint, macro_cam, render_macro, variable_blur, dof_map,
                    blur_fast, bloom, grade, finish, load_posters, motion_samples, draw_text,
                    draw_mask, text_mask, text_width, font, rect)

BEAT = 18
TOTAL = 846  # 28.2 s

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "deliverables")

P = None
WALL = None

# --------------------------------------------------------------- the wall ---

SLOT_W, SLOT_H = 21.0, 29.7          # A4 in cm
LAYOUT = {                            # 2-3-2 arrangement, 6 cm gutters
    "clock": (-13.5, -35.7), "gt3blue": (13.5, -35.7),
    "cr7": (-27.0, 0.0), "gt3black": (0.0, 0.0), "supra": (27.0, 0.0),
    "rsblue": (-13.5, 35.7), "peaky": (13.5, 35.7),
}
# landing frame (poster flat on the wall) — all on the beat grid
LAND = {"gt3black": 432, "clock": 468, "supra": 486, "rsblue": 504,
        "gt3blue": 513, "cr7": 522, "peaky": 531}
LIGHT_DIR = np.array([0.42, 0.55, 1.0]) / np.linalg.norm([0.42, 0.55, 1.0])


def sbox(x, a, b, soft):
    lo = np.clip((x - a) / soft + 0.5, 0, 1)
    hi = np.clip((b - x) / soft + 0.5, 0, 1)
    lo = lo * lo * (3 - 2 * lo)
    hi = hi * hi * (3 - 2 * hi)
    return lo * hi


class WallWorld:
    PPC, LPC = 6.0, 2.0
    X0, X1, Y0, Y1 = -170.0, 170.0, -240.0, 240.0

    def __init__(self):
        w, h = int((self.X1 - self.X0) * self.PPC), int((self.Y1 - self.Y0) * self.PPC)
        rng = np.random.default_rng(29)
        noise = np.zeros((h, w), np.float32)
        for cell, amp in [(140, 0.016), (45, 0.012), (12, 0.010), (3, 0.008)]:
            gw, gh = max(2, w // cell), max(2, h // cell)
            n = rng.standard_normal((gh, gw)).astype(np.float32)
            noise += amp * cv2.resize(n, (w, h), interpolation=cv2.INTER_CUBIC)
        pores = (rng.random((h, w)) > 0.9985).astype(np.float32)
        noise -= 0.06 * cv2.GaussianBlur(pores, (0, 0), 0.8) * 6
        base = CONCRETE * 0.26 + PAPER * 0.74
        self.albedo = (base[None, None, :] * (1 + noise[..., None])).astype(np.float32)
        self.T = np.array([[self.PPC, 0, -self.X0 * self.PPC], [0, self.PPC, -self.Y0 * self.PPC], [0, 0, 1.0]])
        lw, lh = int((self.X1 - self.X0) * self.LPC), int((self.Y1 - self.Y0) * self.LPC)
        xs = self.X0 + (np.arange(lw) + 0.5) / self.LPC
        ys = self.Y0 + (np.arange(lh) + 0.5) / self.LPC
        self.LX, self.LY = [a.astype(np.float32) for a in np.meshgrid(xs, ys)]
        self.TL = np.array([[self.LPC, 0, -self.X0 * self.LPC], [0, self.LPC, -self.Y0 * self.LPC], [0, 0, 1.0]])

    def light_tex(self, sun_x, sun_y, amt):
        X, Y = self.LX, self.LY
        amb = 0.875 + 0.05 * np.clip(-X / 150, -1, 1) - 0.07 * (Y / 230) ** 2
        u = (X - sun_x) - 0.45 * (Y - sun_y)
        v = Y - sun_y
        s = 6.0
        mu = sbox(u, 0, 26, s) + sbox(u, 29.5, 55.5, s)
        mv = sbox(v, 0, 34, s) + sbox(v, 37.5, 71.5, s) + sbox(v, 75, 109, s)
        sun = (amt * mu * mv)[..., None]
        L = amb[..., None] * np.array([0.965, 0.985, 1.0], np.float32) + \
            sun * np.array([1.0, 0.91, 0.76], np.float32) * 0.23
        return L.astype(np.float32)


def poster_dims(p):
    ar = p.w / p.h
    if ar > SLOT_W / SLOT_H:
        return SLOT_W, SLOT_W / ar
    return SLOT_H * ar, SLOT_H


def poster_state(name, f):
    """3D pose of a poster at frame f (None before it enters)."""
    p = P[name]
    cx, cy = LAYOUT[name]
    wc, hc = poster_dims(p)
    land = LAND[name]
    if name == "gt3black":
        start = land - 18
        if f < start:
            return None
        pt = e_out_cubic(c01((f - start) / 13.0))
        ft = e_inout_cubic(c01((f - start - 4) / 14.0))
        dx, dy, z = 30 * (1 - pt), 24 * (1 - pt), -20 * (1 - pt)
        phi = 38 * (1 - ft)
        op = c01((f - start) / 2.0)
    else:
        start = land - 8
        if f < start:
            return None
        t = e_out_cubic(c01((f - start) / 8.0))
        dx, dy, z = 0.0, -3.0 * (1 - t), -7.0 * (1 - t)
        phi = 24 * (1 - t)
        op = c01((f - start) / 2.5)
    ph = math.radians(phi)
    O = np.array([cx - wc / 2 + dx, cy - hc / 2 + dy, z])
    a = np.array([wc / p.w, 0, 0])
    b = np.array([0, hc / p.h * math.cos(ph), -hc / p.h * math.sin(ph)])
    corners = [O, O + a * p.w, O + a * p.w + b * p.h, O + b * p.h]
    return dict(name=name, O=O, a=a, b=b, op=op, corners=corners)


def quad_mask(pts):
    m = np.zeros((H, W), np.float32)
    q = np.round(np.asarray(pts) * 16).astype(np.int32)
    cv2.fillConvexPoly(m, q, 1.0, lineType=cv2.LINE_AA, shift=4)
    return m


def render_wall(cam, f, names, sun_x, sun_y=-70.0, dof=0.0, focus=None):
    Hw = cam.wall_H()
    alb = cv2.warpPerspective(WALL.albedo, Hw @ np.linalg.inv(WALL.T), (W, H),
                              flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    light = cv2.warpPerspective(WALL.light_tex(sun_x, sun_y, 1.0), Hw @ np.linalg.inv(WALL.TL),
                                (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    img = alb * light
    states = [s for s in (poster_state(n, f) for n in names) if s is not None]
    if states:
        shade = np.ones((H, W), np.float32)
        for s in states:
            c3 = np.array(s["corners"])
            hmax = float(max(0.0, -c3[:, 2].min()))
            centre = c3.mean(axis=0)
            _, depth = cam.project(np.array([centre[0], centre[1], 0.0]))
            kpx = FOCAL / max(depth, 1.0)
            # shadow cast along the light direction (+ paper thickness offset)
            sh = [c - (c[2] / LIGHT_DIR[2]) * LIGHT_DIR + np.array([0.10, 0.14, 0]) for c in c3]
            pts = [cam.project(np.array([q[0], q[1], 0.0]))[0] for q in sh]
            m = quad_mask(pts)
            sig = kpx * (0.16 + 0.11 * hmax)
            op = 0.36 / (1 + 0.05 * hmax) * s["op"]
            shade *= 1 - op * np.clip(blur_fast(m, sig), 0, 1)
            pts2 = [cam.project(np.array([q[0] + 0.3, q[1] + 0.45, 0.0]))[0] for q in sh]
            m2 = quad_mask(pts2)
            shade *= 1 - 0.11 * s["op"] * np.clip(blur_fast(m2, kpx * (1.0 + 0.15 * hmax)), 0, 1)
        img *= shade[..., None]
        for s in states:
            Hp = cam.plane_H(s["O"], s["a"], s["b"])
            rgb, a = P[s["name"]].warp_rgba(Hp)
            op = s["op"]
            img = rgb * light * op + img * (1 - a[..., None] * op)
    return variable_blur(img, dof_map(cam, dof, focus))

# ------------------------------------------------------------------ shots ---
# Each shot: cam(f) -> Cam (used for motion-blur sampling), plate(f) -> graded footage.


def cam_A(f):
    s = key(f, [(0, 3.25), (18, 3.25), (56, 2.95, e_inout_sine), (72, 4.6, e_in_expo)])
    yaw = key(f, [(18, 0), (62, -12, e_inout_sine)])
    pitch = key(f, [(18, 0), (62, 8, e_inout_sine)])
    tx = 392 + key(f, [(18, 0), (62, -28, e_inout_sine)])
    return macro_cam((tx, 257.5 + TAIL_DY), s, yaw, pitch, -1.2)


TAIL_DY = 58.0
LINE_Y = 960 - TAIL_DY * 3.25


def plate_A(f):
    img = render_macro(P["gt3black"], cam_A(f), key(f, [(18, 0), (44, 26, e_inout_sine)]))
    red = np.clip((img[..., 0] - np.maximum(img[..., 1], img[..., 2]) - 0.10) * 4, 0, 1)
    v_red = key(f, [(9, 0), (18, 1, e_in_cubic)])
    v_all = key(f, [(15, 0), (32, 1, e_out_cubic)])
    vis = np.maximum(v_all, v_red * red)[..., None]
    img = img * vis + OBSIDIAN * 0.6 * (1 - vis)
    exp = key(f, [(54, 1.0), (72, 5.0, e_in_expo)])
    img = bloom(img * exp, 0.7, 40, 0.35 + 0.8 * ramp(f, 56, 72, e_in_cubic))
    w = ramp(f, 63, 72, e_in_cubic)
    img = img * (1 - w) + PAPER * 1.25 * w
    img = grade(img)
    # the opening hairline: draws out from the centre, then melts into the taillight
    if f < 26:
        half = 351 * e_out_expo(c01(f / 13.0))
        m = ramp(f, 9, 21, e_inout_cubic)
        thick = 2.0 + 30 * m
        op = 1 - ramp(f, 13, 25, e_inout_cubic)
        line = np.zeros((H, W), np.float32)
        rect_mask(line, 540 - half, LINE_Y + 1 - thick / 2, 540 + half, LINE_Y + 1 + thick / 2)
        if m > 0:
            line = blur_fast(line, 0.5 + 7 * m)
        glow = blur_fast(line, 9) * 0.9 + blur_fast(line, 42) * 1.4
        col = RUST * 1.25
        img = img * (1 - line[..., None] * op) + col * line[..., None] * op
        img = img + col * glow[..., None] * op * 0.55
        if f < 16:  # bright tips while drawing
            tip = np.zeros((H, W), np.float32)
            for x in (540 - half, 540 + half):
                rect_mask(tip, x - 3, LINE_Y - 1, x + 3, LINE_Y + 3)
            img = img + np.array([1, .75, .65], np.float32) * blur_fast(tip, 6)[..., None] * 3.0 * (1 - ramp(f, 10, 16))
    return np.clip(img, 0, 1.2)


def rect_mask(m, x0, y0, x1, y1, v=1.0):
    X0, X1 = max(0, int(math.floor(x0))), min(W, int(math.ceil(x1)))
    Y0, Y1 = max(0, int(math.floor(y0))), min(H, int(math.ceil(y1)))
    if X1 <= X0 or Y1 <= Y0:
        return
    xs = np.arange(X0, X1) + 0.5
    ys = np.arange(Y0, Y1) + 0.5
    ax = np.clip(np.minimum(xs - x0 + 0.5, x1 - xs + 0.5), 0, 1)
    ay = np.clip(np.minimum(ys - y0 + 0.5, y1 - ys + 0.5), 0, 1)
    m[Y0:Y1, X0:X1] = np.maximum(m[Y0:Y1, X0:X1], ay[:, None] * ax[None, :] * v)


# B — the clock: follow the melting drip down (focus plane runs along the drip)
def cam_B(f):
    ty = key(f, [(72, 610), (106, 800, e_inout_sine), (117, 1180, e_in_expo)])
    tx = key(f, [(72, 196), (106, 189), (117, 188)])
    return macro_cam((tx, ty), 3.4, YAW_B, 0, 0)


YAW_B = 32


def plate_B(f):
    img = render_macro(P["clock"], cam_B(f), 44)
    exp = key(f, [(72, 3.4), (88, 1.0, e_out_expo)])
    return grade(bloom(img * exp, 0.85, 30, 0.2 * (exp - 1)))


# C — Supra brush lettering: the same downward motion lands on ink drips
def cam_C(f):
    ty = key(f, [(117, 430), (131, 664, e_out_expo), (153, 680, e_lin)])
    tx = key(f, [(117, 420), (145, 446, e_lin), (153, 1200, e_in_expo)])
    return macro_cam((tx, ty), 3.3, -6, -24, 0)


def plate_C(f):
    return grade(render_macro(P["supra"], cam_C(f), 30))


# D — CR letterforms: whip lands, focus on the type, the figure falls out of focus
def cam_D(f):
    tx = key(f, [(153, -420), (165, 300, e_out_expo), (189, 330, e_lin)])
    return macro_cam((tx, 430), 3.6, 10, 26, 0)


def plate_D(f):
    return grade(render_macro(P["cr7"], cam_D(f), 34))


# E — editorial title type, slow track, then a roll that spins into the wheel
def cam_E(f):
    tx = key(f, [(189, 206), (225, 300, e_lin)])
    s = key(f, [(189, 3.2), (225, 3.5, e_lin)])
    roll = key(f, [(189, 0), (214, 1.5, e_lin), (225, 42, e_in_expo)])
    return macro_cam((tx, 682), s, -14, -22, roll)


def plate_E(f):
    return grade(render_macro(P["peaky"], cam_E(f), 34))


# F — wheel: the roll resolves, then a push through the hub
def cam_F(f):
    roll = key(f, [(225, -42), (238, -4, e_out_expo), (251, 0, e_lin)])
    s = key(f, [(225, 4.0), (251, 4.3, e_lin), (261, 9.5, e_in_expo)])
    return macro_cam((214, 540), s, -14, 12, roll)


def plate_F(f):
    return grade(render_macro(P["gt3blue"], cam_F(f), 30))


# G — the push lands on a full beauty frame of the car, then light floods to paper
def cam_G(f):
    s = key(f, [(261, 2.25), (273, 2.75, e_out_expo), (297, 2.95, e_lin)])
    tx = key(f, [(261, 262), (297, 250, e_lin)])
    return macro_cam((tx, 655), s, 12, -14, 0)


def plate_G(f):
    img = render_macro(P["rsblue"], cam_G(f), 26)
    exp = key(f, [(283, 1.0), (297, 3.6, e_in_expo)])
    img = bloom(img * exp, 0.75, 40, 0.3 + 0.6 * ramp(f, 283, 297, e_in_cubic))
    w = ramp(f, 289, 297, e_in_cubic)
    img = img * (1 - w) + PAPER * 1.1 * w
    return grade(img)


# --- H: the format card (A4, 210 x 297 mm) -----------------------------------

_rng = np.random.default_rng(11)
_fib = _rng.standard_normal((H // 2, W // 2)).astype(np.float32)
_fib = cv2.GaussianBlur(_fib, (0, 0), sigmaX=3.0, sigmaY=0.7)
_fib = cv2.resize(_fib / _fib.std(), (W, H), interpolation=cv2.INTER_CUBIC)
_gy, _gx = np.mgrid[0:H, 0:W].astype(np.float32)
_grad = (1.035 - 0.10 * ((_gx / W) * 0.4 + (_gy / H) * 0.6)).astype(np.float32)
PAPER_TEX = (PAPER[None, None, :] * (_grad * (1 + 0.010 * _fib))[..., None]).astype(np.float32)
OBS_TEX = (OBSIDIAN[None, None, :] * (1.0 + 0.10 * np.exp(-(((_gx - W / 2) / 700) ** 2 + ((_gy - H * 0.47) / 900) ** 2))
                                      + 0.02 * _fib)[..., None]).astype(np.float32)
del _gy, _gx

A4_W, A4_H = 500.0, 500.0 * 297 / 210   # on-screen at zoom 1


def h_zoom(f):
    return key(f, [(297, 1.0), (339, 1.07, e_lin), (351, 3.3, e_in_cubic)])


def a4_outline(img, cx, cy, w, h, prog, color, op, th=2.0):
    """Trim-path rectangle, clockwise from the top-left corner."""
    if prog <= 0 or op <= 0:
        return
    segs = [((cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2)),
            ((cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2)),
            ((cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)),
            ((cx - w / 2, cy + h / 2), (cx - w / 2, cy - h / 2))]
    per = 2 * (w + h)
    left = prog * per
    for (x0, y0), (x1, y1) in segs:
        L = abs(x1 - x0) + abs(y1 - y0)
        if left <= 0:
            break
        t = min(1.0, left / L)
        xe, ye = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        rect(img, min(x0, xe) - th / 2, min(y0, ye) - th / 2, max(x0, xe) + th / 2, max(y0, ye) + th / 2, color, op)
        left -= L


def dim_line(img, x0, y0, x1, y1, prog, color, op, th=2.0, tick=16):
    """Dimension line drawn from its centre outwards, with end ticks."""
    if prog <= 0:
        return
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    ax, ay = mx + (x0 - mx) * prog, my + (y0 - my) * prog
    bx, by = mx + (x1 - mx) * prog, my + (y1 - my) * prog
    rect(img, min(ax, bx) - th / 2, min(ay, by) - th / 2, max(ax, bx) + th / 2, max(ay, by) + th / 2, color, op)
    tk = ramp(prog, 0.85, 1.0, e_out_cubic) * tick
    if tk > 0:
        if abs(y1 - y0) < 1e-3:   # horizontal
            for x in (ax, bx):
                rect(img, x - th / 2, my - tk / 2, x + th / 2, my + tk / 2, color, op)
        else:
            for y in (ay, by):
                rect(img, mx - tk / 2, y - th / 2, mx + tk / 2, y + th / 2, color, op)


def h_geom(f):
    z = h_zoom(f)
    cx, cy = 540.0, 930.0
    return z, cx, cy, A4_W * z, A4_H * z


def zoom_tex(tex, z):
    if abs(z - 1) < 1e-4:
        return tex.copy()
    M = np.float32([[z, 0, 540 * (1 - z)], [0, z, 960 * (1 - z)]])
    return cv2.warpAffine(tex, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)


def plate_H(f):
    z, cx, cy, w, h = h_geom(f)
    cyz = 960 + (cy - 960) * z
    img = zoom_tex(PAPER_TEX, z)
    # the A4 window opens onto the wall
    wv = ramp(f, 331, 343, e_inout_cubic)
    if wv > 0:
        wall = grade(render_wall(cam_I(f), f, [], sun_x(f)))
        m = np.zeros((H, W), np.float32)
        rect_mask(m, cx - w / 2, cyz - h / 2, cx + w / 2, cyz + h / 2)
        m = m[..., None] * wv
        img = img * (1 - m) + wall * m
    prog = ramp(f, 300, 320, e_inout_cubic)
    a4_outline(img, cx, cyz, w, h, prog, OBSIDIAN, 0.85)
    gap = 54 * z
    dp = ramp(f, 307, 326, e_out_expo)
    dim_line(img, cx - w / 2, cyz - h / 2 - gap, cx + w / 2, cyz - h / 2 - gap, dp, RUST, 1.0)
    dim_line(img, cx + w / 2 + gap, cyz - h / 2, cx + w / 2 + gap, cyz + h / 2, dp, RUST, 1.0)
    return img


def samples_H(f):
    if f < 338:
        return 1
    zt = h_zoom(f + 0.25) / h_zoom(f - 0.25)
    return int(np.clip(math.ceil((zt - 1) * 1100 / 2.5), 1, 14))


# --- I: the wall — blank, then a point of view --------------------------------

def sun_x(f):
    return key(f, [(331, -52), (540, -34, e_lin), (594, -6, e_inout_cubic), (680, 4, e_lin)])


def cam_I(f):
    if f < 351:
        k = 8.4 * h_zoom(f) / h_zoom(351)
    else:
        k = key(f, [(351, 8.4), (365, 10.0, e_out_expo), (396, 10.6, e_lin), (414, 17.5, e_in_cubic),
                    (432, 21.0, e_out_cubic), (468, 21.6, e_lin), (558, 10.6, e_inout_cubic), (594, 11.1, e_lin)])
    cy = key(f, [(432, 0.0), (468, 0.6), (558, 1.5, e_inout_cubic)])
    return Cam((0.0, cy), FOCAL / k)


def plate_I(f):
    return grade(render_wall(cam_I(f), f, list(LAYOUT), sun_x(f)))


# --- J: the hero — perspective dolly along the finished wall ------------------

def cam_J(f):
    tx = key(f, [(594, 30), (648, -2, e_out_cubic), (668, -75, e_in_expo)])
    yaw = key(f, [(594, 31), (648, 27, e_out_cubic), (668, 42, e_in_expo)])
    return Cam((tx, -2.0), 96, yaw, 0.0, 0.0)


def plate_J(f):
    img = render_wall(cam_J(f), 700, list(LAYOUT), sun_x(f), dof=10)
    img = grade(img)
    # foreground pillar wipe (a dark object passing close to the lens)
    if f >= 650:
        edge = key(f, [(650, -260), (666, 1400, e_in_cubic)])
        xs = np.arange(W, dtype=np.float32)
        m = np.clip((edge - xs) / 90.0 + 0.5, 0, 1)
        m = m * m * (3 - 2 * m)
        rim = np.exp(-((xs - (edge - 70)) / 38.0) ** 2) * 0.05
        img = img * (1 - m[None, :, None]) + OBSIDIAN * m[None, :, None] + PAPER * rim[None, :, None]
    return img


# --- K: the brand -------------------------------------------------------------

END_A4 = (540.0, 930.0, 460.0, 460.0 * 297 / 210)


def plate_K(f):
    img = OBS_TEX.copy()
    cx, cy, w, h = END_A4
    a4_outline(img, cx, cy, w, h, ramp(f, 672, 698, e_inout_cubic), PAPER, 0.30)
    dim_line(img, cx + w / 2 + 46, cy - h / 2, cx + w / 2 + 46, cy + h / 2, ramp(f, 684, 708, e_out_expo), RUST, 1.0)
    return img


SHOTS = [
    (0, 72, cam_A, plate_A), (72, 117, cam_B, plate_B), (117, 153, cam_C, plate_C),
    (153, 189, cam_D, plate_D), (189, 225, cam_E, plate_E), (225, 261, cam_F, plate_F),
    (261, 297, cam_G, plate_G), (297, 351, None, plate_H), (351, 594, cam_I, plate_I),
    (594, 666, cam_J, plate_J), (666, TOTAL, None, plate_K),
]


def shot_at(f):
    for s in SHOTS:
        if s[0] <= f < s[1]:
            return s
    return SHOTS[-1]


def plate(f):
    """Motion-blurred, graded picture for frame f (180-degree shutter)."""
    f0, f1, cam, fn = shot_at(f)
    if cam is not None:
        n = motion_samples(cam(f - 0.25), cam(f + 0.25))
        if 414 <= f <= 432:
            n = max(n, 12)
        elif fn is plate_I and any(LAND[k] - 8 <= f <= LAND[k] for k in LAND):
            n = max(n, 6)
    elif fn is plate_H:
        n = samples_H(f)
    else:
        n = 1
    if n <= 1:
        return fn(float(f))
    acc = None
    for i in range(n):
        t = f - 0.25 + 0.5 * (i + 0.5) / n
        t = min(max(t, f0), f1 - 1e-3)
        im = fn(t)
        acc = im if acc is None else acc + im
    return acc / n

# ------------------------------------------------------------- typography ---


def char_layout(text, size, weight, track):
    fnt = font(weight, size)
    xs, x = [], 0.0
    for i, ch in enumerate(text):
        xs.append(x)
        adv = fnt.getlength(ch)
        kern = fnt.getlength(ch + text[i + 1]) - adv - fnt.getlength(text[i + 1]) if i + 1 < len(text) else 0
        x += adv + kern + (track * size if i + 1 < len(text) else 0)
    return xs, x


def headline(img, f, words, cy, size, f_exit, color, track=0.05, weight=500):
    sp = font(weight, size).getlength(" ") + track * size
    widths = [text_width(w, size, weight, track) for w, _ in words]
    x = 540 - (sum(widths) + sp * (len(words) - 1)) / 2
    xt = ramp(f, f_exit, f_exit + 7, e_in_cubic)
    for (wd, fi), ww in zip(words, widths):
        t = ramp(f, fi, fi + 10)
        if t > 0 and xt < 1:
            clip = (cy - size * 0.62, cy + size * 0.62) if xt == 0 else None
            draw_text(img, wd, size, weight, track, color, x, cy, opacity=1 - xt,
                      dy=(1 - t) * size * 0.95 - xt * 16, clip=clip, blur=xt * 9)
        x += ww + sp


def label(img, f, f_in, f_out, text, y=1352, x=96):
    """Gallery-placard tag: Warm Paper slip, rust index square, tracked caps."""
    if f < f_in or f > f_out + 7:
        return
    op = 1 - ramp(f, f_out, f_out + 6, e_in_cubic)
    size, track, h = 24, 0.32, 46
    tw = text_width(text, size, 500, track)
    full = 18 + 10 + 14 + tw + 22
    tb = ramp(f, f_in, f_in + 10)
    rect(img, x, y - h / 2, x + full * tb, y + h / 2, PAPER, 0.95 * op)
    rect(img, x + 18, y - 5, x + 28, y + 5, RUST, op * ramp(f, f_in + 4, f_in + 9))
    t = ramp(f, f_in + 5, f_in + 15)
    draw_text(img, text, size, 500, track, OBSIDIAN, x + 42, y, opacity=op * min(1, t * 1.4),
              dy=(1 - t) * 20, clip=(y - h / 2 + 2, y + h / 2 - 2))


def digits(img, value, ndig, cx, cy, size, color, op, weight=400):
    s = str(int(round(value))).zfill(ndig)
    cell = size * 0.6
    x0 = cx - cell * ndig / 2
    for i, ch in enumerate(s):
        draw_text(img, ch, size, weight, 0, color, x0 + cell * (i + 0.5), cy, anchor="center", opacity=op)


def text_rot(img, text, size, weight, track, color, cx, cy, op):
    """Text rotated 90 degrees (reads bottom to top), centred at (cx, cy)."""
    m, cap_c, width, pad = text_mask(text, size, weight, track)
    r = np.ascontiguousarray(np.rot90(m))   # (y, x) -> (mw-1-x, y)
    mw = m.shape[1]
    draw_mask(img, r, cx - cap_c, cy - (mw - 1 - pad - width / 2), color, op)


def text_layer(img, f):
    # craft labels (placeholder theme names — swap for real collection names)
    label(img, f, 82, 108, "ART")
    label(img, f, 125, 145, "AUTOMOTIVE")
    label(img, f, 162, 183, "SPORT")
    label(img, f, 197, 214, "CINEMA")
    # format card
    if 300 <= f < 351:
        z, cx, cy, w, h = h_geom(f)
        cyz = 960 + (cy - 960) * z
        gap = 54 * z
        cnt = ramp(f, 309, 331, e_out_expo)
        op = ramp(f, 309, 314, e_lin) * (1 - ramp(f, 339, 345, e_in_cubic))
        digits(img, 210 * cnt, 3, cx - 28 * z, cyz - h / 2 - gap - 38 * z, int(36 * z), OBSIDIAN, op)
        draw_text(img, "MM", int(19 * z), 500, 0.2, OBSIDIAN, cx + 36 * z, cyz - h / 2 - gap - 38 * z, opacity=op * 0.7)
        text_rot(img, "MM", int(19 * z), 500, 0.2, OBSIDIAN, cx + w / 2 + gap + 38 * z, cyz - 66 * z, op * 0.7)
        digits_rot(img, 297 * cnt, cx + w / 2 + gap + 38 * z, cyz + 24 * z, int(36 * z), OBSIDIAN, op)
        lt = ramp(f, 322, 334)
        lop = lt * (1 - ramp(f, 339, 345, e_in_cubic))
        draw_text(img, "A4 ADHESIVE ART POSTERS", int(round(30 * z)), 500, 0.30, OBSIDIAN, 540,
                  cyz + h / 2 + 80 * z, anchor="center", opacity=lop * 0.9, dy=(1 - lt) * 20,
                  clip=(cyz + h / 2 + 80 * z - 20 * z, cyz + h / 2 + 80 * z + 20 * z))
    # the blank wall
    headline(img, f, [("A", 360), ("BLANK", 363), ("WALL", 366)], 900, 68, 402, OBSIDIAN)
    headline(img, f, [("SAYS", 378), ("NOTHING.", 382)], 994, 68, 402, OBSIDIAN)
    headline(img, f, [("SAY", 441), ("SOMETHING.", 445)], 1310, 54, 466, OBSIDIAN)
    # the brand
    if f >= 700:
        cx, cy, w, h = END_A4
        for word, wcy, f_in, weight in (("MOTIF", 876, 702, 500), ("297", 998, 710, 400)):
            size, track = 108, 0.14
            xs, tw = char_layout(word, size, weight, track)
            x0 = 540 - tw / 2
            for i, ch in enumerate(word):
                t = ramp(f, f_in + 2 * i, f_in + 2 * i + 14)
                if t > 0:
                    draw_text(img, ch, size, weight, 0, PAPER, x0 + xs[i], wcy, opacity=min(1, t * 1.3),
                              dy=(1 - t) * 100, clip=(wcy - 64, wcy + 64))
        text_rot(img, "297 MM", 22, 500, 0.32, RUST, cx + w / 2 + 46 + 28, cy, ramp(f, 712, 724, e_lin))
        words = ["WALLS", "WITH", "A", "POINT", "OF", "VIEW"]
        size, track, weight = 32, 0.26, 500
        sp = font(weight, size).getlength(" ") + track * size
        widths = [text_width(wd, size, weight, track) for wd in words]
        dotw = text_width(".", size, weight, 0)
        x = 540 - (sum(widths) + sp * (len(words) - 1) + dotw + 4) / 2
        ycap = cy + h / 2 + 100
        for i, (wd, ww) in enumerate(zip(words, widths)):
            t = ramp(f, 738 + 3 * i, 750 + 3 * i)
            draw_text(img, wd, size, weight, track, PAPER, x, ycap, opacity=t, blur=(1 - t) * 6)
            x += ww + (sp if i < len(words) - 1 else 2)
        t = ramp(f, 762, 768, e_out_cubic)
        if t > 0:
            draw_text(img, ".", size, 700, 0, RUST, x + dotw / 2 + 2, ycap, anchor="center", opacity=t,
                      scale=1 + 0.8 * (1 - t))


def digits_rot(img, value, cx, cy, size, color, op):
    s = str(int(round(value))).zfill(3)
    cell = size * 0.6
    for i, ch in enumerate(s):
        m, cap_c, width, pad = text_mask(ch, size, 400, 0)
        r = np.ascontiguousarray(np.rot90(m))
        mw = m.shape[1]
        yc = cy + cell * (1 - i)   # first digit lowest (reads bottom to top)
        draw_mask(img, r, cx - cap_c, yc - (mw - 1 - pad - width / 2), color, op)


CAPTIONS = [
    (0, 66, "[low hum · a thin tone rises]"),
    (72, 150, "[cinematic pulse · clock ticking]"),
    (150, 294, "[whooshes · paper flick · metal ring]"),
    (297, 348, "[mechanical counter clicks]"),
    (351, 414, "[music stops · a clock ticks]"),
    (414, 462, "[poster pressed onto the wall]"),
    (462, 588, "[music builds · posters tap in]"),
    (594, 648, "[music swells]"),
    (648, 684, "[deep whoosh]"),
    (690, 846, "[music resolves · one last tick]"),
]


def caption_layer(img, f):
    for f0, f1, txt in CAPTIONS:
        if f0 <= f < f1:
            op = ramp(f, f0, f0 + 5, e_lin) * (1 - ramp(f, f1 - 5, f1, e_lin))
            size = 38
            tw = text_width(txt, size, 400, 0.02)
            y = 1490
            rect(img, 540 - tw / 2 - 26, y - 34, 540 + tw / 2 + 26, y + 34, OBSIDIAN, 0.72 * op)
            draw_text(img, txt, size, 400, 0.02, PAPER, 540, y, anchor="center", opacity=op)

# ---------------------------------------------------------------- render ----


def init():
    global P, WALL
    if P is None:
        P = load_posters()
        WALL = WallWorld()


def end_drift(img, f):
    """Slow ambient push on the end card (applied to picture and type together)."""
    if f < 680:
        return img
    z = 1 + 0.03 * e_out_cubic(c01((f - 680) / 166.0))
    M = np.float32([[z, 0, 540 * (1 - z)], [0, z, 960 * (1 - z)]])
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT_101)


def render_frame(f):
    init()
    base = plate(f).astype(np.float32)
    clean = finish(end_drift(base, f), f)
    txt = base.copy()
    text_layer(txt, f)
    txt = end_drift(txt, f)
    master = finish(txt, f)
    cap = txt
    caption_layer(cap, f)
    captioned = finish(cap, f)
    return f, master.tobytes(), clean.tobytes(), captioned.tobytes()


def ffmpeg_writer(path):
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
           "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-maxrate", "16M", "-bufsize", "32M",
           "-profile:v", "high", "-level", "4.2", "-g", "30", "-tune", "film",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-movflags", "+faststart", path]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)


def render_all(workers=4, frames=None):
    os.makedirs(os.path.join(OUT, "_tmp"), exist_ok=True)
    tmp = os.path.join(OUT, "_tmp")
    outs = {k: ffmpeg_writer(os.path.join(tmp, f"{k}_video.mp4")) for k in ("master", "clean", "captions")}
    init()
    frames = list(range(TOTAL)) if frames is None else frames
    ctx = get_context("fork")
    with ctx.Pool(workers) as pool:
        for f, m, c, cp in pool.imap(render_frame, frames, chunksize=1):
            outs["master"].stdin.write(m)
            outs["clean"].stdin.write(c)
            outs["captions"].stdin.write(cp)
            if f % 30 == 0:
                print(f"frame {f}/{TOTAL}", flush=True)
    for p in outs.values():
        p.stdin.close()
        p.wait()


def stills(frames, outdir, which="master"):
    os.makedirs(outdir, exist_ok=True)
    init()
    for f in frames:
        _, m, c, cp = render_frame(f)
        buf = {"master": m, "clean": c, "captions": cp}[which]
        im = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        cv2.imwrite(os.path.join(outdir, f"f{f:04d}.png"), cv2.cvtColor(im, cv2.COLOR_RGB2BGR))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        out = os.environ.get("STILLS", "/tmp/stills")
        stills([int(x) for x in sys.argv[2:]], out, os.environ.get("WHICH", "master"))
    else:
        render_all()
