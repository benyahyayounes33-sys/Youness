# MOTIF 297 — "LOOK CLOSER"
### Pre-production bible for an 18-second premium commercial

| | |
|---|---|
| **Format** | 9:16 vertical · 2160 × 3840 (4K UHD vertical) master · **24 fps** · 18.0 s (15 s and 6 s cutdowns at the end) |
| **Tempo grid** | 90 BPM → **1 beat = 16 frames** at 24 fps. Every cut, hit and super sits on this grid. |
| **Story** | HOOK → PRODUCT REVEAL → EXPERIENCE → DESIRE → BRAND REVEAL |
| **In-film line** | **PEEL. PRESS. YOURS.** |
| **End card** | [OFFICIAL LOGO] · **WALLS WITH A POINT OF VIEW.** |

**The single most important production rule:** AI video models redraw images. They warp lettering and invent details, which your brief forbids. So in this plan **AI never draws your artwork.** AI generates the world: hands, liner, walls, rooms and light. Your real artwork is always composited in from the master file, or filmed for real. Section 4 explains how.

---

## Contents
1. Three commercial concepts
2. Storyboard with timestamps (recommended concept)
3. Shot-by-shot cinematography plan
4. Production method and the artwork-accuracy pipeline
5. AI video-generation prompts, shot by shot
6. Negative prompt
7. Sound-design timeline (frame-accurate)
8. Music direction
9. Editing, transitions, colour and finishing
10. Text overlays and tagline
11. Claims guardrails and QC checklist
12. What I need from you

---

## 1. Three original concepts

### Concept A — "LOOK CLOSER" ★ recommended
**Logline:** It opens like a supercar film: a light bar slides across black bodywork and a taillight ignites. Then the camera pulls back and you realise **it's printed on an A4 sheet in someone's hand.**

- **Hook (0–2 s):** a genuine double take. It looks like an automotive spot and turns out to be a poster. The reveal *is* the product demo, because the print holds up as cinema.
- **Body:** the application ritual filmed like a luxury unboxing. An ASMR liner peel, the top edge aligned, the sheet smoothed down onto a dark plaster wall as the liner is drawn away behind it.
- **Payoff:** a spotlight snaps on and the room comes alive. Designs swap on the beat to show the range. A final designed interior, then the brand.
- **Why it wins:** a thumb-stopping twist in under 2 s, the poster is the hero of every frame, it speaks to car enthusiasts first, and the swap beat opens it to film, sport, gaming and music fans.
- **Risk:** the hook design. Choose a design you hold paid-ad rights for (see section 11).

### Concept B — "ONE PRESS. ANY WORLD."
**Logline:** One gesture, a palm pressing a poster flat, match-cut across four rooms: a car lover's garage studio, a student's desk wall, a gamer's dark setup lit by monitor spill, a music lover's vinyl corner. Each press switches the room's light on.

- Rhythm-driven: one press per beat. The same hand position and frame position give a seamless match cut while the world changes around it.
- **Line:** *Same press. Your world.*
- **Why:** it speaks to every audience segment explicitly.
- **Risk:** four environments means more cost and more consistency risk. It also needs **real gaming and music designs** from your catalogue (none were supplied, and I won't invent artwork).

### Concept C — "PREMIERE"
**Logline:** A poster on a black wall, treated like a film premiere. In total darkness a single moving light passes across it, each pass revealing new detail (ink, edge, colour). The camera orbits; red-carpet silence; then a wall of three posters, each under its own pin-spot like a gallery opening.

- **Line:** *Every wall deserves a premiere.*
- **Why:** the most "luxury art" of the three, and perfect for film fans.
- **Risk:** it doesn't show the adhesive application, which is your product's key action.

**Recommendation:** shoot **Concept A**. It answers every point of the brief (macro, peel, application, tracking, light, orbit, final interior, brand) in 18 s, with the strongest hook. Concept B's match-cut press is reused inside A (shot 09) to reach the wider audience.

---

## 2. Storyboard — "LOOK CLOSER" (18.0 s · 432 frames @ 24 fps)

Source codes: **REAL** = film the physical print · **FILE** = virtual camera on the master artwork file (exact) · **AI** = generated, artwork-free · **AI+COMP** = generated with a blank stand-in sheet, real artwork composited in post · **GFX** = motion graphics.

| # | Time (s) | Frames | Act | Frame | Super | Source |
|---|---|---|---|---|---|---|
| 01 | 0.00–1.33 | 0–32 | HOOK | Pure black. A soft horizontal light bar glides across glossy black curves; a red taillight line ignites on beat 1 (f16). It reads as a real car. | — | **REAL** macro of the print (alt: FILE) |
| 02 | 1.33–2.67 | 32–64 | REVEAL | One continuous move: the macro pulls back fast (speed ramp), the paper edge slides into frame, and the whole A4 sheet appears, held by two fingertips, rim-lit in darkness. Double take. | `210 × 297 MM` hairline dimension (f52) | **AI+COMP** (alt: REAL) |
| 03a | 2.67–3.00 | 64–72 | REVEAL | Extreme macro: ink and paper grain on a detail of a second design. | — | **REAL** |
| 03b | 3.00–3.33 | 72–80 | REVEAL | Extreme macro: a third design, a different texture or colour. | — | **REAL** |
| 03c | 3.33–4.00 | 80–96 | REVEAL | Macro with a rack focus across the print surface from soft to razor-sharp lettering. | — | **REAL** |
| 04 | 4.00–5.33 | 96–128 | EXPERIENCE | Back of the sheet, black void. A fingertip lifts the liner corner; slow motion; a thread of light runs along the adhesive line. **No artwork visible.** | **PEEL.** (f100) | **AI** |
| 05 | 5.33–6.67 | 128–160 | EXPERIENCE | Dark charcoal plaster wall. Two hands bring the sheet's top edge to the wall; fingertips press it on beat 9 (f144). Slight handheld life. | **PRESS.** (f144) | **AI+COMP** |
| 06 | 6.67–9.33 | 160–224 | EXPERIENCE | The unveil. The camera tracks down with one palm smoothing the sheet onto the wall while the other hand draws the liner down from behind. Slow motion ramps to real time. | — | **AI+COMP** (best: REAL) |
| 07 | 9.33–10.67 | 224–256 | EXPERIENCE | Macro: the last palm press on the bottom corner, then the hand lifts away. The liner drifts out of frame. **Silence f244–256.** | — | **AI+COMP** |
| 08 | 10.67–13.33 | 256–320 | DESIRE | **Reveal on the hit (f256).** Match cut to wide: a minimalist dark interior. A ceiling pin-spot snaps on and the poster glows. Slow dolly back with a gentle arc; its reflection blooms on the polished floor. | **YOURS.** (f264) | **AI+COMP** |
| 09 | 13.33–14.67 | 320–352 | DESIRE | Grazing-angle orbit across the poster's surface. The artwork **swaps on every 8th note** (f320/328/336/344): car → film → sport → gaming or music (if supplied). | — | **AI+COMP** |
| 10 | 14.67–16.00 | 352–384 | DESIRE | Final composition: three posters in a precise row above a low black sideboard (unbranded turntable, a game controller, a film book), each under its own pin-spot. Slow push in. | — | **AI+COMP** |
| 11 | 16.00–18.00 | 384–432 | BRAND | The room lights power down, then the posters, then black. The official logo resolves (f392); the slogan follows (f400). Hold to end. | Logo + **WALLS WITH A POINT OF VIEW.** | **GFX** |

---

## 3. Shot-by-shot cinematography plan

**Global look.** Low-key, contrast about 8:1, rich blacks with detail at 2–3 % (never crushed), highlights rolled off. Warm 2700–3200 K key on the artwork, cool 5600 K moonlight fill only in the interior. Shoot camera-native 24 fps with a 180° shutter (1/48 s) unless overcranking. Log capture, 10-bit minimum.

**Art direction.** Black duvetyne studio (shots 01–04). A flat set wall in charcoal limewash, roughly `#24221F`, with subtle trowel texture (05–09). An interior set (08–10) with polished dark concrete floor, a low black oak sideboard, a large window with sheer curtain at frame edge, and one sculptural floor lamp (unlit). No visible brands anywhere.

**Talent / hands.** One pair of hands throughout. Natural skin, short clean unpainted nails, a fitted black fine-knit sleeve, no jewellery or watch. Hand-model prep: moisturise, matte powder to kill shine.

| # | Lens / aperture | Support and move | Capture | Light | Focus | Notes |
|---|---|---|---|---|---|---|
| 01 | 100 mm macro, f/4 | Micro slider, 3 cm lateral, very slow | 48 fps (2× slow) | One 4 ft LED tube on a boom, hand-swept across the print as the "light bar". A tiny red-gelled kicker accentuates the printed taillight. | Locked on the taillight line | Choose the crop so it reads as a real car. |
| 02 | 100 mm → (cut) 50 mm, f/2.8 | Slider pull-back; speed ramp 48 → 24 → 12 fps-equivalent in post | 48 fps | Hard rim from behind (snooted fresnel); faint bounce on the fingertips | Follow focus pulls from the macro plane to the sheet | Start frame must **match the last frame of 01** exactly (same crop). |
| 03a–c | Laowa 2× macro or 100 mm + extension tubes, f/5.6 | Locked or micro push | 24 fps | Raking light at about 10° to show ink and paper texture | 03c is a rack focus from soft to sharp | **This is the only honest way to show print quality: film the physical print.** |
| 04 | 100 mm macro, f/2.8 | Locked, slight drift | **120 fps** (5×) | Hard backlight grazing the liner edge; black flags | Focus on the peel line; rack along it | Film the **back** of the sheet: no artwork visible. |
| 05 | 35 mm, f/2 | Controlled handheld (very gentle), slow push | 48 fps | Soft key camera-left (1×1 with grid, 3200 K); top light on the wall edge | Fingertips and the top edge | Contact on f144 exactly. |
| 06 | 35 mm, f/2.8 | Vertical slide or crane-down, tracking the smoothing palm | **96 fps** ramping to 24 | Same key; a slow light sweep down the sheet as it flattens | Follow the palm | Highest-risk shot for AI. **Film practically if at all possible.** |
| 07 | 100 mm macro, f/2.8 | Locked | 48 fps | Grazing light along the wall shows the sheet now flat | Corner and palm | Hold the hand still in the 0.5 s of silence before the reveal. |
| 08 | 35 mm, f/2.8 | Dolly back about 1.5 m with a 10° arc right | 24 fps | Ceiling pin-spot 2700 K on the poster (switched on camera); moonlight window fill 5600 K; floor reflections | Deep: the poster and the room | The poster must be the brightest element in frame. |
| 09 | 50 mm, f/2 | Slow orbit from 60° grazing to frontal | 24 fps | Pin-spot plus a moving soft highlight across the surface | Rack from edge to centre | Designs swap on 8th notes (locked plate, comp swaps). |
| 10 | 35 mm, f/4 | Slow push in, 4 % | 24 fps | Three pin-spots, practical lamp off, moonlight | Deep | Symmetrical composition, generous negative space. |
| 11 | — | — | — | — | — | Motion graphics only. |

---

## 4. Production method: how the artwork stays 100 % accurate

**Rule 1 — AI never renders the artwork.** Any shot where artwork is visible is generated with a **blank matte light-grey stand-in sheet**. The real artwork is then **planar-tracked and composited** from the master file (Mocha Pro / After Effects / Nuke).

- Add a light-match pass: the grade's shadows and highlights, a soft-light layer for the moving light, and grain.
- This keeps typography, colours and proportions identical to your design, and keeps it razor-sharp at 4K even where the AI plate was upscaled.

**Rule 2 — Detail and print quality are filmed, never generated.** AI would invent paper texture, which would misrepresent the product.

- Shots 01 and 03 need the **physical print** under a macro lens. A phone with a clip-on macro lens is the minimum.
- If unavailable: a virtual camera over the master file (FILE) shows the *design* in detail. Label it accordingly and never call it print quality.

**Rule 3 — Shots without artwork are free for AI:** the back of the sheet and liner (04), the falling liner (07), empty rooms and walls.

**Rule 4 — Even "good" image-to-video clips get re-composited.** If you start a clip from a frame containing the real artwork, models drift over a few seconds. Treat the clip as a plate and re-track the true artwork over it.

**Rule 5 — Lock the world before generating motion.** Generate (or photograph) three **look-bible stills**: studio black, plaster wall with hands, interior. Use them as start frames or references for every clip, so walls, light and hands stay consistent. Lock seeds per shot. Reject any clip with a hand defect.

**Resolution and frame rate.**
- Generate every clip vertical 9:16 at the highest resolution your tool offers (typically 1080p) and at 24 fps.
- Upscale plates to 2160 × 3840 with a video upscaler before compositing; composite artwork from the 4K-ready print file.
- For slow motion, generate at real speed and retime with optical flow (RIFE / Twixtor / DaVinci Speed Warp). AI "slow motion" is inconsistent.

**Clip length.** Generate 5–8 s per shot and use the best 1–3 s. Make 4–6 variants per shot; expect a 15–30 % keep rate on hand shots.

**Audio.** If your generator produces audio (e.g. Veo), **mute it**. All sound comes from section 7.

---

## 5. AI video-generation prompts (Kling · Runway · Veo)

**How to use them:**
- Paste the **Prompt**.
- If your tool has a negative-prompt field (e.g. Kling), paste section 6 into it. If it doesn't, the "Avoid:" line inside each prompt does the job.
- Use **Mode** as written: T2V = text-to-video; I2V = image-to-video from a start frame; F/L = first-and-last-frame.
- Camera-motion controls, where available, should mirror the text.

### Look-bible stills (generate first with an image model; use as I2V start frames)
**LB-1 Studio black:**
```
Photorealistic still, vertical 9:16. A pure black studio void. A pair of hands with natural skin texture, short clean unpainted nails, fitted black fine-knit sleeves, no rings, no watch, holds a completely blank matte light-grey A4 sheet (exact 210 x 297 mm proportions, unprinted, no image, no text) by its top corners. A hard rim light from behind traces the sheet's edges and the fingertips; everything else falls to deep black. 50 mm lens, f/2.8, premium commercial photography, rich blacks with detail, soft highlight roll-off, subtle film grain.
```
**LB-2 Plaster wall:**
```
Photorealistic still, vertical 9:16. A dark charcoal limewashed plaster wall with subtle hand-troweled texture, lit by a soft warm 3200K light from camera left with a gentle falloff to deep shadow on the right. A completely blank matte light-grey A4 sheet (exact 210 x 297 mm proportions, unprinted, no text) is mounted flat at the centre of frame. 35 mm lens, f/2, premium commercial photography, rich blacks, controlled highlights, subtle film grain.
```
**LB-3 Interior:**
```
Photorealistic still, vertical 9:16, night. A minimalist dark interior: charcoal limewashed walls, a polished dark concrete floor with soft reflections, a low black oak sideboard, a large window at the right edge with sheer curtains glowing faintly with cool moonlight. On the wall above the sideboard, three completely blank matte light-grey A4 sheets (exact 210 x 297 mm proportions, unprinted) hang in a precise horizontal row at eye level, each lit by its own narrow warm 2700K ceiling pin-spot. Architectural Digest-level composition, symmetrical, generous negative space, rich blacks, subtle film grain. No logos, no text, no brands.
```

### 01 — HOOK "Bodywork"
*Mode: none (film the print). Fallback: I2V from a macro crop of the master file, minimal motion, re-composite after.*
```
Start frame: [macro crop of the real poster artwork showing the black car body and red taillight]. Extremely slow lateral camera slide to the right, as if on a micro slider. A soft horizontal band of white light glides once across the image from left to right, raking across the glossy black curves, and the red taillight line brightens gently as the light passes. Deep black surroundings. The image content stays completely unchanged: no morphing, no new details, no new reflections, no text changes. 100 mm macro look, shallow depth of field, 24 fps, 180-degree shutter, premium automotive commercial lighting, rich blacks, subtle film grain, vertical 9:16.
Avoid: morphing, warping, redrawn details, added text or logos, flicker.
```

### 02 — REVEAL "The double take"
*Mode: T2V (or I2V from LB-1), 5 s. Comp the artwork onto the sheet; the first frames are replaced by a zoom from the shot-01 crop.*
```
Starting extremely close on the surface of a blank matte light-grey A4 sheet in a pure black void, the camera pulls back smoothly and quickly, accelerating then easing out, until the whole sheet is revealed held upright by two fingertips at its top corners. The hands have natural skin texture, short clean unpainted nails and fitted black fine-knit sleeves; no rings, no watch. The sheet is completely blank, unprinted, exact 210 x 297 mm proportions, with crisp straight edges. A hard rim light from behind traces the sheet's edges and the fingertips; everything else is deep black. 100 mm to 50 mm look, f/2.8, motion blur on the fast part of the move, 24 fps, premium commercial cinematography, rich blacks, subtle film grain, vertical 9:16.
Avoid: any print or text on the sheet, extra fingers, bent or wavy paper, flicker.
```

### 03a / 03b / 03c — "Print detail"
*Mode: none: film the physical print (Rule 2). If footage is impossible, render FILE moves from the master files and do not describe them as print quality. No AI prompt is recommended for these shots on purpose.*

### 04 — "The peel"
*Mode: T2V, 5–6 s. Artwork-free.*
```
Extreme macro close-up in a pure black void, slow motion. We see the plain white back of an A4 sheet. A fingertip with a short, clean, unpainted nail gently lifts one corner of the white backing liner, and the liner slowly peels away in a smooth continuous curve, revealing a thin, even adhesive layer that catches a razor-thin line of warm backlight. Paper fibres glow along the edge. One hard backlight from above and behind, deep black everywhere else. 100 mm macro, f/2.8, very shallow depth of field, focus follows the peel line, smooth and continuous, 24 fps, premium commercial cinematography, rich blacks, subtle film grain, vertical 9:16.
Avoid: printed images or text anywhere, extra fingers, tearing, wrinkles, sticky strings, flicker.
```

### 05 — "Align & press"
*Mode: I2V from LB-2 (with the sheet removed from the wall in that still) or T2V, 5 s. Comp the artwork onto the sheet.*
```
Close-up, gentle slow push-in with very subtle handheld life. Two hands with natural skin texture, short clean unpainted nails and fitted black fine-knit sleeves (no rings, no watch) bring a completely blank matte light-grey A4 sheet (exact 210 x 297 mm proportions, unprinted, no text) to a dark charcoal limewashed plaster wall. The top edge is aligned carefully, then both index fingers press the top edge flat against the wall, left then right. The lower part of the sheet still curves slightly away from the wall. Soft warm 3200K key light from camera left, deep shadow on the right, the wall's subtle trowel texture visible. 35 mm, f/2, shallow depth of field, 24 fps, premium commercial cinematography, rich blacks, subtle film grain, vertical 9:16.
Avoid: print or text on the sheet, tape, pins, frames, extra fingers, crumpled paper, flicker.
```

### 06 — "The unveil" (hero action)
*Mode: T2V, 6–8 s; generate several variants. If the two-layer action fails, cover it in two cuts: 06a = palm smoothing (front, comp); 06b = liner pulled down seen from a low side angle (edge only, artwork-free). Practical filming strongly preferred.*
```
Medium close-up. The camera tracks smoothly downward, following one open palm that slowly smooths a completely blank matte light-grey A4 sheet (exact 210 x 297 mm proportions, unprinted, no text) flat onto a dark charcoal limewashed plaster wall from top to bottom, while the other hand draws a white backing liner down and away from behind the sheet. As the palm passes, the sheet lies perfectly flat against the wall. A soft band of warm light travels down the sheet with the hand. Hands with natural skin texture, short clean unpainted nails, fitted black fine-knit sleeves, no jewellery. Elegant, deliberate, unhurried movement. 35 mm, f/2.8, 24 fps, premium commercial cinematography, rich blacks, controlled highlights, subtle film grain, vertical 9:16.
Avoid: print or text on the sheet, air bubbles, wrinkles, creases, tearing, extra fingers, fused hands, flicker.
```

### 07 — "Last press"
*Mode: T2V, 5 s. Comp the artwork corner. Second pass (artwork-free) for the liner drop.*
```
Macro close-up on the bottom corner of a completely blank matte light-grey A4 sheet now lying flat on a dark charcoal plaster wall. A palm with natural skin texture presses the corner once, firmly and gently, holds for a beat, then lifts slowly away. Grazing warm light skims along the wall and reveals that the sheet sits perfectly flat. 100 mm macro, f/2.8, shallow depth of field, 24 fps, premium commercial cinematography, rich blacks, subtle film grain, vertical 9:16.
Avoid: print or text on the sheet, bubbles, creases, extra fingers, flicker.
```
```
Slow motion: a long white paper backing liner drifts down through a dark void past the camera, gently twisting, caught by a thin warm rim light, then falls out of frame. Black background, shallow depth of field, 24 fps, premium commercial cinematography, vertical 9:16.
Avoid: text, print, logos, flicker.
```

### 08 — "The room comes alive" (reveal)
*Mode: I2V from LB-3 (single-sheet version) or T2V, 6 s. Comp the artwork. The light switch-on must land on f256 when retimed.*
```
Starting on a medium shot of a completely blank matte light-grey A4 sheet (exact 210 x 297 mm proportions, unprinted) on a dark charcoal limewashed wall in near darkness. A narrow warm 2700K ceiling pin-spot switches on and lights only the sheet with a soft-edged pool of light. The camera then dollies slowly backward with a gentle arc to the right, revealing a minimalist dark interior at night: polished dark concrete floor softly reflecting the lit sheet, a low black oak sideboard, a large window at the right edge with sheer curtains glowing with cool moonlight. The lit sheet stays the brightest element in frame. 35 mm, f/2.8, 24 fps, Architectural Digest-level composition, premium commercial cinematography, rich blacks, controlled highlights, subtle film grain, vertical 9:16. No logos, no brands.
Avoid: text or print on the sheet, extra posters, cluttered decor, neon colours, oversaturation, flicker.
```

### 09 — "Desire orbit"
*Mode: T2V or I2V, 5 s. Lock the plate; the artwork swaps in comp every 8 frames.*
```
Close-up. A slow, smooth orbit around a completely blank matte light-grey A4 sheet (exact 210 x 297 mm proportions, unprinted) mounted flat on a dark charcoal limewashed plaster wall, moving from a grazing 60-degree side angle to nearly frontal. A soft warm highlight glides across the sheet's surface as the angle changes; the wall texture rakes in the side light. Rack focus from the near edge of the sheet to its centre. 50 mm, f/2, shallow depth of field, 24 fps, premium commercial cinematography, rich blacks, controlled highlights, subtle film grain, vertical 9:16.
Avoid: print or text on the sheet, glossy mirror reflections, bending paper, flicker.
```

### 10 — "Final composition"
*Mode: I2V from LB-3, 5 s. Comp three artworks.*
```
Wide shot, very slow push-in. A minimalist dark interior at night: charcoal limewashed walls, polished dark concrete floor with soft reflections, a low black oak sideboard. On it: an unbranded turntable with a black vinyl record, an unbranded matte black game controller, and a closed hardcover book. Above the sideboard, three completely blank matte light-grey A4 sheets (exact 210 x 297 mm proportions, unprinted) hang in a precise horizontal row at eye level, each lit by its own narrow warm 2700K pin-spot. Cool moonlight through sheer curtains at the right edge. Symmetrical, generous negative space, calm and luxurious. 35 mm, f/4, 24 fps, Architectural Digest-level composition, premium commercial cinematography, rich blacks, subtle film grain, vertical 9:16. No logos, no brand names, no text anywhere.
Avoid: print or text on the sheets, branded products, clutter, RGB/neon lighting, oversaturation, flicker.
```

### 11 — Brand reveal
*Mode: none. After Effects with the official logo file. Never generate or redraw the logo with AI.*

---

## 6. Negative prompt (paste in full where supported)
```
text, letters, words, numbers, typography, captions, subtitles, watermark, signature, logo, brand name, trademark, label, printed image on the blank sheet, artwork on the blank sheet, extra posters, distorted text, gibberish text, warped poster, bent paper, wavy paper, crumpled paper, torn paper, creased paper, air bubbles under paper, wrinkles, sticky residue strings, tape, pushpins, nails, frames, glass, glossy mirror reflections on paper, extra fingers, missing fingers, fused fingers, deformed hands, long nails, nail polish, rings, jewellery, watch, tattoos, plastic skin, waxy skin, morphing, melting, shape shifting, flicker, strobing, jitter, frame-to-frame inconsistency, sudden lighting changes, warping background, duplicated objects, low resolution, blurry subject, compression artefacts, noise blocks, oversaturated colours, neon RGB lighting, teal and orange grade, HDR look, CGI look, 3D render look, cartoon, illustration, anime, stock-footage look, cheap studio, cluttered background, people's faces, water droplets, wet surfaces on paper, smoke, particles, lens flare overload
```

---

## 7. Sound-design timeline (24 fps · 90 BPM · beat = 16 f)

Record **real** paper, liner and wall sounds with a contact mic and a small-diaphragm condenser at 20–30 cm (48 kHz / 24-bit). Synthesised placeholders are a fallback only. Every cue below is tied to a picture event.

| Time (s) | Frame | Picture | SFX | Music / ambience |
|---|---|---|---|---|
| 0.00 | 0 | Black | Near-silent room tone | Sub swell begins (felt more than heard) |
| 0.17–1.00 | 4–24 | Light bar crosses the "bodywork" | Soft airy light-sweep whoosh, panned L→R with the light | Sub swell continues |
| 0.67 | **16** | Taillight ignites | **Mechanical relay click** + glassy ignition tone | Low drone opens |
| 1.17–1.67 | 28–40 | Speed-ramp pull-back | Air whoosh peaking at f40 | Drone rises |
| 1.67 | 40 | Paper edge enters frame | Dry paper edge *flick* | — |
| 2.00 | **48** | Full sheet revealed (double take) | Deep, short **bass impact** (restrained) | Music hit, first beat of the pulse |
| 2.17 | 52 | `210 × 297 MM` draws | Fine hairline tone, very quiet | — |
| 2.67 / 3.00 / 3.33 | **64 / 72 / 80** | Macro inserts 03a/b/c | Three **precise mechanical clicks** (lens-focus clicks), slightly different pitches | Pulse continues |
| 3.33–4.00 | 80–96 | Rack focus | Soft "breath" texture (filtered air) | Pulse thins out |
| 4.00 | **96** | Back of sheet | — | **Music drops to near-silence** (sub pad only) |
| 4.08 | 98 | Nail touches the liner | Tiny fingernail *tick* | — |
| 4.17–5.33 | 100–128 | Slow-motion peel | **Signature ASMR liner peel**: slow crackle, close-mic, centred; "PEEL." super gets a soft paper tick at f100 | — |
| 5.33–6.00 | 128–144 | Sheet travels to wall | Soft air movement, paper flutter | Low pulse re-enters |
| 6.00 | **144** | Top edge meets wall | **Soft surface-contact *thup*** + "PRESS." | Pulse on beat |
| 6.17 / 6.42 | 148 / 154 | Fingertips press left, right | Two fingertip taps, panned left and right | — |
| 6.67–9.33 | 160–224 | The unveil | **Long liner peel** whose pace rises with the speed ramp + **palm smoothing swipe** (panned with the hand) + paper settling crackle | Build: pulse, rising granular paper texture, string harmonics, riser from f192 |
| 9.33 | **224** | Last palm press | Low-mid palm *thump* | Build peaks |
| 9.67–10.08 | 232–242 | Liner drifts away | Paper flutter, tiny landing tick at f242 | Riser into a reverse swell |
| 10.17–10.63 | **244–255** | Hand lifts away | **SILENCE** (all music and SFX cut; room tone only) | — |
| 10.63 | 255 | — | Light-switch *click* (1 frame before the reveal) | — |
| 10.67 | **256** | **REVEAL**: pin-spot on, dolly back | **Deep cinematic bass impact** + light-bloom swell | **Hero theme lands** (chord lift) |
| 11.00 | 264 | "YOURS." | Soft paper tick | Hero theme |
| 10.67–13.33 | 256–320 | Room reveal | Warm room tone, very distant city hum, subtle floor-reflection shimmer | Hero theme sustains |
| 13.33 / 13.67 / 14.00 / 14.33 | **320 / 328 / 336 / 344** | Artwork swaps | Four soft, tight **shutter-like clicks**, one per swap | Pulse on 8ths |
| 14.67–16.00 | 352–384 | Final composition | Quiet; a slow airy swell into the end | Theme opens, then a reverse swell from f376 |
| 16.00 | **384** | Lights power down | Low relay *thunk* (power-down) | Music cuts to the sub tail |
| 16.33 | **392** | Logo resolves | **Sonic logo**: a quick peel + soft tap (0.6 s), sitting on a low, soft impact | — |
| 16.67 | 400 | Slogan | Faint air swell | Final chord tail |
| 17.33–18.00 | 416–432 | Hold | Tail to silence by f432 | — |

**Mix:** −14 LUFS integrated, ≤ −1 dBTP. Deliver stems (music / SFX / ambience) that sum to the mix. Mono-compatible (phone speakers). Keep the sub firm but controlled: high-pass at 30 Hz, no boom under the peel.

---

## 8. Music direction

- **Commission an original 18 s score.** No library or stock tracks. Title: *"Paper Engine."*
- **Identity idea:** build the instruments from the product itself. Record the liner peel, paper taps and wall contacts, then make them the score's textures (granular pads from the peel, percussion from paper slaps layered with sub). The music is literally made of the poster.
- **Tempo / key:** 90 BPM, D minor, lifting to F major at the reveal (f256) and resolving on an open D5/add9 under the logo.
- **Palette:** sine-sub pulse, paper-granular pads, felt piano (single notes, not chords), cello harmonics and sul-tasto swells, restrained low percussion. No vocals, no EDM drops, no trailer clichés.
- **Arc:**
  - 0–2 s mysterious and dark, with the sub swell.
  - 2–4 s a confident pulse.
  - 4–6.7 s almost nothing, to make room for the peel.
  - 6.7–10.2 s a controlled build.
  - **10.2–10.7 s silence.**
  - 10.7–16 s the hero theme: warm, expensive, assured.
  - 16–18 s resolve into the sonic logo.
- **Sonic logo:** a 0.6 s "peel + tap" over a low tone. Reuse it at the end of every brand video so the sound becomes recognisable.

---

## 9. Editing, transitions, colour and finishing

**Cutting philosophy.** Cut picture *to the sound timeline* in section 7: every cut is on a beat or on its sound event. There are only five transition types in the whole film, and each one is motivated.

| Transition | Where | How |
|---|---|---|
| **Macro-to-wide (continuous)** | 01 → 02 | 02's first frame matches 01's last crop. Speed ramp: ease-in over 6 f to about 300 % speed, ease-out over 10 f (Bezier). Optical-flow motion blur. |
| **Rhythm cuts** | 03a/b/c, 09 swaps | Hard cuts on 8th notes (8 f). No dissolves. |
| **Speed ramp in slow motion** | 04, 06 | 04 stays slow (5×). 06 goes from 4× slow to real time over the last 20 frames, so the smoothing hand "lands". |
| **Match cut** | 07 → 08 | The hand lifts off the macro corner; cut on f256 to the wide where the poster sits in the same screen position. Light switch and bass impact sit on the cut. |
| **Light-driven end** | 10 → 11 | The practical lights power down in sequence, black for 4 f, then the logo resolves. No whoosh transitions anywhere in the film. |

**Colour pipeline.**
- Grade the **world**, not the artwork. Composite the artwork after the creative grade, through a light-match layer (shadow and highlight shaping only, no hue shift). This keeps colours true to the design.
- Look: rich blacks lifted only 2–3 %, gentle S-curve, warm highlights on the pin-spots, cool moonlight confined to the window side, natural skin. No teal-orange, no crushed blacks, no oversaturation.
- Finish with uniform fine grain (35 mm character, low intensity) over everything, including the composited artwork, so it sits *in* the image.

**Masters and cutdowns.**
- **Master:** 2160 × 3840, 24 fps, ProRes 422 HQ.
- **Delivery:** H.265/H.264 at 2160 × 3840, about 35–50 Mbps, plus 1080 × 1920 at 16–20 Mbps; AAC 320 kb/s.
- **15 s cutdown:** drop 03b and 03c (keep 03a for 16 f); shorten 06 to 48 f and 09 to 2 swaps.
- **6 s bumper:** 01 → 02 (double take) → 08 (reveal) → logo.

**Safe zones (Reels / TikTok, 2160 × 3840).** Keep supers inside x 160–1840 and y 440–2760. Paid ads add a CTA button at the bottom, so nothing important below y 2760.

---

## 10. Text overlays and tagline

| Time (s) | Frame | Text | Style |
|---|---|---|---|
| 2.17–3.33 | 52–80 | `210 × 297 MM` | Tiny tracked caps (36 px @4K), hairline dimension line beside the sheet, Warm Paper `#F4F0E8` at 70 % |
| 4.17–5.33 | 100–128 | **PEEL.** | Geometric sans (Jost or the official brand font), Medium, 150 px @4K, tracking +40, centred upper third, mask-rise 6 f, expo ease-out |
| 6.00–6.67 | 144–160 | **PRESS.** | Same style, lands with the contact sound |
| 11.00–12.67 | 264–304 | **YOURS.** | Same style, slightly larger (180 px), lower third over the dark floor |
| 16.33–18.00 | 392–432 | [OFFICIAL LOGO] | Official file only, never redrawn. Clean mask reveal, 10 f |
| 16.67–18.00 | 400–432 | **WALLS WITH A POINT OF VIEW.** | 52 px @4K, tracking +260, Warm Paper; the full stop in Signal Rust `#B64A3A` lands last |

- **In-film line:** **PEEL. PRESS. YOURS.**
- **Brand slogan (end card):** **WALLS WITH A POINT OF VIEW.**
- **Alternative campaign lines:** *LOOK CLOSER.* · *MADE TO BE STARED AT.* · *OWN THE WALL.*
- **Optional paid-ad end frame:** add "SHOP THE COLLECTION" under the slogan (no product claims).

---

## 11. Claims guardrails and QC checklist

**Never state or imply, unless confirmed in writing:** waterproof, water-resistant, removable, repositionable, reusable, residue-free, damage-free, wall-safe, fade-proof, UV-resistant, tear-proof, scratch-resistant, "museum-grade", "archival", "HD print", "gloss" or "matte" (until the finish is confirmed). The film shows *only* the action (peel, press) and the result (a poster on a wall).

**Physical accuracy.**
- This plan assumes the adhesive liner is on the **back** and is removed while applying. If your application method differs, tell me and I'll re-board shots 04–07.
- The artwork is visible from the front at all times; a peel never "reveals" the image.

**Rights for paid advertising.** Several supplied designs show third-party trademarks (Porsche, Toyota/GR, Nike), a real athlete's likeness, TV-series stills and other designers' credits. Ad platforms often reject or remove ads using these. Build the paid version around designs you own or have licensed, especially the hook.

**Per-shot QC (before approving any clip).**
- [ ] The composited artwork matches the master file: difference-blend check, letter-by-letter text check, correct proportions, nothing added or cropped.
- [ ] Hands: five fingers, natural joints, no fused or extra digits in any frame (scrub frame by frame).
- [ ] No AI-invented text, logos or brands anywhere in the plate.
- [ ] Paper sits flat when shown applied (no bubbles or creases unless real).
- [ ] Lighting continuity matches the look-bible stills.
- [ ] Every visual event has its sound; every sound has its picture.
- [ ] Supers inside safe zones; logo untouched.
- [ ] Loudness −14 LUFS / ≤ −1 dBTP; picture 2160 × 3840 @ 24 fps.

---

## 12. What I need from you
1. **Official logo** (SVG/AI + usage rules) and **brand font**.
2. **Print-ready artwork** for every design in the film (A4 @ 300 dpi or vector), plus how each design is laid out on A4.
3. **Real photos of the product:** front, back with the liner, edge/thickness, and one photo of a poster applied to a wall.
4. **Confirmed facts:** paper finish, adhesive and liner type, application method, and any claims you can prove.
5. **Which designs are cleared for paid ads**, ideally including at least one gaming design and one music design for shot 09.
6. **Physical prints** for the macro shots (01, 03) if we film them.
