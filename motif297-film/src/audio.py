"""MOTIF 297 — original score + sound design, synthesised from scratch.

Everything is generated here (no samples, no library music), so the soundtrack
is 100% original and rights-free. Cues are locked to the picture's frame grid:
100 BPM, one beat = 18 frames = 0.6 s, sample = frame * 1600 at 48 kHz.

Outputs (deliverables/audio): music stem, SFX stem, full mix (24-bit WAV).
"""
import os
import subprocess

import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve, resample_poly

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "deliverables", "audio")

SR = 48000
FPS = 30
SPF = SR // FPS            # samples per frame
TOTAL = 846
N = TOTAL * SPF
BEAT = 18

LAND = {"gt3black": 432, "clock": 468, "supra": 486, "rsblue": 504,
        "gt3blue": 513, "cr7": 522, "peaky": 531}

rng = np.random.default_rng(297)


def T(f):
    return f / FPS


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


def noise(n):
    return rng.standard_normal(n)


def tt(dur):
    return np.arange(int(dur * SR)) / SR

# ---------------------------------------------------------------- filters ---


def _sos(kind, fc, order=2):
    return butter(order, fc, kind, fs=SR, output="sos")


def lp(x, fc, order=2):
    return sosfilt(_sos("low", min(fc, SR * 0.45), order), x, axis=-1)


def hp(x, fc, order=2):
    return sosfilt(_sos("high", fc, order), x, axis=-1)


def bp(x, lo, hi, order=2):
    return sosfilt(_sos("band", [lo, min(hi, SR * 0.45)], order), x, axis=-1)


def sweep_bp(x, fc, bw_oct=1.0, block=256):
    """Time-varying band-pass (filter state carried across blocks)."""
    out = np.zeros_like(x)
    zi = None
    for i in range(0, len(x), block):
        c = float(np.clip(fc[min(i, len(fc) - 1)], 40, SR * 0.4))
        lo, hi = c / 2 ** (bw_oct / 2), min(c * 2 ** (bw_oct / 2), SR * 0.45)
        sos = butter(2, [lo, hi], "band", fs=SR, output="sos")
        if zi is None:
            zi = np.zeros((sos.shape[0], 2))
        out[i:i + block], zi = sosfilt(sos, x[i:i + block], zi=zi)
    return out


def pan2(x, pan):
    """Equal-power pan; pan may be scalar or per-sample array in [-1, 1]."""
    th = (np.asarray(pan) + 1) * np.pi / 4
    return np.stack([x * np.cos(th), x * np.sin(th)]) * np.sqrt(2)


def place(buf, sig, t, gain=1.0, pan=0.0):
    if sig.ndim == 1:
        sig = pan2(sig, pan)
    i0 = int(round(t * SR))
    if i0 < 0:
        sig, i0 = sig[:, -i0:], 0
    i1 = min(buf.shape[1], i0 + sig.shape[1])
    if i1 > i0:
        buf[:, i0:i1] += gain * sig[:, :i1 - i0]

# -------------------------------------------------------------- oscillators ---


def saw(freq, n, phase0=0.0):
    dt = np.broadcast_to(np.asarray(freq, float) / SR, (n,))
    ph = (phase0 + np.cumsum(dt)) % 1.0
    y = 2 * ph - 1
    m = ph < dt
    x = ph[m] / dt[m]
    y[m] -= x + x - x * x - 1
    m = ph > 1 - dt
    x = (ph[m] - 1) / dt[m]
    y[m] -= x * x + x + x + 1
    return y


def sine_glide(f_curve, phase0=0.0):
    return np.sin(phase0 + 2 * np.pi * np.cumsum(f_curve) / SR)

# ------------------------------------------------------------- instruments ---


def supersaw(m, dur, voices=5, spread=0.11, seed=0):
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    f = mtof(m)
    out = np.zeros((2, n))
    for ch in range(2):
        det = np.linspace(-spread, spread, voices) + r.normal(0, 0.02, voices)
        for d in det:
            out[ch] += saw(f * 2 ** (d / 12), n, r.random())
    return out / voices


def pad_chord(buf, notes, f0, f1, gain=0.18, att=0.9, rel=1.6, bright=(0.15, 0.35), seed=1,
              hpf=110):
    dur = T(f1 - f0) + rel
    n = int(dur * SR)
    t = np.arange(n) / SR
    sus = T(f1 - f0)
    env = np.clip(t / att, 0, 1) ** 1.5
    env *= np.where(t < sus, 1.0, np.exp(-(t - sus) / (rel / 4.0)))
    b = bright[0] + (bright[1] - bright[0]) * np.clip(t / max(sus, 1e-3), 0, 1)
    acc = np.zeros((2, n))
    for i, m in enumerate(notes):
        x = supersaw(m, dur, seed=seed * 31 + i)
        x = x + 0.35 * np.sin(2 * np.pi * mtof(m) * t)[None, :]
        dark, br = lp(x, 650), lp(x, 4200)
        acc += dark * (1 - b) + br * b
    acc = hp(acc, hpf) * env / np.sqrt(len(notes))
    place(buf, acc, T(f0), gain)


def bass(buf, m, f0, f1, gain=0.32, rel=0.4):
    dur = T(f1 - f0) + rel
    t = tt(dur)
    f = mtof(m)
    sus = T(f1 - f0)
    env = np.clip(t / 0.25, 0, 1) * np.where(t < sus, 1.0, np.exp(-(t - sus) / 0.12))
    x = np.sin(2 * np.pi * f * t) + 0.22 * np.sin(4 * np.pi * f * t) + 0.08 * np.sin(6 * np.pi * f * t)
    x = np.tanh(1.4 * x) / np.tanh(1.4)
    place(buf, x * env, T(f0), gain)


def kick(depth=1.0):
    t = tt(0.9)
    f = 43 + (96 - 43) * np.exp(-t / 0.045)
    body = sine_glide(f) * np.exp(-t / (0.24 * depth))
    click = lp(hp(noise(len(t)), 1200), 4500) * np.exp(-t / 0.004) * 0.10
    return np.tanh(1.6 * body) / np.tanh(1.6) + click


def tick(kind=0, bright=1.0):
    t = tt(0.14)
    freqs = [3150, 4870, 6900, 1820] if kind == 0 else [2380, 3610, 5240, 1390]
    decs = [0.010, 0.006, 0.0035, 0.016]
    amps = [1.0, 0.55, 0.3 * bright, 0.45]
    x = sum(a * np.sin(2 * np.pi * f * t + rng.random() * 6) * np.exp(-t / d)
            for f, d, a in zip(freqs, decs, amps))
    x += hp(noise(len(t)), 2500) * np.exp(-t / 0.0012) * 0.7
    return x * 0.5


def boom(size=1.0):
    t = tt(4.5)
    f = 29 + (80 - 29) * np.exp(-t / 0.22)
    sub = sine_glide(f) * np.exp(-t / (1.3 * size))
    thump = lp(noise(len(t)), 170) * np.exp(-t / 0.11) * 3.0
    mid = bp(noise(len(t)), 250, 1100) * np.exp(-t / 0.045) * 0.5
    air = hp(noise(len(t)), 3500) * np.exp(-t / (0.5 * size)) * 0.05
    return np.tanh(1.2 * (sub + 0.6 * thump + mid)) * 0.9 + air


def whoosh(dur, peak=0.78, f_lo=260, f_hi=2400, pan_from=-0.5, pan_to=0.5, low=0.5):
    n = int(dur * SR)
    u = np.linspace(0, 1, n)
    env = np.where(u < peak, (u / peak) ** 2.6, np.exp(-((u - peak) / (1 - peak)) * 4.5))
    fc = f_lo * (f_hi / f_lo) ** env
    x = sweep_bp(noise(n), fc, 1.1) * 1.6 + lp(noise(n), 320) * low
    x = x * env
    pan = pan_from + (pan_to - pan_from) * u
    return pan2(x, pan)


def riser(dur):
    n = int(dur * SR)
    u = np.linspace(0, 1, n)
    amp = u ** 2.8
    fc = 300 * (8500 / 300) ** (u ** 1.4)
    x = sweep_bp(noise(n), fc, 1.4) * amp
    rate = 3 + 22 * u ** 2
    trem = 0.75 + 0.25 * np.sin(2 * np.pi * np.cumsum(rate) / SR)
    tone = sine_glide(220 * 4 ** (u ** 1.6)) * amp * 0.12
    return (x * trem * 0.9 + tone)


def reverse_cymbal(dur=1.1):
    t = tt(dur)
    x = hp(noise(len(t)), 3800) * np.exp(-t / 0.33) + bp(noise(len(t)), 6000, 14000) * np.exp(-t / 0.2) * 0.6
    return x[::-1] * 0.5


def paper_flick():
    t = tt(0.3)
    snap = bp(noise(len(t)), 1600, 7500) * np.exp(-t / 0.010)
    body = bp(noise(len(t)), 300, 1300) * np.exp(-t / 0.028) * 0.5
    crk = np.zeros(len(t))
    for _ in range(9):
        i = int(rng.uniform(0.004, 0.09) * SR)
        crk[i] += rng.uniform(0.3, 1.0) * rng.choice([-1, 1])
    crk = bp(crk, 2000, 8000) * 3
    return snap + body + crk * np.exp(-t / 0.06)


def paper_press(pitch=1.0):
    t = tt(0.5)
    thump = np.sin(2 * np.pi * 112 * pitch * t) * np.exp(-t / 0.075)
    slap = bp(noise(len(t)), 450 * pitch, 2800 * pitch) * np.exp(-t / 0.022) * 0.85
    crk = np.zeros(len(t))
    for _ in range(6):
        crk[int(rng.uniform(0.002, 0.05) * SR)] += rng.uniform(0.2, 0.7)
    crk = bp(crk, 2500, 9000) * 2.0
    return np.tanh(1.3 * (thump + slap)) + crk


def smooth_swipe(dur=0.6):
    n = int(dur * SR)
    u = np.linspace(0, 1, n)
    env = np.sin(np.pi * u) ** 1.5
    x = bp(noise(n), 900, 4800) * env * 0.5
    crk = np.zeros(n)
    for _ in range(int(40 * dur)):
        crk[int(rng.uniform(0, n - 1))] += rng.uniform(0.1, 0.5)
    x += bp(crk, 2500, 9000) * 1.5 * env
    return pan2(x, -0.25 + 0.5 * u)


def flutter(dur=0.6):
    n = int(dur * SR)
    u = np.linspace(0, 1, n)
    env = u ** 2 * np.clip((1 - u) * 12, 0, 1)
    rate = 20 + 6 * np.sin(2 * np.pi * 3 * u)
    am = 0.55 + 0.45 * np.sin(2 * np.pi * np.cumsum(rate) / SR)
    return bp(noise(n), 280, 1800) * am * env


def tag_tick():
    t = tt(0.06)
    return bp(noise(len(t)), 2500, 7500) * np.exp(-t / 0.003) * 0.5 + \
        np.sin(2 * np.pi * 1900 * t) * np.exp(-t / 0.008) * 0.12


def counter_click(alt=0):
    t = tt(0.05)
    f1, f2 = (2650, 4300) if alt == 0 else (2350, 3900)
    return (np.sin(2 * np.pi * f1 * t) * np.exp(-t / 0.004) + 0.5 * np.sin(2 * np.pi * f2 * t) * np.exp(-t / 0.0025)
            + hp(noise(len(t)), 3000) * np.exp(-t / 0.0008)) * 0.4


def pen_scratch(dur, speed):
    n = int(dur * SR)
    gr = np.abs(lp(noise(n), 70))
    gr /= gr.max() + 1e-9
    return bp(noise(n), 2400, 7500) * (0.3 + gr) * speed[:n] * 0.35


def line_tone(dur, f0, f1, env):
    n = int(dur * SR)
    u = np.linspace(0, 1, n)
    f = f0 * (f1 / f0) ** u
    x = sine_glide(f) + 0.3 * sine_glide(f * 2.003) + 0.12 * sine_glide(f * 3.0)
    return x * env[:n]


def plip():
    t = tt(0.35)
    f = 420 + (1150 - 420) * np.exp(-t / 0.018)
    a = sine_glide(f) * np.exp(-t / 0.06)
    t2 = np.clip(t - 0.07, 0, None)
    f2 = 360 + (760 - 360) * np.exp(-t2 / 0.015)
    b = sine_glide(f2) * np.exp(-t2 / 0.045) * (t >= 0.07) * 0.35
    return (a + b) * 0.6


def metal_shimmer(base=640):
    t = tt(2.6)
    out = np.zeros((2, len(t)))
    for ch, det in ((0, 1.0), (1, 1.004)):
        for r, d, a in zip([1, 2.76, 5.40, 8.93, 13.34], [1.6, 1.1, 0.7, 0.45, 0.3], [1, .6, .4, .25, .15]):
            out[ch] += a * np.sin(2 * np.pi * base * r * det * t + rng.random() * 6) * np.exp(-t / d)
    brush = bp(noise(len(t)), 3000, 9000) * np.exp(-t / 0.08) * 0.6
    return (out + brush[None, :]) * 0.22


def light_swell(dur):
    t = tt(dur)
    u = t / dur
    amp = u ** 3
    x = np.zeros((2, len(t)))
    for i, m in enumerate([86, 93, 98, 100]):  # D6 A6 D7 E7
        for ch in range(2):
            x[ch] += np.sin(2 * np.pi * mtof(m) * (1 + 0.002 * (ch - 0.5) * (i + 1)) * t + rng.random() * 6)
    x *= (0.8 + 0.2 * np.sin(2 * np.pi * 6 * t))[None, :] * 0.08
    air = hp(noise(len(t)), 5000) * 0.35
    return (x + air[None, :]) * amp[None, :]


def bells(notes, dur=6.0):
    t = tt(dur)
    out = np.zeros((2, len(t)))
    for i, m in enumerate(notes):
        f = mtof(m)
        pan = -0.5 + i / max(1, len(notes) - 1)
        x = sum(a * np.sin(2 * np.pi * f * r * t + rng.random() * 6) * np.exp(-t / d)
                for r, d, a in zip([1, 2.0, 2.99, 4.17, 5.43], [3.2, 2.0, 1.1, 0.7, 0.45], [1, .4, .22, .12, .08]))
        x *= np.clip(t / 0.004, 0, 1)
        out += pan2(x, pan)
    return out / len(notes) * 0.5


def room_tone(n):
    b = np.cumsum(noise(n))
    b = hp(b, 25)
    b = lp(b, 220)
    b /= np.abs(b).max() + 1e-9
    air = hp(noise(n), 3000) * 0.02
    return b * 0.6 + air

# ------------------------------------------------------------------ reverb ---


def make_ir(rt=(3.0, 2.4, 1.3), dur=3.6, pre=0.02, seed=5):
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    t = np.arange(n) / SR
    ir = np.zeros((2, n))
    for ch in range(2):
        w = r.standard_normal(n)
        bands = [lp(w, 300), bp(w, 300, 3000), hp(w, 3000)]
        for b, r60 in zip(bands, rt):
            ir[ch] += b * np.exp(-6.91 * t / r60)
    ir *= np.clip(t / 0.03, 0, 1)
    ir = np.concatenate([np.zeros((2, int(pre * SR))), ir], axis=1)
    return ir / np.sqrt((ir ** 2).sum(axis=1, keepdims=True))


def reverb(x, ir):
    mono = x.mean(axis=0)
    wet = np.stack([fftconvolve(mono, ir[0])[:x.shape[1]], fftconvolve(mono, ir[1])[:x.shape[1]]])
    return wet


# ------------------------------------------------------------------- score ---

DM9 = [50, 53, 57, 60, 64]
BBMAJ9 = [46, 53, 57, 62, 64]
GM9 = [43, 50, 53, 57, 58]
A7SUS = [45, 52, 55, 57, 62]
FMAJ9 = [41, 48, 57, 64, 67]
DMADD9 = [50, 57, 62, 64, 69]


def compose():
    mus = np.zeros((2, N))    # music (dry)
    mus_send = np.zeros((2, N))
    sfx = np.zeros((2, N))
    sfx_send = np.zeros((2, N))
    room_send = np.zeros((2, N))
    duck = np.ones(N)

    def duck_at(f, depth=0.45, rel=0.35):
        i0 = f * SPF
        t = np.arange(N - i0) / SR
        duck[i0:] *= 1 - depth * np.exp(-t / rel)

    # ---- ACT 1 — hook
    t = tt(0.75)
    swell = np.sin(2 * np.pi * 36.7 * t) * (t / 0.6) ** 2 * (t < 0.62)
    place(mus, swell, 0, 0.35)
    env = np.concatenate([np.linspace(0.15, 1, int(0.45 * SR)), np.linspace(1, 0, int(0.3 * SR))])
    place(sfx, line_tone(0.75, 1250, 1690, env), 0, 0.10)
    place(sfx_send, line_tone(0.75, 1250, 1690, env), 0, 0.10)
    place(sfx, boom(0.9), T(18), 0.55)
    place(sfx_send, boom(0.9), T(18), 0.25)
    pad_chord(mus, [38, 45, 50, 52, 57], 18, 72, gain=0.22, att=1.0, rel=0.5, bright=(0.05, 0.4), seed=2, hpf=60)
    place(sfx, light_swell(T(16)), T(56), 0.9)
    place(sfx_send, light_swell(T(16)), T(56), 0.6)

    # ---- ACT 2 — the craft: pulse, ticking time, four chords
    for i, (ch, f0, f1, bn) in enumerate([(DM9, 72, 144, 38), (BBMAJ9, 144, 216, 34),
                                          (GM9, 216, 288, 31), (A7SUS, 288, 351, 33)]):
        last = i == 3
        pad_chord(mus, ch, f0, f1, gain=0.085 + 0.012 * i, att=0.5, rel=0.18 if last else 1.0,
                  bright=(0.2, 0.55 if last else 0.32), seed=10 + i)
        bass(mus, bn, f0, f1, gain=0.15, rel=0.08 if last else 0.4)
    for f in range(72, 340, BEAT):
        place(mus, kick(1.0), T(f), 0.29)
        duck_at(f, 0.2, 0.18)
    for j, f in enumerate(range(72, 340, 9)):
        k = tick(j % 2)
        g = 0.038 if j % 2 else 0.05
        place(mus, k, T(f), g, pan=0.35 if j % 2 else -0.2)
        place(mus_send, k, T(f), g * 0.5)
    # transitions & details
    for f in (82, 125, 162, 197):
        place(sfx, tag_tick(), T(f), 0.22, pan=-0.4)
    w = whoosh(0.42, 0.88, 1800, 300, 0.1, -0.1, low=0.8)
    place(sfx, w, T(117) - 0.42 * 0.88, 0.32)
    place(sfx, plip(), T(119), 0.42, pan=0.05)
    place(sfx_send, plip(), T(119), 0.35)
    place(sfx, whoosh(0.45, 0.5, 2500, 5200, -0.1, 0.25, low=0.0), T(120), 0.10)
    w = whoosh(0.38, 0.86, 300, 2600, -0.7, 0.7)
    place(sfx, w, T(153) - 0.38 * 0.86, 0.36)
    place(sfx_send, w, T(153) - 0.38 * 0.86, 0.12)
    place(sfx, lp(noise(int(0.2 * SR)), 200) * np.exp(-tt(0.2) / 0.05), T(155), 0.5)
    place(sfx, paper_flick(), T(189), 0.42, pan=0.1)
    place(sfx_send, paper_flick(), T(189), 0.15)
    w = whoosh(0.42, 0.85, 400, 2900, 0.6, -0.6)
    w *= (0.7 + 0.3 * np.sin(2 * np.pi * 28 * np.arange(w.shape[1]) / SR))[None, :]
    place(sfx, w, T(225) - 0.42 * 0.85, 0.34)
    place(sfx, metal_shimmer(), T(226), 0.55)
    place(sfx_send, metal_shimmer(), T(226), 0.35)
    w = whoosh(0.4, 0.92, 220, 3800, 0.0, 0.0, low=0.9)
    place(sfx, w, T(261) - 0.4 * 0.92, 0.36)
    place(sfx, lp(noise(int(0.4 * SR)), 140) * np.exp(-tt(0.4) / 0.09), T(261), 0.9)
    place(sfx, light_swell(T(16)), T(281), 0.8)
    place(sfx_send, light_swell(T(16)), T(281), 0.5)

    # ---- format card: pen, counters, the window opens
    sp = np.clip(np.sin(np.linspace(0, np.pi, int(T(20) * SR))), 0, 1)
    place(sfx, pen_scratch(T(20), sp), T(300), 0.35, pan=-0.1)
    last = -1
    for f10 in range(int(309 * 10), int(331 * 10)):
        f = f10 / 10.0
        u = min(1.0, (f - 309) / 22.0)
        v = int(21 * (1 - 2 ** (-10 * u)))
        if v != last:
            place(sfx, counter_click(v % 2), T(f), 0.30, pan=0.15 if v % 2 else -0.15)
            last = v
    place(sfx, tag_tick(), T(322), 0.18)
    w = whoosh(0.75, 0.93, 180, 1500, 0, 0, low=1.0)
    place(sfx, w, T(351) - 0.75 * 0.93, 0.42)
    place(sfx_send, w, T(351) - 0.75 * 0.93, 0.15)

    # ---- ACT 3 — the blank wall: strategic silence, a clock in an empty room
    rt = room_tone(N)
    rt_env = np.zeros(N)
    i0, i1 = 351 * SPF, 432 * SPF
    rt_env[i0:] = 1.0
    rt_env[i0:i0 + 3000] = np.linspace(0, 1, 3000)
    rt_env[i1:] = 0.45
    sfx += pan2(rt * rt_env * 0.025, 0)
    t = tt(T(81) + 0.5)
    drone = (np.sin(2 * np.pi * 36.7 * t) + 0.3 * np.sin(2 * np.pi * 73.4 * t)) * np.clip(t / 1.2, 0, 1)
    drone *= np.where(t < T(81), 1, np.exp(-(t - T(81)) / 0.15))
    place(mus, drone, T(351), 0.035)
    for j, f in enumerate(range(354, 430, BEAT)):
        place(sfx, tick(j % 2, 0.8), T(f), 0.11, pan=0.45)
        place(room_send, tick(j % 2, 0.8), T(f), 0.18)
    for f in (360, 363, 366, 378, 382, 441, 445):
        place(sfx, tag_tick(), T(f), 0.07)
    w = whoosh(0.62, 0.95, 160, 900, 0, 0, low=1.0)
    place(sfx, w, T(414) - 0.62 * 0.95, 0.28)
    place(sfx, flutter(T(16)), T(415), 0.30, pan=0.3)
    place(sfx, paper_press(1.25), T(426), 0.12, pan=0.2)
    place(sfx, paper_press(1.0), T(432), 0.62)
    place(room_send, paper_press(1.0), T(432), 0.35)
    place(sfx, boom(0.7), T(432), 0.30)
    duck_at(432, 0.5, 0.3)
    place(sfx, smooth_swipe(0.6), T(434), 0.30)
    for nme, fl in LAND.items():
        if nme == "gt3black":
            continue
        place(sfx, flutter(T(8)), T(fl - 8), 0.18, pan=float(rng.uniform(-0.5, 0.5)))
        p = paper_press(float(rng.uniform(0.9, 1.25)))
        place(sfx, p, T(fl), 0.38, pan=float(rng.uniform(-0.45, 0.45)))
        place(room_send, p, T(fl), 0.18)

    # ---- the build: music returns on the press
    for i, (ch, f0, f1, bn) in enumerate([(DM9, 432, 504, 38), (BBMAJ9, 504, 540, 34),
                                          (GM9, 540, 576, 31), (A7SUS, 576, 588, 33)]):
        pad_chord(mus, ch, f0, f1, gain=0.11 + 0.045 * i, att=0.25, rel=0.06 if i == 3 else 0.6,
                  bright=(0.25 + 0.12 * i, 0.4 + 0.15 * i), seed=20 + i)
        pad_chord(mus, [m + 12 for m in ch[2:]], f0, f1, gain=0.035 + 0.03 * i, att=0.4,
                  rel=0.06 if i == 3 else 0.6, bright=(0.4, 0.7), seed=40 + i, hpf=300)
        bass(mus, bn, f0, f1, gain=0.20 + 0.02 * i, rel=0.05 if i == 3 else 0.3)
    for f in list(range(450, 540, BEAT)) + list(range(540, 588, 9)):
        place(mus, kick(1.0 if f < 540 else 0.7), T(f), 0.36 + 0.06 * (f - 450) / 138)
        duck_at(f, 0.25, 0.15)
    step = 9
    f = 432
    j = 0
    while f < 586:
        k = tick(j % 2)
        place(mus, k, T(f), 0.06, pan=0.3 if j % 2 else -0.3)
        place(mus_send, k, T(f), 0.03)
        f += step if f < 540 else 4.5
        j += 1
    # 16th-note ostinato (pluck) with ping-pong echo
    chords = [(DM9, 468, 504), (BBMAJ9, 504, 540), (GM9, 540, 576), (A7SUS, 576, 588)]
    pat = [0, 2, 4, 2, 1, 3, 4, 3]
    arp = np.zeros((2, N))
    for ch, f0, f1 in chords:
        tones = sorted(ch)[1:] + [ch[2] + 12]
        k = 0
        f = f0
        while f < f1:
            m = tones[pat[k % 8] % len(tones)] + 12
            d = 0.32
            tn = tt(d)
            x = saw(mtof(m), len(tn)) + 0.5 * saw(mtof(m) * 1.005, len(tn))
            e = np.exp(-tn / 0.11)
            br = np.exp(-tn / 0.035)
            x = lp(x, 900) * (1 - br) + lp(x, 5000) * br
            place(arp, x * e, T(f), 0.06, pan=-0.3 if k % 2 else 0.3)
            f += 4.5
            k += 1
    dl = int(0.45 * SR)
    echo = np.zeros_like(arp)
    echo[0, dl:] = arp[1, :-dl] * 0.45
    echo[1, 2 * dl:] = arp[0, :-2 * dl] * 0.3
    mus += arp + lp(echo, 3500)
    mus_send += (arp + echo) * 0.5
    place(sfx, whoosh(3.0, 0.6, 90, 500, -0.2, 0.2, low=1.2), T(468), 0.18)
    place(sfx, riser(T(588 - 504)), T(504), 0.30)
    place(sfx_send, riser(T(588 - 504)), T(504), 0.2)
    place(sfx, reverse_cymbal(T(588 - 566)), T(566), 0.55)

    # ---- the reveal (b33): everything lands at once
    place(sfx, boom(1.3), T(594), 0.80)
    place(sfx_send, boom(1.3), T(594), 0.45)
    duck_at(594, 0.35, 0.5)
    pad_chord(mus, FMAJ9, 594, 650, gain=0.27, att=0.01, rel=1.3, bright=(0.85, 0.45), seed=60)
    pad_chord(mus, [53, 60, 65, 69, 72, 76], 594, 650, gain=0.10, att=0.01, rel=1.6, bright=(0.9, 0.5), seed=61,
              hpf=400)
    bass(mus, 29, 594, 650, gain=0.26, rel=0.8)
    lo = supersaw(29, 2.6, seed=62) + supersaw(41, 2.6, seed=63)
    lo = lp(lo, 480) * np.exp(-tt(2.6) / 0.9)[None, :]
    place(mus, lo, T(594), 0.16)
    place(mus, kick(1.2), T(630), 0.45)
    place(sfx, light_swell(1.6) * 0.6, T(600), 0.6)
    w = whoosh(0.75, 0.82, 140, 2000, -0.75, 0.75, low=1.3)
    place(sfx, w, T(664) - 0.75 * 0.82, 0.5)
    place(sfx_send, w, T(664) - 0.75 * 0.82, 0.18)
    place(sfx, lp(noise(int(0.5 * SR)), 120) * np.exp(-tt(0.5) / 0.12), T(666), 0.8)

    # ---- ACT 4 — the brand
    env = np.clip(np.sin(np.linspace(0, np.pi, int(T(30) * SR))), 0, 1) ** 2
    place(sfx, line_tone(T(30), 1250, 1500, env), T(672), 0.045)
    place(sfx_send, line_tone(T(30), 1250, 1500, env), T(672), 0.06)
    env2 = np.clip(np.sin(np.linspace(0, np.pi, int(T(24) * SR))), 0, 1) ** 2
    place(sfx, line_tone(T(24), 840, 940, env2), T(684), 0.04, pan=0.4)
    place(sfx, boom(0.8), T(702), 0.5)
    place(sfx_send, boom(0.8), T(702), 0.3)
    b = bells([62, 69, 76, 81], 7.0)
    place(mus, b, T(702), 0.40)
    place(mus_send, b, T(702), 0.4)
    pad_chord(mus, DMADD9, 702, 800, gain=0.08, att=0.6, rel=1.4, bright=(0.3, 0.12), seed=70)
    bass(mus, 26, 702, 790, gain=0.14, rel=1.0)
    place(sfx, light_swell(T(18)) * 0.5, T(738), 0.6)
    tk = tick(0, 1.0)
    place(sfx, tk, T(762), 0.30)
    place(sfx_send, tk, T(762), 0.22)
    place(room_send, tk, T(762), 0.3)

    return mus * duck[None, :], mus_send * duck[None, :], sfx, sfx_send, room_send

# --------------------------------------------------------------- mastering ---


def lufs(x):
    """Integrated loudness (ITU-R BS.1770-4) at 48 kHz."""
    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]
    from scipy.signal import lfilter
    y = lfilter(b2, a2, lfilter(b1, a1, x, axis=-1), axis=-1)
    blk, hop = int(0.4 * SR), int(0.1 * SR)
    ms = np.array([(y[:, i:i + blk] ** 2).mean(axis=1).sum() for i in range(0, y.shape[1] - blk, hop)])
    L = -0.691 + 10 * np.log10(ms + 1e-12)
    g = L > -70
    rel = -0.691 + 10 * np.log10(ms[g].mean()) - 10
    g2 = L > rel
    return -0.691 + 10 * np.log10(ms[g & g2].mean())


def limiter_gain(x, ceiling_db=-1.2, look=0.003, rel=0.08):
    """Gain curve keeping 4x-oversampled (true) peaks under the ceiling."""
    up = resample_poly(x, 4, 1, axis=-1)
    pk = np.abs(up).max(axis=0).reshape(-1, 4).max(axis=1)[:x.shape[1]]
    pk = np.pad(pk, (0, x.shape[1] - len(pk)))
    c = 10 ** (ceiling_db / 20)
    need = np.minimum(1.0, c / np.maximum(pk, 1e-9))
    la = int(look * SR)
    from scipy.ndimage import minimum_filter1d
    need = minimum_filter1d(need, size=2 * la + 1, origin=0)
    g = np.empty_like(need)
    a = np.exp(-1 / (rel * SR))
    cur = 1.0
    for i in range(len(need)):   # release smoothing (attack handled by look-ahead min)
        cur = need[i] if need[i] < cur else a * cur + (1 - a) * need[i]
        g[i] = cur
    k = np.hanning(2 * la + 1)
    k /= k.sum()
    gp = np.pad(g, (la, la), mode="edge")
    return np.convolve(gp, k, mode="valid")


def write_wav(path, x):
    tmp = path + ".f32"
    x.T.astype("<f4").tofile(tmp)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", tmp,
                    "-c:a", "pcm_s24le", path], check=True)
    os.remove(tmp)


def build(target_lufs=-14.0):
    os.makedirs(OUT, exist_ok=True)
    mus, mus_send, sfx, sfx_send, room_send = compose()
    hall = make_ir()
    room = make_ir(rt=(0.9, 0.7, 0.4), dur=1.2, pre=0.008, seed=9)
    music = mus + 0.32 * reverb(mus_send + 0.25 * mus, hall)
    effects = sfx + 0.30 * reverb(sfx_send, hall) + 0.35 * reverb(room_send, room)
    music, effects = hp(music, 30), hp(effects, 30)
    music = music - 0.22 * lp(music, 85)   # keep the low end firm, not boomy
    effects = effects - 0.18 * lp(effects, 70)
    # gentle tilt: tame harsh highs on the effects bus
    effects = effects - 0.25 * hp(effects, 9000)
    # fade the final tail into the cut
    fade = np.ones(N)
    i0 = int(27.5 * SR)
    fade[i0:] = np.linspace(1, 0, N - i0) ** 1.5
    music *= fade
    effects *= fade
    mix = music + effects
    gain = 10 ** ((target_lufs - lufs(mix)) / 20)
    for _ in range(3):
        g = limiter_gain(mix * gain)
        out = mix * gain * g[None, :]
        gain *= 10 ** ((target_lufs - lufs(out)) / 20)
    g = limiter_gain(mix * gain)
    music_o, effects_o = music * gain * g[None, :], effects * gain * g[None, :]
    mix_o = music_o + effects_o
    write_wav(os.path.join(OUT, "MOTIF297_Mix_Stereo_48k24.wav"), mix_o)
    write_wav(os.path.join(OUT, "MOTIF297_Stem_Music_48k24.wav"), music_o)
    write_wav(os.path.join(OUT, "MOTIF297_Stem_SFX_48k24.wav"), effects_o)
    up = resample_poly(mix_o, 4, 1, axis=-1)
    print(f"integrated {lufs(mix_o):.2f} LUFS | sample peak {20*np.log10(np.abs(mix_o).max()):.2f} dBFS | "
          f"true peak ~{20*np.log10(np.abs(up).max()):.2f} dBTP | max limiter GR {20*np.log10(g.min()):.2f} dB")
    return mix_o


if __name__ == "__main__":
    build()
