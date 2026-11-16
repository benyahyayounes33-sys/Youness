# MOTIF 297 — Live-Action Filming Plan

The supplied material was seven digital poster files (661–736 px wide, web JPEGs).
There was **no footage** of the physical product: no prints, paper, adhesive backing,
hands, packaging or real walls. The current film is built entirely from those files
with a virtual camera, plus a virtual wall. Nothing in it pretends to be live-action
product footage.

This plan lists the real shots that would replace or strengthen the virtual ones.
Every shot maps onto the existing edit (same beat grid, same transitions, same
sound cues), so the new footage drops into a timeline that is already timed and scored.

---

## Before the shoot — supply list

| Item | Why |
|---|---|
| **Print-ready master files** (A4 @ 300 dpi = 2480 × 3508 px, or vector/PDF) | Current files are ~700 px wide. That is enough for 1080p but not for macro detail or a 4K master. |
| **How each design is laid out on A4** (cropped, bordered or rescaled) | None of the supplied files is A4 ratio (they are 9:16, 4:5, 3:4 and 2:3). The film shows them at native ratio and does not invent a layout. |
| **Official MOTIF 297 logo files** (SVG/AI + usage rules) | The film uses a *typographic placeholder* set in Jost. It was not designed as, and must not be read as, the logo. |
| **Real collection names** | The tags ART / AUTOMOTIVE / SPORT / CINEMA are placeholders. |
| **Packaging** (only if it exists) | The brief mentions packaging. None was supplied, so none was shown. |
| **Rights confirmation** | See "Rights" at the end. |

---

## Kit

- **Camera:** any cinema or mirrorless body that shoots 4K/UHD 10-bit log at **120 fps** (macro and peel) and **24/30 fps** (wall).
- **Lenses:** 100 mm macro (1:1); 35 mm and 50 mm primes; probe lens optional (Laowa 24 mm) for gliding along the paper surface.
- **Support:** slider (60–120 cm) or small motion-control rig for repeatable parallax moves; tripod; top-down rig.
- **Light:** one large soft key through a window frame or 4×4 diffusion (recreates the film's window-light look); one hard "sun" source through a cucoloris shaped like window panes; black flags for negative fill; a thin strip light for edge/raking light.
- **Sound:** contact mic + small-diaphragm condenser, close-miked at 20–30 cm for paper, peel, press and smoothing; 60 s of room tone in each location.
- **Surface:** smooth matte wall painted close to Warm Paper `#F4F0E8`, or a light concrete-grey plaster close to `#B7B2AA`.

**Look:** expose for the print whites (never clip paper). Keep colour temperature consistent (≈ 5200 K key, warm sun accent). No teal-orange grade.

---

## Shot list

Timecodes refer to the current edit (30 fps). "Replaces" = the virtual shot this footage would take over.

### ACT 1 — The hook

| # | Shot | Framing / move | Spec | Sound to record | Replaces |
|---|---|---|---|---|---|
| L1 | **Taillight print detail in the dark** | 100 mm macro, the GT3 RS print lit only by a thin raking strip light. Start black, bring the light up so the red taillight appears first. Slow lateral slide 2–3 cm. | 120 fps, f/2.8, focus on the red strip | room tone, light switch (optional) | Shot 1 (00:00:00:00–00:00:02:12). Keep the motion-graphic rust line over it. |

### ACT 2 — The craft

| # | Shot | Framing / move | Spec | Sound | Replaces |
|---|---|---|---|---|---|
| L2 | **Ink & paper texture** | Extreme macro (1:1) along the clock poster's drip, plane tilted ~30° so focus falls off naturally. Slow tilt down the drip. | 120 fps, f/4, slider down | finger brushing paper | Shot 2 |
| L3 | **Brush-stroke detail** | Macro on the Supra brush lettering; land the downward move from L2. | 120 fps | — | Shot 3 |
| L4 | **Poster edge** | The A4 sheet's edge and corner in raking light, so paper thickness is visible. Push in. | 60 fps, f/5.6 | paper flick, sheet lifted | Shot 4/5 (or an insert) |
| L5 | **Hands handling the sheet** | Clean, neutral hands lift a print by its edges, turning it toward the light. Top-down or 45°. No jewellery, neutral sleeves (Obsidian/Concrete). | 60 fps, 50 mm | paper handling | New insert, ~1 s, before Shot 8 |
| L6 | **Adhesive backing removed** | Macro on a corner as the backing is peeled. Slow, continuous peel. **Only film this the way the real product works.** | 120 fps, 100 mm, f/4 | **contact-mic the peel** (the defining sound) | New insert at Shot 8 (00:00:09:27), before the A4 card |
| L7 | **Packaging** *(only if it exists)* | Product removed from its sleeve/envelope; one clean top-down move. | 60 fps | slide, open | New insert, Act 2 |

### ACT 3 — The transformation

| # | Shot | Framing / move | Spec | Sound | Replaces |
|---|---|---|---|---|---|
| L8 | **The blank wall** | Locked-off or very slow push on an empty wall with window light (cucoloris panes). Leave the centre clean for the super "A BLANK WALL / SAYS NOTHING." | 24/30 fps, 35 mm | 60 s room tone; a real clock tick | Shot 9 |
| L9 | **Placement** | Hands bring the GT3 RS print in from lower right; top edge aligned first, then pressed flat and smoothed with one hand pass. | 60 fps (conform to 30), 50 mm | press, smoothing swipe | Shot 10. Land the press exactly on **00:00:14:12** (frame 432). |
| L10 | **The wall fills** | Six more prints placed one per beat (see landing frames in the cue sheet). Camera pulls back on the slider. A motion-control repeat pass of the empty wall helps a clean edit. | 30 fps | each press | Shot 11 |

### ACT 4 — The brand

| # | Shot | Framing / move | Spec | Sound | Replaces |
|---|---|---|---|---|---|
| L11 | **Hero dolly** | Angled view (~30°) along the finished 2-3-2 wall, slow dolly left, shallow focus. Sun shape moves slowly across the prints. | 24/30 fps, 50 mm, f/2 | — | Shot 12 |
| L12 | **Foreground wipe** | Same dolly continuing past a dark foreground element (door frame, column, black flag) close to the lens, so it fully covers the frame. | same | whoosh is already designed | Shot 12→13 transition |

**Do not shoot:** a printer, unless MOTIF 297 actually prints in-house. Do not shoot packaging that does not exist. Do not stage customer testimonials or "unboxing by a customer".

---

## Wild sound list (record clean, 48 kHz / 24-bit)

paper lift · paper flick · sheet slide · **adhesive peel (slow, fast)** · press onto wall · hand smoothing · finger tap on print · room tone (60 s per room) · a mechanical clock tick (close and distant).
These replace the synthesised placeholders in `src/audio.py` one-for-one. The cue positions are already set.

---

## Rights (please check before paid use)

The supplied designs feature third-party marks and real people: Porsche crest and model names, Toyota/GR marks, the Nike logo, a footballer's likeness, and a TV series' stills, title and cast list. Some files also carry other creators' credits ("ABC.DESIGN", "@dransz_", "Design Professional of Smartphone"). Using these in **advertising** is a different question from selling decorative prints. Confirm you hold or license the rights, or swap in designs you own, before running the film as a paid ad.
