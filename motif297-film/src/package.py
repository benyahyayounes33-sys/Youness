"""Package deliverables: mux audio, write SRT + timeline, render thumbnail."""
import json
import os
import shutil
import subprocess
import sys

import cv2
import numpy as np

import film
from engine import W, H, OBSIDIAN, PAPER, RUST, Cam, FOCAL, grade, finish, draw_text, text_width, font

OUT = film.OUT
AUD = os.path.join(OUT, "audio")
MIX = os.path.join(AUD, "MOTIF297_Mix_Stereo_48k24.wav")


def tc(f, fps=30):
    s, fr = divmod(int(f), fps)
    return f"00:{s // 60:02d}:{s % 60:02d}:{fr:02d}"


def srt_time(f):
    ms = int(round(f / 30 * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def mux():
    tmp = os.path.join(OUT, "_tmp")
    names = {"master": "MOTIF297_BrandFilm_9x16_Master.mp4",
             "clean": "MOTIF297_BrandFilm_9x16_Clean_NoText.mp4",
             "captions": "MOTIF297_BrandFilm_9x16_Captions.mp4"}
    for k, name in names.items():
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(tmp, f"{k}_video.mp4"), "-i", MIX,
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
                        "-shortest", "-movflags", "+faststart", os.path.join(OUT, name)], check=True)
    print("muxed", list(names.values()))


def write_srt():
    lines = []
    for i, (f0, f1, txt) in enumerate(film.CAPTIONS, 1):
        lines += [str(i), f"{srt_time(f0)} --> {srt_time(f1)}", txt, ""]
    with open(os.path.join(OUT, "MOTIF297_BrandFilm_Captions_SDH.srt"), "w") as fh:
        fh.write("\n".join(lines))


SHOTS = [
    dict(n=1, act="1 HOOK", f_in=0, f_out=72, source="porsche_gt3rs_black.jpg",
         picture="Black frame. A Signal Rust hairline draws out from the centre (tips glowing), widens and "
                 "graphic-matches into the GT3 RS taillight as the car lights up around it. Slow macro orbit, "
                 "focus falls off across the body.",
         transition_out="Light transition: the taillight glow blooms to warm white (exposure ramp + bloom).",
         sound="Sub swell + glass line tone that follows the draw; first hit on frame 18; dark Dm drone; "
               "air swell into the white."),
    dict(n=2, act="2 CRAFT", f_in=72, f_out=117, source="clock_dont_waste_time.jpg",
         picture="White resolves into the melting clock. Camera tilts down the ink drip; focus plane runs along the "
                 "drip, the type falls soft. Tag: ART.",
         transition_out="Motion-matched tilt: accelerates down (motion blur) into the next shot.",
         sound="Pulse enters at 100 BPM, clock ticks on 8ths (tick/tock); downward whoosh; ink 'plip' on the cut."),
    dict(n=3, act="2 CRAFT", f_in=117, f_out=153, source="toyota_supra_mk5.jpg",
         picture="Downward move lands on the brush-lettering ink drips. Tag: AUTOMOTIVE.",
         transition_out="Whip-pan right (motion blur).",
         sound="Brush swish; whoosh L->R on the whip."),
    dict(n=4, act="2 CRAFT", f_in=153, f_out=189, source="cr7.jpg",
         picture="Whip lands on the CR letterforms; the figure below is thrown out of focus. Tag: SPORT.",
         transition_out="Graphic match cut, type to type, on the beat.",
         sound="Low landing thud; paper flick on the cut."),
    dict(n=5, act="2 CRAFT", f_in=189, f_out=225, source="peaky_blinders.jpg",
         picture="Slow track across the editorial title type. Tag: CINEMA. Camera rolls into a spin.",
         transition_out="Spin (roll) transition, continued in the next shot.",
         sound="Rotational whoosh with flutter."),
    dict(n=6, act="2 CRAFT", f_in=225, f_out=261, source="porsche_911gt3_blue.jpg",
         picture="The spin resolves on the wheel; push through the hub.",
         transition_out="Zoom-through (radial motion blur).",
         sound="Metallic shimmer (inharmonic partials); rising whoosh + air thump."),
    dict(n=7, act="2 CRAFT", f_in=261, f_out=297, source="porsche_gt3rs_blue_rear.jpg",
         picture="Push lands on the rear three-quarter and its reflection.",
         transition_out="Light transition to Warm Paper.",
         sound="Air swell into white."),
    dict(n=8, act="2 CRAFT", f_in=297, f_out=351, source="(graphic)",
         picture="Warm Paper. An A4 outline draws itself; rust dimension lines extend while counters roll to 210 and "
                 "297 mm. 'A4 ADHESIVE ART POSTERS'. The A4 frame becomes a window onto the wall.",
         transition_out="Masking transition + zoom-through the A4 window.",
         sound="Pen scratch; mechanical counter clicks (decelerating); deep whoosh. Music cuts at the window."),
    dict(n=9, act="3 TRANSFORMATION", f_in=351, f_out=414, source="(virtual wall)",
         picture="A blank wall in window light. 'A BLANK WALL / SAYS NOTHING.' Camera begins to push in.",
         transition_out="Continuous push-in.",
         sound="Strategic silence: room tone and a single clock ticking in the space."),
    dict(n=10, act="3 TRANSFORMATION", f_in=414, f_out=468, source="porsche_gt3rs_black.jpg",
         picture="The GT3 RS poster arrives top-edge first and is pressed flat (shadow tightens to contact). "
                 "'SAY SOMETHING.'",
         transition_out="Continuous pull-back.",
         sound="Paper flutter; top-edge tap; PRESS on the beat (music returns); smoothing swipe."),
    dict(n=11, act="3 TRANSFORMATION", f_in=468, f_out=594, source="all seven posters",
         picture="Pull back as six more posters land on the beat (accelerating), forming a 2-3-2 gallery wall; "
                 "window light drifts across.",
         transition_out="Hard cut on the musical hit after a 6-frame silence.",
         sound="Each poster: flutter + press; 16th ostinato, strings crescendo, riser, accelerating ticks, "
               "reverse cymbal, 0.2 s gap."),
    dict(n=12, act="4 BRAND", f_in=594, f_out=666, source="all seven posters",
         picture="HERO: perspective dolly along the finished wall, shallow focus, sun moving. A dark foreground "
                 "pillar passes the lens.",
         transition_out="Foreground object wipe to Obsidian.",
         sound="Reveal hit: sub boom + Fmaj9 stab; deep L->R whoosh into the wipe."),
    dict(n=13, act="4 BRAND", f_in=666, f_out=846, source="(graphic)",
         picture="Obsidian. A4 outline draws; rust 297 mm dimension line; MOTIF / 297 rises letter by letter; "
                 "'WALLS WITH A POINT OF VIEW' + the rust full stop. Slow ambient push.",
         transition_out="End (holds for loop).",
         sound="Line tone (callback to the hook); logo hit + Dm(add9) bells; final single clock tick on the "
               "full stop; music resolves."),
]

TEXT = [
    (82, 113, "Tag: ART (placeholder theme — replace with real collection name)"),
    (125, 151, "Tag: AUTOMOTIVE (placeholder)"),
    (162, 190, "Tag: SPORT (placeholder)"),
    (197, 221, "Tag: CINEMA (placeholder)"),
    (309, 345, "210 / 297 MM counters"),
    (322, 345, "A4 ADHESIVE ART POSTERS"),
    (360, 409, "A BLANK WALL / SAYS NOTHING."),
    (441, 473, "SAY SOMETHING."),
    (702, 846, "MOTIF / 297 (typographic wordmark — placeholder until the official logo file is supplied)"),
    (712, 846, "297 MM (dimension label)"),
    (738, 846, "WALLS WITH A POINT OF VIEW."),
]


def write_timeline():
    d = os.path.join(OUT, "timeline")
    os.makedirs(d, exist_ok=True)
    data = dict(
        title="MOTIF 297 — Walls With a Point of View", fps=30, resolution=[W, H], duration_frames=film.TOTAL,
        duration_seconds=film.TOTAL / 30, tempo_bpm=100, frames_per_beat=18,
        shots=[dict(s, tc_in=tc(s["f_in"]), tc_out=tc(s["f_out"]), seconds=round((s["f_out"] - s["f_in"]) / 30, 2))
               for s in SHOTS],
        on_screen_text=[dict(f_in=a, f_out=b, tc_in=tc(a), tc_out=tc(b), text=t) for a, b, t in TEXT],
        captions_sdh=[dict(f_in=a, f_out=b, text=t) for a, b, t in film.CAPTIONS],
        poster_landing_frames=film.LAND,
        project="Procedural project: src/film.py (picture), src/audio.py (score + SFX), src/engine.py. "
                "Re-render with `python3 src/film.py && python3 src/audio.py && python3 src/package.py`.",
    )
    with open(os.path.join(d, "MOTIF297_timeline.json"), "w") as fh:
        json.dump(data, fh, indent=2)
    md = ["# MOTIF 297 — Edit Decision List / Cue Sheet", "",
          "30 fps · 1080×1920 · 100 BPM (1 beat = 18 frames) · 28.2 s", "",
          "| # | Act | TC in | TC out | Dur | Source | Picture | Transition out | Sound |",
          "|---|---|---|---|---|---|---|---|---|"]
    for s in SHOTS:
        md.append(f"| {s['n']} | {s['act']} | {tc(s['f_in'])} | {tc(s['f_out'])} | {(s['f_out'] - s['f_in']) / 30:.2f}s "
                  f"| {s['source']} | {s['picture']} | {s['transition_out']} | {s['sound']} |")
    md += ["", "## On-screen text", "", "| TC in | TC out | Text |", "|---|---|---|"]
    md += [f"| {tc(a)} | {tc(b)} | {t} |" for a, b, t in TEXT]
    md += ["", "## Poster landing frames (each lands on the beat grid)", ""]
    md += [f"- {k}: frame {v} ({tc(v)})" for k, v in film.LAND.items()]
    with open(os.path.join(d, "MOTIF297_cue_sheet.md"), "w") as fh:
        fh.write("\n".join(md) + "\n")


def thumbnail():
    """Cover frame: the finished wall + wordmark, key content inside the 3:4 grid-safe area."""
    film.init()
    cam = Cam((0.0, -11.0), FOCAL / 10.4)
    img = grade(film.render_wall(cam, 700, list(film.LAYOUT), -20.0))
    size, track = 92, 0.14
    tw = text_width("MOTIF 297", size, 500, track)
    draw_text(img, "MOTIF 297", size, 500, track, OBSIDIAN, 540, 330, anchor="center")
    words = "WALLS WITH A POINT OF VIEW"
    s2 = 30
    w2 = text_width(words, s2, 500, 0.26)
    dot = text_width(".", s2, 700, 0)
    x = 540 - (w2 + dot + 4) / 2
    draw_text(img, words, s2, 500, 0.26, OBSIDIAN, x, 418)
    draw_text(img, ".", s2, 700, 0, RUST, x + w2 + 4, 418)
    out = finish(img, 7)
    cv2.imwrite(os.path.join(OUT, "MOTIF297_Thumbnail_1080x1920.jpg"), cv2.cvtColor(out, cv2.COLOR_RGB2BGR),
                [cv2.IMWRITE_JPEG_QUALITY, 95])
    crop = out[240:1680]
    cv2.imwrite(os.path.join(OUT, "MOTIF297_Thumbnail_GridCrop_1080x1440.jpg"), cv2.cvtColor(crop, cv2.COLOR_RGB2BGR),
                [cv2.IMWRITE_JPEG_QUALITY, 95])


if __name__ == "__main__":
    steps = sys.argv[1:] or ["srt", "timeline", "thumb", "mux"]
    if "srt" in steps:
        write_srt()
    if "timeline" in steps:
        write_timeline()
    if "thumb" in steps:
        thumbnail()
    if "mux" in steps:
        mux()
