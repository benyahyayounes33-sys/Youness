# MOTIF 297 — "Walls With a Point of View"

**Format:** 9:16 · 1080 × 1920 · 30 fps · 28.2 s · H.264 · stereo AAC 320 kb/s (48 kHz)
**Score:** original, synthesised from scratch for this film (no samples, no library music): rights-free.

---

## 1. The idea

**297 is the height of an A4 sheet in millimetres.** The brand name is a measurement.
The film builds its whole visual language on that fact: hairlines, crop marks, dimension
lines and an A4 outline are the "logo system" that carries the brand from the first frame
to the last.

The story turns on one contrast:

> A BLANK WALL SAYS NOTHING. → SAY SOMETHING. → MOTIF 297 — WALLS WITH A POINT OF VIEW.

A poster is shown as a choice that says who you are, not as decoration.

The second motif is **time**, taken from the melting-clock design ("Don't waste time"). A clock
tick is the film's rhythm instrument. It is the only sound left in the silence, it speeds up in
the build, and a single tick lands the final full stop.

---

## 2. Structure (100 BPM — every cut sits on an 18-frame beat grid)

| Act | Time | What happens | Feeling |
|---|---|---|---|
| **1 · Hook** | 0.0–2.4 s | A Signal Rust hairline draws across black, then turns into the GT3 RS taillight as the car lights up around it. | Curiosity: "what is that line?" |
| **2 · Craft** | 2.4–11.7 s | Six macro passages through the designs (ink drip → brush drips → letterforms → editorial type → wheel → bodywork), each linked by a motivated transition. Then the format: an A4 outline, dimension lines counting to **210 × 297 mm**. | Visual attraction, texture, detail |
| **3 · Transformation** | 11.7–19.8 s | The A4 frame becomes a window onto a blank wall. The music stops. "A BLANK WALL / SAYS NOTHING." One poster is pressed onto the wall on the beat and the music returns ("SAY SOMETHING."). Six more land on accelerating beats as the camera pulls back. | Tension, then desire |
| **4 · Brand** | 19.8–28.2 s | After a 0.2 s silence: the reveal, a perspective dolly along the finished wall. A foreground pillar wipes to Obsidian. A4 outline → **MOTIF / 297** → *WALLS WITH A POINT OF VIEW* + the rust full stop. | Emotional payoff, brand recognition |

The full shot-by-shot list with timecodes, transitions and sound cues is in `deliverables/timeline/MOTIF297_cue_sheet.md`.

---

## 3. Transitions — each one has a reason

| Cut | Technique | Motivation |
|---|---|---|
| Line → taillight | **Graphic match** | The brand's hairline *becomes* the product's light line. |
| Taillight → clock | **Light transition** (bloom to white) | The glow turns into the white of the next print. |
| Clock → Supra | **Motion-matched tilt** with motion blur | Following ink downward: drip to drip. |
| Supra → CR | **Whip pan** | Energy shift from ink to bold geometry. |
| CR → Peaky Blinders | **Graphic match cut** on the beat | Type to type: white letterforms to black. |
| Peaky → wheel | **Spin / roll** continued across the cut | The roll resolves on a wheel. |
| Wheel → GT3 rear | **Zoom-through** the hub | Push through the dark centre. |
| GT3 rear → A4 card | **Light transition** to Warm Paper | From the image to the paper it lives on. |
| A4 card → wall | **Mask transition + push-in** | The A4 frame literally frames the wall: the format becomes the place. |
| Build → reveal | **Hard cut on the hit** after 6 frames of silence | The one cut in the film that should be felt. |
| Hero → end card | **Foreground object wipe** | A dark pillar passes the lens during the dolly; its darkness *is* the end card. |

Motion blur is real sub-frame sampling (180° shutter, up to 14 samples), never a blur effect laid on top.

---

## 4. Cinematography (virtual camera)

- Every poster is treated as a **physical plane in 3D**, filmed through a pinhole camera that can tilt, orbit and roll.
- **Depth of field is physically derived** from the plane's per-pixel depth (thin-lens circle of confusion). When a shot looks like a macro lens on a tilted print, the focus falloff matches the perspective.
- The wall is a 3D scene. Each poster is placed **top edge first, then pressed flat**, the way adhesive posters are applied. Its shadow is cast along the window-light direction and tightens to a contact shadow as it meets the wall. All prints sit in the same window light as the wall.
- Fine film grain, a soft vignette and a highlight roll-off protect paper whites.

---

## 5. Motion design & typography

- **Typeface:** Jost (geometric, Futura-lineage, open licence OFL). Tracked caps for supers, light/medium weights only.
- **Colour:** Obsidian `#171717` and Warm Paper `#F4F0E8` carry everything. **Signal Rust `#B64A3A` appears only where it means something:** the opening line, the dimension lines, the tag index squares and the final full stop. Concrete Grey `#B7B2AA` lives in the wall.
- **Motion:** expo ease-out ("fast in, soft landing"), mask-rise reveals by word and by letter, 2–4 frame staggers, ≥ 0.4 s holds. No glow on type, no particles, no 3D type.
- **Gallery tags:** small Warm Paper slips with a rust index square, like museum labels.
- **End card:** A4 outline (trim path) → 297 mm dimension line → **MOTIF / 297** rises letter by letter → slogan → the rust full stop lands on the last tick → slow ambient push.

---

## 6. Music & sound design

**Score** (D minor, 100 BPM, all synthesised):

1. **Opening:** sub swell plus a glassy tone that rises in pitch as the line draws; first hit on frame 18; dark Dm drone.
2. **Development:** a deep pulse on every beat; clock tick/tock on 8ths; Dm9 → B♭maj9 → Gm9 → A7sus4 pads.
3. **Silence:** at the blank wall, everything stops except room tone and one clock ticking in the room. This is the film's strategic silence.
4. **Build:** the music returns on the poster press. A 16th-note pluck ostinato with ping-pong echo, a string swell, a riser, and ticks accelerating to 16ths. Reverse cymbal, then a **0.2 s gap**.
5. **Reveal:** sub boom plus a wide Fmaj9 chord stab, then a perspective dolly.
6. **Ending:** a callback to the opening line tone as the A4 outline draws, a low logo hit with Dm(add9) bells, and one last tick on the full stop, then everything decays.

**Sound design** (every visual action has one sound, no generic whoosh on every cut): ink plip, brush swish, directional whooshes on whips only, paper flick on the graphic cut, metal shimmer on the wheel, pen scratch on the outline, decelerating mechanical counter clicks on 210/297, paper flutter, the press, the smoothing swipe, gallery-tag ticks.

**Mix:** music and SFX stems sum exactly to the mix. Master: **−14.0 LUFS integrated, −1.2 dBTP true peak**, loudness range 7.4 LU. Low end is high-passed at 30 Hz and shelved to stay firm, not boomy. The limiter only works on the reveal transient.

---

## 7. Creative-director QC

| Check | Verdict |
|---|---|
| First two seconds compelling? | Yes. Motion starts on frame 0 (the line draws from the centre), the taillight lights up by 0.6 s with the first hit, and there's no logo or intro card. |
| Story clear without explanation? | Yes. Detail → format → blank wall → one poster → full wall → brand. The supers carry the argument in nine words. |
| Every shot has a purpose? | Yes. Each craft shot shows one quality (ink, brush, geometry, editorial type, mechanical detail, finish) and leads into the next. |
| Transitions motivated by movement? | Yes; see section 3. Only the reveal is a hard cut, and on purpose. |
| Motion design sophisticated? | One accent colour with meaning, a single type family, an A4/dimension-line system tied to the name, no templates. |
| Sound in sync? | Yes. Cues are generated from the same frame grid as the picture (sample = frame × 1600). |
| Music builds tension? | Yes: drone → pulse → silence → build → gap → reveal → resolve. |
| Product real and premium? | The **designs** are shown faithfully (never redrawn). The **physical product is not shown**: there was no footage. See the Filming Plan. |
| Brand recognisable? | Yes: palette, A4 outline, rust full stop, wordmark. **The wordmark is a placeholder** until the official logo is supplied. |
| Strong ending? | Yes: the full stop lands on the last tick, then a slow push and a held frame for looping. |

**What was changed after review (first-pass problems found on contact sheets):**
- Tilted macro views showed mirrored artwork past the poster edges. A bounds checker now verifies every frame, and four shots were reframed.
- The opening line sat *on top of* the taillight. It now widens, softens and melts into it.
- Depth of field was too weak to read as macro. It was roughly doubled, with the focal plane chosen per shot (along the drip, through the letterforms).
- The tiny labels disappeared over busy artwork. They became Warm Paper gallery tags.
- The window light was huge and harsh and drowned the posters. It became smaller and softer (6 cm penumbra), and the wall was brightened toward Warm Paper.
- The hero poster's entrance ghosted, because motion blur followed only the camera. It now samples the poster's motion too.
- The mix had no arc (the craft section was as loud as the reveal) and too much sub. Act 2 was pulled down about 5 dB, the low end tightened, and a 4 Hz bell beat removed.

---

## 8. Honest limitations

- **Source resolution.** The posters are ~700 px web files. The 1080p master holds up (macro moves stay under ~4× magnification and use real depth of field), but a **4K master isn't supported** by these sources and wasn't faked with upscaling.
- **No live-action footage.** Hands, adhesive peel, real wall, packaging and print texture are listed in `FILMING_PLAN.md` with exact slots in this edit.
- **Proportions.** The supplied designs aren't A4 ratio. They're shown at native proportion.
- **Placeholders.** The wordmark (no logo file supplied) and the collection tags (ART / AUTOMOTIVE / SPORT / CINEMA).
- **Third-party rights.** The designs include other brands' marks, a real athlete, a TV series and other designers' credits; see the Filming Plan.
