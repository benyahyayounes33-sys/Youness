# ONELINE: 10 Cinematic Ad Films

**Peel. Stick. Say something.**

These are ten 15-second vertical films for a premium adhesive poster brand. Each one has its own
technique, look and sound, and all ten end on the same brand signature.

| # | Film | Technique | Look | Sound | Best made by |
|---|---|---|---|---|---|
| 01 | **MICRON** | Extreme macro | Black void, one grazing light | Binaural ASMR, no music | Real phone macro + AI |
| 02 | **EVERY VERSION OF YOU** | Match-cut story | Five film looks, one fixed frame | One unbroken piano line | AI or real |
| 03 | **BILLBOARD** | Scale illusion | Rain-soaked night city → bedroom | A city that shrinks | AI + composite, or a real model |
| 04 | **WEIGHTLESS** | Surreal motion | Dark gallery, light shafts, slow-mo | Choir, breath, reversed swells | AI + composite |
| 05 | **THE MOVE-IN** | Stop-motion | Pastel, symmetrical, 12 fps | Pizzicato + paper foley | Real (phone + tripod) |
| 06 | **PERFECT FIT** | Satisfying ASMR | Top-down, flat-perspective, warm white | Foley played as a drum kit | Real (phone + tripod) |
| 07 | **IMPACT** | High-speed | Black studio, strobes, pigment | Trailer hits, then silence | AI + composite |
| 08 | **24 HOURS** | Light transitions | One locked frame, the light performs | A day compressed into sound | AI relighting + composite |
| 09 | **RECOLOR** | Room transformation | Grey room floods with colour | The room builds its own song | AI + grade |
| 10 | **MAISON** | Luxury editorial | Black & white, the poster is the only colour | Solo cello, heels, silk | AI or real |

---

## Before you generate anything

### 1. Keeping your artwork identical (read this first)

AI video models redraw everything in the frame, including a poster you upload. Over 15 seconds
they bend letters, change faces and invent details. Writing "don't change the poster" in the
prompt helps, but it never guarantees the result. Studios solve this by never trusting the
generator with the artwork:

| Shot type | Method |
|---|---|
| **Poster visible and still** (the camera moves, the poster doesn't) | **Composite keyframe → image-to-video.** Place your real print file onto the start frame (Photoshop or Firefly, perspective warp), then generate with gentle motion. If the art drifts, replace it with tracking (next row). |
| **Poster moves, peels or flies** | **Tracking plate → replace in post.** Generate the shot with a plain light-grey sheet with a small black dot in each corner. Then planar-track it (After Effects + Mocha, DaVinci Resolve, or CapCut's tracking) and pin your real artwork onto it. Lay the plate's shadows (Multiply) and highlights (Screen) over the art so it sits in the light. |
| **Macro, hands, peeling, smoothing** | **Shoot it for real.** A phone in macro mode, a tripod and one LED lamp beat AI for paper texture and finger physics, and it shows your actual product. |

**Final check:** scrub every shot frame by frame at 200% zoom on the poster. If any letter is
warped, replace the poster using tracking.

### 2. Prompt conventions

- `[POSTER]` means attach your poster image as the start frame or image reference.
- Every prompt where the poster is visible must end with the **POSTER LOCK**:

```
POSTER LOCK: The poster is the attached reference image reproduced exactly: identical artwork, colours, typography, spelling and layout. No added, removed or altered text or details. It behaves like a real sheet of thick matte paper: flat and rigid, bending only where the action bends it, with real thickness and a crisp edge.
```

- If your tool has a negative-prompt field, paste this:

```
warped text, morphing letters, gibberish text, changed artwork, extra posters, watermark, logo, melting, rubbery paper, fabric-like paper, extra fingers, deformed hands, plastic skin, flicker, jitter, CGI look, cartoon render, oversaturation, stutter
```

- **Build the end cards in your editor; don't generate them.** AI can't draw your logo reliably.

### 3. Technical specs (all films)

- **Format:** 9:16 vertical, master at 2160 × 3840, 24 fps. Film 05 animates at 12 fps, with each
  image held for 2 frames.
- **4K:** most AI video tools output below 4K. Generate at the highest resolution your tool
  offers, upscale with a dedicated video upscaler, then do the final grade. Master in 10-bit
  (ProRes 422 HQ or DNxHR HQX) and upload a high-bitrate H.264/H.265 export.
- **Takes:** generate 3–4 takes per shot and keep the one with the most convincing physics.
- **Sound off:** feeds autoplay muted, so every hook must work without sound.
- **Text safe zone:** at 1080 × 1920 (double these for 4K), keep text out of the top ~250 px,
  the bottom ~450 px and the right ~150 px, where the app's buttons and captions sit. These are
  approximate, so check each platform.
- **Audio:** 48 kHz / 24-bit. Mix to about −14 LUFS integrated, with true peak at −1 dBTP.
  Phone speakers can't play deep sub-bass, so layer every low boom with a mid-frequency click or
  crack so it still lands on a phone.
- **Music:** use only music cleared for advertising, either commissioned or licensed from a
  production-music library with ad rights (on TikTok, the Commercial Music Library). Trending
  songs used in normal posts are **not** licensed for paid ads. Each film describes its music by
  style, tempo and instruments, so a composer or a library search can match it.

### 4. Brand signature (shared by all ten)

Each film has its own look and sound, but all ten close the same way so they build one brand.

**End card**, the last 2.0 s (48 frames at 24 fps):

| Frames | Picture | Sound |
|---|---|---|
| 0–10 | Background settles (Ink `#0b0b0c` or Paper `#f6f4ef`, per film). The words "ONE" and "LINE" in Anton fade up over 6 frames, centred just above the middle. The full wordmark is about 60% of the frame width. | The film's music resolves or cuts out |
| 6–24 | The red line (`#ff3b30`) draws left to right between ONE and LINE, easing out at the end | **Sonic logo, part 1: the peel.** A rising crackle, panned left to right with the line |
| 24 | The line lands | **Sonic logo, part 2: the tack.** One dense, soft thump of paper meeting the wall, plus a short low tone |
| 26–40 | "Peel. Stick. Say something." in Inter Medium, small, under the wordmark | Air tail |
| 32–48 | Your handle or URL, smaller | Room tone, then silence |

- **Sonic logo:** the peel and tack together last under 1 second, and they are the brand's sound
  signature. Each film plays them in its own sound world (noted per film), but the rhythm stays
  the same: a rising crackle, then one landing.
- **Loops:** TikTok and Reels replay automatically. Where a film says so, its last frame flows
  back into its first.
- If your brand name isn't ONELINE, swap the wordmark and keep the system.

### 5. Choosing which posters to feature

Your photos include posters with cartoon and film characters, a singer's photo, film posters and
car-brand logos. That causes three practical problems for these ads:

- **Ad review.** Meta and TikTok check ads for intellectual property. Ads that show other
  companies' characters, celebrities, film posters or logos are likely to be rejected, or taken
  down later when the rights-holder reports them, and that can restrict your ad account.
- **AI tools.** AI video tools often refuse uploads that show a real celebrity's face or a
  well-known character.
- **Profanity.** The "breathe…" newspaper poster contains a swear word, and both platforms
  restrict profanity in ads. Use it in normal posts, not paid ads.

**For paid ads, feature designs you own.** The two typographic posters ("Think outside the box" and
the newspaper one) are creatively the strongest heroes, but only if they're your own designs. They
look like designs that circulate online, so check. Every film treats the poster as a swappable
input, so new original designs drop straight in.

### 6. Claims check

Only show what your product really does:

- **Film 09** puts posters up on a wall without removing them, so it makes no removal claim. If
  you make a version that swaps posters, your adhesive must peel off cleanly with no residue or
  wall damage.
- **Film 08** shows the poster in every kind of light. If your finish is glossy, keep the
  reflections natural and don't claim "glare-free".
- **Films 06 and 07** imply the poster stays put. Test it first on painted walls and on tiles.

---

## 01 · MICRON
*Extreme macro · binaural ASMR*

**Concept.** A peel filmed at the scale of a dust mite. As the backing liner separates, the gap
glows like a sunrise over a white glacier. Adhesive strands stretch like dew on spider silk. The
paper meets the wall like a tide rolling across a desert. The moving edge of the peel is a
perfect line: the ONELINE mark, drawn by physics. Only in the last seconds does the camera pull
back far enough to show that it's a poster.

- **Best with:** any poster. Big flat areas of colour make the ink texture spectacular in macro
  (for example a single-colour print).
- **Visual identity:** a pitch-black void lit by one hard light at a grazing 5–10° angle, so every
  paper fibre throws a shadow. Macro and probe lenses with deep, focus-stacked sharpness. A cold
  neutral grade with crushed blacks. The only colours are the ink and one warm glint.
- **Sound identity:** binaural, close-mic ASMR built for headphones, with every micro-sound
  magnified and moving through space. No music until 0:12.
- **Sonic logo:** the real peel crackle recorded at macro scale, then the tack as a deep, dry thump.

**Hook (0:00–0:02).** Black screen. A razor-thin line of light slowly opens across the frame with a
crackling sound. Nobody can tell what it is (a horizon? a glacier? an eclipse?), so they keep watching.

**S1 · 0:00–0:02.5 · Horizon**
- **Camera:** probe lens at surface level, side-on to the liner, locked off with an almost invisible
  push-in (about 2% over the shot). Put the line on the middle third of the frame.
- **Action:** the liner lifts away and light floods the widening gap. Adhesive micro-strands
  stretch, glint and snap.
- **SFX:** cellophane and Velcro crackle slowed by 30%, panned left to right with the line. Each
  strand snap is a tiny high "tik" on the exact frame it breaks, over a low air bed.
```
Extreme macro probe-lens shot at surface level, side-on: a glossy white release liner slowly peels away from the matte adhesive back of a thick sheet of paper. The separating edge forms one glowing horizontal line across a pitch-black frame, like a sunrise over a white glacier. Microscopic strands of clear adhesive stretch, glint and snap in a hard raking light. Fine dust floats in the beam. Locked-off camera with an almost imperceptible push-in. Focus-stacked deep sharpness, cold neutral grade, crushed blacks, photorealistic macro photography, 9:16 vertical.
```

**S2 · 0:02.5–0:05 · Ink City**
- **Camera:** top-down over the printed face, with a slow sideways slide like a plane flying over a
  city at night.
- **Action:** the ink dots and paper fibres look like a lit city grid, and the liner's edge slides
  underneath like a moving shadow.
- **SFX:** a soft continuous paper hiss, granular "glitter" ticks as bright ink dots pass, and a
  distant low wind (altitude).
- **Shoot this one for real,** because AI invents ink patterns. Use your phone's macro mode or a
  clip-on 10–15× lens and one LED at a low angle. Slide the poster slowly under the phone.
```
Top-down extreme macro of the printed surface of a matte paper poster, individual pigment ink dots and paper fibres visible, resembling a city grid seen from an airplane at night. Slow, steady lateral slide. A hard low-angle light reveals the paper's texture. The colours are those of the attached poster [POSTER]. Photorealistic, 9:16 vertical.
```

**S3 · 0:05–0:08 · Contact**
- **Camera:** low, side-on macro at the wall surface, locked. The painted plaster looks like a
  desert landscape.
- **Action:** the adhesive face descends and touches the wall, and a wave of contact rolls across
  like a tide, squeezing out a shimmer of air. Speed ramps from 100% to 25% at contact.
- **SFX:** a whoomp of displaced air, pitched down, then a dry rolling "zipper" sound that follows
  the contact wave, under a swelling low tone.
```
Low side-on extreme macro at the surface of a white painted wall whose plaster texture looks like a desert landscape. The adhesive back of a thick poster descends from above and makes contact; a smooth wave of contact rolls across the surface like a tide, pushing out a faint shimmer of air and lifting tiny dust particles into a raking light. Locked-off camera, slow motion, deep focus, cold neutral grade, black surroundings, photorealistic, 9:16 vertical.
```

**S4 · 0:08–0:10.5 · Fingerprint**
- **Camera:** macro at 45° to the surface, tracking slowly with the thumb.
- **Action:** a thumb presses and slides across the poster, its fingerprint ridges like sand dunes,
  and the paper flattens perfectly behind it.
- **SFX:** close-mic skin-on-paper friction and one tiny squeak, then a deep, satisfying thud when
  full contact is made.
- **Shoot for real if you can:** hands and skin are where AI fails most.
```
Macro shot at 45 degrees: a human thumb presses onto the matte surface of [POSTER] on a wall and slides slowly across it, the fingerprint ridges visible like sand dunes, the paper flattening perfectly behind the thumb. Camera tracks slowly with the thumb. Hard raking light, black surroundings, realistic skin texture, natural paper behaviour, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S5 · 0:10.5–0:13 · The Pull**
- **Camera:** one continuous pull-back from paper texture to the full poster on a charcoal wall
  under a single spotlight. Build it as an "infinite zoom" by joining the macro, close and wide
  shots with scale-matched zoom transitions.
- **Action:** for the first time you see what it is: a poster, perfectly flat on a dark wall.
- **SFX:** a rising airy whoosh (0.6 s) opening into room tone. At 0:12.0 comes the film's first
  musical sound.
```
Wide-to-medium shot of [POSTER] perfectly flat on a dark charcoal wall, lit by a single tight spotlight from above, the rest of the room in darkness. Slow, steady pull-back. Matte paper, crisp edges, faint dust in the light beam. Cold neutral grade, deep blacks, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S6 · 0:13–0:15 · End card (Ink background)**

**Sound timeline**

| Time | Sound |
|---|---|
| 0:00.0 | Near-silence (room tone at −50 dB) |
| 0:00.2 | Peel crackle begins, binaural, left to right |
| 0:02.5 | Paper hiss and glitter ticks, wind at altitude |
| 0:05.4 | Air whoomp; the contact "zipper" rolls from 0:05.6 to 0:07.8 |
| 0:08.2 | Skin friction; squeak at 0:09.9; thud at 0:10.3 |
| 0:10.5 | Rising whoosh |
| 0:12.0 | **First music:** a sub hit (45 Hz plus a click layer for phones) and one sustained low felt-piano note |
| 0:13.0 | Sonic logo |

**Edit**
- **No hard cuts.** Each shot drifts out of focus into light, and the next begins from the same
  blur (a "focus-breath" dissolve of 6–8 frames).
- **Speed ramp at 0:05.4:** 100% down to 25% over 8 frames, back to 100% by 0:07.5.
- **Text:** none until the end card.
- **Finish:** no added grain, a faint vignette to deepen the void.
- **Loop:** the film ends on black and starts on black, so it loops seamlessly.

**Brand reveal.** On black, the line of light from 0:00 slides back in from the left. It turns
Signal Red as it reaches the gap between ONE and LINE, and the wordmark fades up around it.

---

## 02 · EVERY VERSION OF YOU
*Match-cut storytelling · one unbroken piano line*

**Concept.** One gesture across thirty years. A hand smooths a poster onto a wall, and with every
sweep the film jumps to a new chapter of a life: a child's bedroom, a teenager's room, a student
flat, a first apartment, a home. The rooms, the decades and the hands all change, but the gesture
and its position on screen never do. In the last shot, the adult's hand finishes the sweep and a
small hand beside it smooths a poster of its own. The cycle starts again.

- **Super:** "Every version of you deserves a wall."
- **Best with:** five different posters, one per chapter: something bright and playful (child),
  music or editorial (teen), typographic (student), a car or travel print (first apartment) and
  your hero design (now).
- **Visual identity:** the frame never moves: 50 mm, eye level, the poster centred, the hand
  entering from the right. Each chapter has its own film look:
  - **Child:** warm, faded late-90s home video, heavy grain, sun-bleached.
  - **Teen:** cool, harsh on-camera flash, slightly overexposed (mid-2000s digital camera).
  - **Student:** tungsten night, desk lamp, deep shadows.
  - **First apartment:** soft, clean daylight.
  - **Now:** the brand grade, rich and warm-neutral.
- **Sound identity:** one unbroken felt-piano phrase (a simple 4-note motif at 72 BPM) runs across
  every cut: the continuity of one person. Under it, each chapter has its own room sound. The
  smoothing "shhk" is the identical sound every time, as a sonic match cut.
- **Sonic logo:** the piano plays the peel as a soft glissando and the tack as its final low note.

**Hook (0:00–0:02).** An extreme close-up in faded home-video colour. A small child's hand slaps a
poster on crooked and smooths it with a big sweep. At 1.6 s, mid-sweep, the hand becomes a
teenager's: same motion, same spot. Viewers spot the pattern instantly and stay to see where it goes.

> Every cut happens mid-sweep, with the hand at the exact centre of the screen.

**S1 · 0:00–0:01.6 · Child**
- **Camera:** locked 50 mm at eye level, medium close-up, with the poster filling about 60% of the frame.
- **Action:** a small hand with a plaster on one finger presses the poster onto a pastel wall with
  crayon scribbles, then sweeps right to left.
- **SFX:** the "shhk", a giggle off-screen, a muffled TV cartoon from another room.
```
Locked-off medium close-up, 50mm lens at eye level: a small child's hand with a plaster on one finger and felt-tip marks on the knuckles presses [POSTER] onto a pastel yellow bedroom wall with crayon scribbles at the edge, then smooths it with one sweeping right-to-left motion. Warm, faded late-1990s home-video look, heavy grain, sun-bleached colours, afternoon light. Realistic hand anatomy and paper physics, 9:16 vertical. + POSTER LOCK
```

**S2 · 0:01.6–0:04 · Teen**
- **Action:** a hand with chipped black nail polish and a woven bracelet, against a dark-blue wall
  with old tape marks and photo-booth strips.
- **SFX:** the same "shhk", bass leaking from headphones on the bed, a phone buzzing.
```
Locked-off medium close-up, 50mm lens at eye level: a teenager's hand with chipped black nail polish and a woven friendship bracelet presses [POSTER] onto a dark blue bedroom wall with old tape marks and photo-booth strips, smoothing it with one sweeping right-to-left motion. Harsh on-camera flash, slightly overexposed, cool mid-2000s digital camera look. Realistic hand and paper physics, 9:16 vertical. + POSTER LOCK
```

**S3 · 0:04–0:06.4 · Student**
- **Action:** an ink-stained hand with a hair tie on the wrist, against a white rental wall, with a
  coffee mug's edge in the foreground.
- **SFX:** "shhk", rain on the window, a kettle clicking off.
```
Locked-off medium close-up, 50mm lens at eye level: an ink-stained hand with a hair tie on the wrist presses [POSTER] onto a plain white rental-flat wall at night, smoothing it with one sweeping right-to-left motion; the blurred edge of a coffee mug in the foreground. Warm tungsten desk-lamp light, deep shadows, rain-streaked window reflections. Realistic hand and paper physics, 9:16 vertical. + POSTER LOCK
```

**S4 · 0:06.4–0:08.8 · First apartment**
- **Action:** a hand with a simple watch, against fresh greige paint, with a houseplant leaf in the foreground.
- **SFX:** "shhk", the city through an open window, keys dropped into a bowl.
```
Locked-off medium close-up, 50mm lens at eye level: an adult hand wearing a simple minimalist watch presses [POSTER] onto a freshly painted greige wall, smoothing it with one sweeping right-to-left motion; a soft houseplant leaf in the foreground. Clean, soft natural daylight, modern apartment. Realistic hand and paper physics, 9:16 vertical. + POSTER LOCK
```

**S5 · 0:08.8–0:13 · Now, and next**
- **Camera:** the film's only camera move. After the sweep, a slow pull-back with a slight dolly
  left (about 3 s).
- **Action:** the adult hand (with a wedding ring) finishes its sweep. As the camera pulls back, a
  young child beside them stands on tiptoe and smooths a smaller poster onto the wall at their own
  height, with the same sweep. Faces stay soft or out of frame.
- **SFX:** two "shhk"s a beat apart, one big and one small, which are also the motif's last two
  notes. A quiet house and birdsong.
- **Super (0:11.3–0:12.9):** "Every version of you deserves a wall."
```
Medium shot slowly pulling back with a slight dolly left: an adult hand wearing a wedding ring finishes smoothing [POSTER] onto a warm white wall in a calm, sunlit family home; beside them a young child on tiptoe smooths a smaller poster onto the same wall at child height with the same sweeping gesture. Faces softly out of focus at the top of frame. Rich warm-neutral premium colour grade, soft window light, gentle film grain, realistic hands and paper, 9:16 vertical. + POSTER LOCK
```

**S6 · 0:13–0:15 · End card (Paper background)**

**Music and sound timeline**

| Time | Sound |
|---|---|
| 0:00.0 | Piano note 1 (the motif begins); child's room sound |
| 0:01.6 | Note 2 on the cut; the teen's room sound replaces the child's |
| 0:04.0 | Note 3; rain and kettle |
| 0:06.4 | Note 4; the city |
| 0:08.8 | The motif repeats an octave lower and fuller (left-hand chord); a quiet house, birds |
| 0:11.0 | Two "shhk"s land as the motif's final two notes |
| 0:13.0 | Piano glissando (peel), low note (tack) |

**Edit**
- **Cut on motion:** every cut lands on the frame where the hand is at screen centre. While
  editing, keep a fixed guide overlay so the poster rectangle sits in the same place in all five
  chapters.
- **Hard cuts:** add a 2-frame motion-blur bridge across each cut. No dissolves: the change of film
  look is the time jump.
- **Lead with sound:** each chapter's room sound starts 4 frames before its picture cut (a J-cut),
  so the ear moves first.

**Brand reveal.** On Paper, the red line draws with the piano glissando and lands on the low note.

---

## 03 · BILLBOARD
*Optical illusion (forced perspective) · a city that shrinks*

**Concept.** It opens like a global campaign: a giant poster glowing on a skyscraper at night,
rain falling, traffic streaming below, a helicopter orbit. Then the camera pulls back too far.
A desk lamp, a coffee mug the size of a stadium, a hand. The city is a tabletop model, and the
billboard is a poster on a bedroom wall. The scale snaps.

- **Super:** "Billboard energy. Bedroom wall."
- **Best with:** a bold graphic poster that reads from a distance like real outdoor advertising.
- **Visual identity:** a night city in teal and sodium orange: rain, wet reflections, horizontal
  anamorphic-style flares, haze. The model city is filmed with a probe lens at "street" height so it
  reads as full-size. The reveal is a warm, intimate bedroom lit by a tungsten desk lamp.
- **Sound identity:** a huge city: high-altitude wind, a distant helicopter, swelling traffic, a far
  siren, a deep cinematic drone. At the reveal the whole city shrinks into a tiny, tinny toy sound
  coming from the model, swallowed by quiet room tone and a lamp click. A sound illusion to match
  the picture.
- **Sonic logo:** a rising city whoosh for the peel; a heavy, intimate thump in a small room for the tack.
- **Practical build:** a tabletop city (cardboard or foam buildings, LED strips, black acrylic for
  wet streets) on a desk in front of the wall with the poster. Film it for real with a probe lens
  or a phone's ultra-wide close to the model, or generate it entirely with AI and composite the poster.

**Hook (0:00–0:02).** A low angle up a skyscraper in the rain. At the top, a colossal glowing
poster, and the camera cranes up toward it. It looks like a real outdoor campaign.

**S1 · 0:00–0:02.5 · The Tower**
- **Camera:** extreme low angle, ultra-wide, craning up the facade toward the poster.
- **SFX:** rain, wind at altitude, a deep drone swelling, a distant siren.
- **Composite:** pin the real poster onto the lit rectangle in post.
```
Extreme low-angle ultrawide shot craning up the side of a glass skyscraper at night in the rain; at the top, an enormous illuminated poster [POSTER] mounted like a billboard, lit by floodlights. Teal and sodium-orange city light, rain streaks, wet reflective surfaces, haze, horizontal anamorphic lens flares. Photorealistic, epic scale, 9:16 vertical. + POSTER LOCK
```

**S2 · 0:02.5–0:05 · The Orbit**
- **Camera:** a "helicopter" orbit at roof level around the billboard, about a 20° arc, with a
  rooftop water tower passing in the foreground for parallax.
- **SFX:** a low, rhythmic helicopter rotor fades in, with gusts of wind.
```
Aerial-style orbit at rooftop level around a giant illuminated poster billboard [POSTER] on a skyscraper at night, a rooftop water tower passing in the foreground for parallax, rain falling, city lights and light trails far below. Teal and sodium-orange grade, haze, anamorphic flares. Photorealistic, 9:16 vertical. + POSTER LOCK
```

**S3 · 0:05–0:08 · Street Level**
- **Camera:** a probe-lens glide down a wet avenue at street height. Headlights pass, the billboard
  looms at the end of the street, and its reflection shimmers in a puddle.
- **SFX:** tyres on a wet road (pass-bys panning across), a car horn, the rain getting heavier, the drone rising.
```
Low street-level gliding shot down a rain-soaked city avenue at night, cars with glowing headlights passing, a huge illuminated poster billboard [POSTER] high above at the end of the street, its reflection shimmering in a puddle in the foreground. Shot through a probe lens close to the ground. Teal and sodium-orange grade, anamorphic flares, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S4 · 0:08–0:11 · The Pull**
- **Camera:** one continuous pull back and up, with no cut. The edge of a wooden desk enters frame,
  then a giant coffee mug and a desk lamp. A human hand reaches in and smooths the poster's corner.
  The scale snaps.
- **SFX:** at 0:09.0 the whole city pitches up an octave and narrows to a tiny, tinny band over
  0.4 s. Lamp click at 0:09.6, then quiet room tone, and the hand's soft "shhk" at 0:10.2.
```
Continuous pull-back revealing that a rainy night city of skyscrapers is a detailed miniature model on a wooden desk in a bedroom; the giant "billboard" is [POSTER] on the bedroom wall behind the model. A coffee mug and a desk lamp tower over the tiny buildings; a human hand reaches in and smooths the poster's corner. Warm tungsten lamp light mixing with the model's teal and orange LEDs. Photorealistic, 9:16 vertical. + POSTER LOCK
```

**S5 · 0:11–0:13 · The Room**
- **Camera:** wide, eye level, with a slight push-in. A person sits cross-legged on the bed, looking
  up at the poster above their tiny city.
- **SFX:** room tone, a sip of coffee, and a tiny rain sound from the model (a spray bottle).
- **Super (0:11.4):** "Billboard energy. Bedroom wall."
```
Wide eye-level shot of a cosy bedroom at night: a young person sits cross-legged on the bed looking up at [POSTER] on the wall above a desk holding a glowing miniature city model. Warm tungsten desk lamp, small teal and orange LED lights in the model, slight push-in. Photorealistic, intimate, 9:16 vertical. + POSTER LOCK
```

**S6 · 0:13–0:15 · End card (Ink background).** A row of tiny streetlights switches on from left
to right and becomes the red line.

**Music and sound timeline**

| Time | Sound |
|---|---|
| 0:00 | Drone and rain, distant siren |
| 0:02.5 | Helicopter rotor joins |
| 0:05 | Tyres on wet asphalt, horn; the drone climbs |
| 0:08.6 | Peak: a hybrid orchestral hit (low brass and taiko, with a crack layer) |
| 0:09.0 | **The shrink:** the whole city pitched up an octave and band-passed to a tiny sound |
| 0:09.6 | Lamp click, then room tone |
| 0:11.0 | One soft lo-fi electric-piano chord, held |
| 0:13.0 | Sonic logo: city whoosh (peel), small-room thump (tack) |

**Edit**
- **S1–S3 feel like one continuous flight:** join them with dissolves that use rain streaks as the wipe.
- **S4 is the climax:** one unbroken move. At 0:09.0, take the grade from teal and orange to warm
  tungsten over 12 frames.
- **Text:** the super is the only text before the end card.

**Brand reveal.** On Ink, the tiny streetlights become the red line, then the wordmark and endline appear.

---

## 04 · WEIGHTLESS
*Surreal product movement · choir and breath*

**Concept.** A dark, monumental gallery where gravity has been switched off. Posters drift through
shafts of light, turning slowly like sculptures. One by one, their backing liners lift away on
their own and fall like white petals. Each poster glides to the wall and settles with one soft
breath. The elegance of a perfume campaign, for paper.

- **Super:** "Effortless."
- **Best with:** calm palettes and photography: minimalist designs and photographic prints.
- **Visual identity:** a monumental dark gallery: polished concrete, charcoal walls, high
  windows. Thick light shafts through haze. 85 mm lens, slow arcs, everything in slow motion
  (about 120 fps). Graphite tones and warm white light, so the only colour is the poster.
- **Sound identity:** ethereal. A wordless choir pad, reversed reverb swells that "breathe" into
  each movement, airy whooshes like exhales, slowed paper flutters. Each landing is a soft felt
  thump with a long cathedral reverb.
- **Sonic logo:** a slowed, silk-like tear in reverb for the peel; the choir resolving on a felt
  thump for the tack.
- **Realism:** thick paper doesn't ripple like fabric. The prompts ask for rigid, slow tumbling with
  only a gentle flex.

**Hook (0:00–0:02).** In darkness, a single white liner falls through a shaft of light like a
feather, flipping slowly. The camera tilts up to show a poster floating above it, face down,
slowly turning toward us. Impossible, but photoreal.

**S1 · 0:00–0:02.5 · Petal**
- **Camera:** 85 mm, a slow tilt up from the falling liner to the floating poster.
- **SFX:** a reversed reverb swell into the choir, the airy flutter of the liner.
- **Composite:** generate with a blank tracking sheet, then pin your art.
```
In a dark monumental gallery, a single white glossy backing sheet drifts down through a shaft of volumetric light like a feather, flipping slowly. The camera tilts up to reveal [POSTER] floating weightlessly high above, face down, slowly rotating to face the camera. The poster is rigid thick paper turning as one flat sheet, not fabric. Haze, dust in the light, polished concrete floor, charcoal walls, warm white light, graphite tones, slow motion, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S2 · 0:02.5–0:05 · Constellation**
- **Camera:** a slow dolly forward through three suspended posters at different depths (parallax),
  with focus shifting from one to the next.
- **SFX:** soft air passes as each poster slides past the lens (left, then right), and the choir
  swells a little.
```
Slow dolly forward through a dark gallery where three posters float weightlessly in mid-air at different depths, each slowly turning as a rigid flat sheet, catching shafts of volumetric light through haze. Focus racks gently from the nearest poster to the farthest. Polished concrete, charcoal walls, warm white light, graphite tones, slow motion, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S3 · 0:05–0:08 · The Unveiling**
- **Camera:** close, 100 mm, a slow arc around one poster's corner.
- **Action:** the liner peels itself away corner first, as if pulled by an invisible hand. It curls
  and drifts off into the dark.
- **SFX:** a delicate peel crackle slowed by 50% with a long reverb; the choir rises half a step.
```
Close-up slow arc around the corner of a poster floating in mid-air in a dark gallery: its glossy white backing liner peels away by itself, corner first, as if pulled by an invisible hand, curling gracefully and drifting off into the darkness, revealing the adhesive back. A shaft of warm white light, haze, floating dust, slow motion, photorealistic, 9:16 vertical.
```

**S4 · 0:08–0:11 · The Kiss**
- **Camera:** side-on to the wall plane, slow motion (about 120 fps).
- **Action:** the poster glides to the wall and touches at the centre first. Contact spreads to the
  edges, and a puff of dust lifts off the wall into the light.
- **SFX:** a slow inhale (0:08.0–0:08.8), then a felt thump at 0:09.2 with a cathedral reverb, and the choir resolves.
```
Side-on slow-motion shot along a charcoal gallery wall: a poster [POSTER] glides through the air and meets the wall, touching at the centre first, contact spreading smoothly to the edges until it is perfectly flat; a soft puff of dust lifts off the wall into a shaft of warm light. Haze, graphite tones, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S5 · 0:11–0:13 · The Gallery**
- **Camera:** wide and symmetrical, with a very slow push-in.
- **Action:** three posters hang in a perfect row, the liners lie on the floor like petals, and a
  figure in a long black coat walks slowly across the frame and pauses.
- **SFX:** footsteps echoing, the choir holding.
- **Super (0:11.5):** "Effortless."
```
Wide symmetrical shot of a monumental dark gallery: three posters hang in a perfect row on a charcoal wall, white backing liners scattered on the polished concrete floor like fallen petals, a figure in a long black coat walks slowly across the frame and pauses to look. Volumetric light shafts, haze, very slow push-in, graphite and warm white tones, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S6 · 0:13–0:15 · End card (Ink background).** The last white petal falls through the frame,
and the red line draws in its wake.

**Music and sound timeline**

| Time | Sound |
|---|---|
| 0:00 | Reversed swell into a choir pad (major 7th) |
| 0:02.5 | Air passes; the choir thickens |
| 0:05.0 | Slowed peel crackle; the choir rises half a step |
| 0:08.0 | Inhale |
| 0:09.2 | Felt thump with a 4 s cathedral reverb; the choir resolves |
| 0:11.0 | Footsteps in a big room, choir sustain |
| 0:13.0 | Sonic logo: silk tear (peel), felt thump (tack) |

**Edit**
- **Transitions:** cut on light flares, letting a bright shaft fill the frame for 4 frames to hide
  each cut. No hard cuts in darkness.
- **Slow motion:** if your takes aren't slow enough, use optical-flow interpolation and deliver at 24 fps.
- **Grade:** slightly milky lifted blacks, warm highlights, soft halation on the light shafts.

**Brand reveal.** The petal falls, the red line draws, then the wordmark and endline appear on Ink.

---

## 05 · THE MOVE-IN
*Stop-motion · pizzicato and paper*

**Concept.** Moving day. The room is empty because the new tenant has gone down for another box.
A shipping tube rolls in by itself, pops its cap, and the posters take over. They unroll, flip off
their backing like pancakes, fold the liners into paper planes and fly them out of the window.
Then they flop end over end across the floorboards, climb the wall and arrange themselves into a
perfect gallery wall. The tenant walks back in and drops the box.

- **Super:** "No nails. No tape. No drama."
- **Best with:** 4–6 mixed posters (a gallery set).
- **Visual identity:** real stop-motion at 12 fps, each frame held twice. Its handmade imperfection
  (slight light flicker, paper "boil") is the charm. A locked, perfectly symmetrical wide shot:
  sage walls, honey floorboards, a big window with soft north daylight, flat graphic composition.
- **Sound identity:** playful and handmade: pizzicato strings, kalimba and woodblock at 112 BPM.
  Every poster movement gets exaggerated but real paper foley: flaps, rustles, tiny "pap-pap"
  steps, a "fwip" for each liner flip, a cork pop for the tube cap.
- **Sonic logo:** a quick kalimba glissando for the peel, a woodblock "tok" for the tack.
- **How to make it (recommended):** a phone on a tripod, with exposure and white balance locked,
  and a stop-motion app with onion-skinning. Hold posters mid-move with removable putty or fishing
  line. 12 photos per second of screen time means about 130 photos for the 11 seconds of animation.
  Using your real posters shows your real product. AI can imitate stop-motion, but it warps the
  posters, so the prompts below are for previsualisation and for the room background.

**Hook (0:00–0:02).** An empty, perfectly symmetrical room. A shipping tube rolls in from the left
by itself, stops dead centre, wobbles, and its cap pops off. Movement that shouldn't happen in an
empty room stops the scroll.

**S1 · 0:00–0:02 · The Tube**
- **Camera:** locked wide, one-point perspective; the window is centred.
- **SFX:** cardboard rolling rumble, a wobble rattle, the cork "pop" at 0:01.8.
```
Stop-motion animation style, real miniature-set photography, 12 frames per second: a perfectly symmetrical empty room with pastel sage-green walls, honey-coloured floorboards and a large open window with soft north daylight. A cardboard shipping tube rolls in from the left on its own, stops in the centre, wobbles, and its end cap pops off. Locked-off wide camera, one-point perspective, handmade tactile texture, slight frame-to-frame light flicker, 9:16 vertical.
```

**S2 · 0:02–0:05 · Liftoff**
- **Action:** rolled posters slide out and unroll with a snap. Each flips its liner off, and the
  liners fold themselves into paper planes and glide out of the open window.
- **SFX:** three unroll snaps and three "fwip"s on the beats, paper-folding crinkles, and a little
  whoosh for each plane.
```
Stop-motion animation, real paper on a real set, 12 fps: rolled posters slide out of a cardboard tube on a honey-coloured wooden floor and unroll themselves with a snap; their white backing sheets flip off, fold themselves into paper airplanes and glide out through an open window. Symmetrical pastel sage room, soft north daylight, locked-off wide camera, handmade charm, 9:16 vertical. + POSTER LOCK
```

**S3 · 0:05–0:08 · The March**
- **Action:** the posters flop end over end across the floorboards like inchworms, then climb the
  wall in little jumps.
- **SFX:** "pap-pap" paper steps, each on a pizzicato note, and a scratchy "climb" sound on the wall.
```
Stop-motion animation, 12 fps: several posters flop end over end across honey-coloured floorboards like inchworms, then climb up a pastel sage-green wall in small jumps. Real paper, real set, symmetrical locked-off wide shot, soft north daylight, playful handmade movement, 9:16 vertical. + POSTER LOCK
```

**S4 · 0:08–0:11 · The Hang**
- **Action:** the posters jostle into a gallery grid. One nudges a crooked neighbour straight while
  a small spirit level slides in and its bubble centres. Then they slap flat one after another.
- **SFX:** the level's "tink" at 0:09.4, then slap, slap, slap on the beats at 0:10.0, 0:10.5 and 0:11.0.
```
Stop-motion animation, 12 fps: posters on a pastel sage-green wall jostle into a neat gallery grid; one poster nudges a crooked neighbour straight while a small wooden spirit level slides into place and its bubble centres; then they press themselves flat one after another. Real paper on a real set, symmetrical locked-off wide shot, soft daylight, 9:16 vertical. + POSTER LOCK
```

**S5 · 0:11–0:13 · Busted**
- **Action:** the door opens, and the tenant's legs come in carrying a box. The box drops, and the
  posters freeze, looking innocent.
- **SFX:** door creak, footsteps, the box hitting the floor at 0:11.8. **The music stops dead** for
  one beat of silence, then a single kalimba "tink".
- **Super (0:12.1):** "No nails. No tape. No drama."
```
Stop-motion animation, 12 fps: a door opens in a pastel sage-green room and a person's legs in jeans and trainers walk in carrying a cardboard moving box, which drops to the floor; on the wall, a perfectly arranged gallery of posters sits completely still. Symmetrical locked-off wide shot, honey floorboards, soft daylight, comedic timing, 9:16 vertical. + POSTER LOCK
```

**S6 · 0:13–0:15 · End card (Paper background).** A strip of red paper slides in, in stop-motion,
and becomes the line.

**Music and sound timeline (112 BPM)**

| Time | Sound |
|---|---|
| 0:00 | Room tone, then the cardboard rumble; pop at 0:01.8 starts the music: pizzicato, kalimba and woodblock |
| 0:02 | Unroll snaps and "fwip"s on the beat; paper-plane whooshes |
| 0:05 | "Pap-pap" steps follow the pizzicato line |
| 0:09.4 | Spirit-level "tink" |
| 0:10.0 / 0:10.5 / 0:11.0 | Three slaps, played like a kick drum |
| 0:11.8 | Box drop, **music stops**; one beat of silence, then one kalimba "tink" |
| 0:13.0 | Sonic logo: kalimba glissando (peel), woodblock "tok" (tack) |

**Edit**
- **Frame rate:** animate at 12 fps (each frame held twice) on a 24 fps timeline.
- **Cuts:** S1–S4 are one continuous locked shot, with no cuts at all. S5 is the only cut, to the
  door, then back to the wide.
- **Keep the flicker:** leave the slight exposure flicker, which reads as handmade. Lock white
  balance so the colour doesn't drift.

**Brand reveal.** On Paper, the red paper strip slides in, then the wordmark and endline appear.

---

## 06 · PERFECT FIT
*Satisfying ASMR · foley played as a drum kit*

**Concept.** An "oddly satisfying" film made with a luxury eye, where everything fits to the
millimetre. A liner peels off in one unbroken curl. A poster lowers into a gap with a hair's
clearance. A smoothing card leaves not a single bubble. A spirit-level bubble glides to centre on
the beat. A poster's edges land exactly on the grout lines of white tiles. Every action lands on
the beat, because the foley is the drum kit.

- **Super:** "Perfectly placed."
- **Best with:** any poster. Typographic designs look best because of their crisp edges. Your own
  photos already show posters on white square tiles, so use that.
- **Visual identity:** dead-on, flattened framing (a long 100–135 mm lens) and top-down shots.
  Soft, diffused daylight from a big window. Minimalist warm white, greige and oak. Perfect
  symmetry, slightly bright and airy, grid compositions. Every cut is on the bar.
- **Sound identity:** foley played as percussion over a minimal deep-house groove at 100 BPM. The
  peel is a hi-hat roll, poster contact is the kick, the smoothing card is a brushed snare, the
  level bubble is a rim click, and the tile alignment is a finger snap. Mic everything extremely
  close and dry.
- **Sonic logo:** a hi-hat roll for the peel, a kick for the tack.
- **How to make it:** shoot it for real on a phone and tripod, because "satisfying" depends on real
  physics. At 100 BPM one bar is 2.4 s, and each shot is one bar.

**Hook (0:00–0:02.4).** Top-down: fingers lift the corner of the backing liner and peel it off in
one long, unbroken, spiralling curl that drops perfectly into a small bin. Clean and hypnotic.

**S1 · 0:00–0:02.4 · The Curl**
- **Camera:** top-down, 35 mm, locked.
- **SFX:** a hi-hat roll building with the peel, and a soft "tock" as the curl lands in the bin on beat 4.
```
Top-down locked shot on a warm white oak table in soft diffused daylight: fingers lift the corner of the glossy white backing liner of a poster and peel it off in one long, unbroken, spiralling curl that drops neatly into a small white bin. Minimalist, symmetrical, high-key, crisp detail, oddly satisfying, photorealistic, 9:16 vertical.
```

**S2 · 0:02.4–0:04.8 · The Gap**
- **Camera:** front-on, 135 mm (flattened), locked.
- **Action:** hands lower a poster into the exact gap between two framed mirrors, with about a
  millimetre to spare on each side. It touches the wall on beat 1.
- **SFX:** the kick on contact.
```
Front-on telephoto shot, flat perspective, of a warm white wall with two thin oak-framed mirrors: two hands lower [POSTER] into the exact gap between them with a hair's clearance on each side and press it flat to the wall. Soft diffused daylight, minimalist greige and oak interior, perfect symmetry, oddly satisfying precision, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S3 · 0:04.8–0:07.2 · The Pass**
- **Camera:** front-on, 100 mm, locked.
- **Action:** a felt-edged smoothing card slides from top to bottom in one stroke, and a soft
  highlight sweeps across a dead-flat surface.
- **SFX:** a brushed-snare stroke for the whole pass.
```
Front-on locked shot: a felt-edged smoothing card slides from the top to the bottom of [POSTER] on a warm white wall in one slow, even stroke, a soft highlight sweeping across a perfectly flat, bubble-free surface. Diffused daylight, minimalist interior, crisp detail, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S4 · 0:07.2–0:09.6 · Level**
- **Camera:** close-up, eye level with the top edge.
- **Action:** a brass-and-oak spirit level rests on the top edge, and its bubble glides to dead
  centre on beat 3.
- **SFX:** the rim click on the exact frame the bubble stops.
```
Close-up at eye level of a small brass-and-oak spirit level resting on the top edge of a poster on a warm white wall; the bubble glides and stops precisely in the centre between the two lines. Soft daylight, shallow depth of field, crisp detail, oddly satisfying, photorealistic, 9:16 vertical.
```

**S5 · 0:09.6–0:12 · The Grid**
- **Camera:** macro at one corner, locked.
- **Action:** the poster's corner lands exactly on a crossing of tile grout lines, so its edges
  continue the grid.
- **SFX:** a finger snap; the groove thins to just kick and snap.
```
Macro shot of glossy white square wall tiles: the corner of a poster is pressed onto the tiles so that its corner lands exactly on the intersection of two grout lines and its edges align perfectly with the grout grid. Soft diffused daylight, crisp detail, minimal, oddly satisfying precision, photorealistic, 9:16 vertical.
```

**S6 · 0:12–0:13 · The Grid, wide**
- **Camera:** a pull-back, the film's only camera move, to a wall of white tiles with several
  posters in a perfect grid, every edge on a grout line.
- **Super (0:12.0):** "Perfectly placed."
```
Pull-back to a wide front-on view of a wall of glossy white square tiles with several posters arranged in a perfect grid, every poster edge aligned exactly with the grout lines. Soft daylight, minimalist bathroom-kitchen aesthetic, perfect symmetry, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S7 · 0:13–0:15 · End card (Paper background)**

**Music and sound timeline (100 BPM, one bar = 2.4 s)**

| Time | Sound |
|---|---|
| 0:00 | Bar 1: hi-hat roll (peel); curl lands in the bin on beat 4 |
| 0:02.4 | Bar 2: kick on the poster's contact; the deep-house bass enters |
| 0:04.8 | Bar 3: brushed snare (smoothing card) |
| 0:07.2 | Bar 4: rim click on the bubble |
| 0:09.6 | Bar 5: finger snap; everything drops out except the kick |
| 0:12.0 | Half bar: the full groove returns under the pull-back |
| 0:13.0 | Sonic logo: hi-hat roll (peel), kick (tack) |

**Edit**
- **Cut on the downbeat**, always. If an action lands a few frames early, slip the clip so it
  lands exactly on the beat.
- **Framing:** keep the poster or action dead centre in every shot so the eye never hunts.
- **Text:** the super only.

**Brand reveal.** The red line draws on a hi-hat roll and lands on the kick.

---

## 07 · IMPACT
*High-speed cinematography · trailer hits, then silence*

**Concept.** At 1,000 frames per second, a palm slaps a poster onto a wall dusted with fine
pigment powder. The air blast at contact throws the powder outward in a perfect ring, in the
poster's own colours, rolling like a shockwave. Hair whips, and particles hang in the air like
galaxies. Then it snaps back to real time and silence. The poster sits flat and clean in the
middle of a radial burst, like a painting.

- **Super:** "Make an impression."
- **Best with:** a poster with one dominant colour and strong contrast. Match the powder to the
  poster's colours.
- **Visual identity:** a black studio with one hard key light and two strobes edge-lighting the
  powder. Razor-sharp with no motion blur, very high contrast, deep blacks, saturated pigment.
- **Sound identity:** trailer-grade sound design: a ramping whoosh, the impact slowed down (sub boom
  plus a layered crack), powder hissing like distant fireworks, a low heartbeat through the slow
  motion, then total silence, then a real-time "snap".
- **Sonic logo:** a reversed whoosh for the peel; a boom plus crack for the tack.
- **Realism:** the powder is on the wall, not on the poster. The air blast from the slap pushes it
  outward, so the face of the poster stays clean.

**Hook (0:00–0:02).** For 8 frames at real speed, a hand with a poster rushes at the wall (blur and
whoosh). At contact the image drops to 1,000 fps, and a ring of coloured powder blasts outward
from all four edges. The sudden change of speed is the hook.

**S1 · 0:00–0:02 · Contact**
- **Camera:** front-on at the wall, 35 mm. Speed ramps from 100% to about 4% at 0:00.33.
- **SFX:** the whoosh, then at contact a slowed sub boom with a crack layer and a low rumble.
```
High-speed 1000fps cinematography in a black studio: a hand slaps [POSTER] flat onto a dark wall that is dusted with fine coloured pigment powder; at the moment of contact the air blast throws the powder outward from all four edges of the poster in a perfect expanding ring, in the colours of the poster. Hard key light and two edge strobes, razor-sharp particles with no motion blur, deep blacks, saturated colour, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S2 · 0:02–0:05 · Shockwave**
- **Camera:** low, side-on, looking along the wall's surface.
- **Action:** the ring of powder rolls outward like a shockwave, swirling into vortices, while the
  poster stays perfectly flat.
- **SFX:** a low rumble and a granular hiss, panned outward.
```
Low side-on 1000fps shot looking along the surface of a dark wall: a ring of coloured pigment powder rolls outward from the edges of a poster pressed flat on the wall, curling into slow vortices like a shockwave, the poster itself perfectly flat and clean. Black studio, hard edge strobes, razor-sharp particles, deep blacks, saturated colour, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S3 · 0:05–0:08 · The Face**
- **Camera:** a close-up of the person, 85 mm, at 1,000 fps.
- **Action:** hair whips in slow motion, powder particles drift past their eyes, and they blink slowly.
- **SFX:** a heartbeat thump and a slowed breath.
```
High-speed 1000fps close-up portrait in a black studio: a person with a strong profile, hair whipping slowly through the air, fine coloured pigment particles drifting past their eyes as they blink slowly; hard key light and rim strobes, razor-sharp detail, realistic skin texture, deep blacks, saturated colour, photorealistic, 9:16 vertical.
```

**S4 · 0:08–0:10.5 · The Crown**
- **Camera:** wide, 45° to the wall, at 1,000 fps.
- **Action:** the powder cloud forms a crown around the poster, and the hand slowly lifts away from
  the paper.
- **SFX:** a rising granular shimmer, the heartbeat speeding up.
```
Wide 1000fps shot at 45 degrees to a dark wall: a cloud of coloured pigment powder blooms into a crown shape around a poster pressed flat on the wall, while a hand slowly lifts away from the poster's surface. Black studio, hard strobes, razor-sharp particles, deep blacks, saturated colour, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S5 · 0:10.5–0:13 · The Print**
- **Camera:** front-on wide; the speed ramps back to 100%.
- **Action:** the powder settles in under a second. The poster sits flat and clean in the middle of
  a radial burst painted onto the wall.
- **SFX:** **0.5 s of total silence** (0:10.6–0:11.1), then one real-time "snap" (a hand clap, dry)
  and the room tone returns.
- **Super (0:11.4):** "Make an impression."
```
Front-on wide shot in a black studio at real speed: the last pigment dust settles, revealing a poster perfectly flat and clean on a dark wall at the centre of a radial burst of coloured powder sprayed across the wall around it like a painting. Hard key light, deep blacks, saturated colour, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S6 · 0:13–0:15 · End card (Ink background).** The red line slams in with its own small burst of
red powder.

**Music and sound timeline**

| Time | Sound |
|---|---|
| 0:00 | Ramping whoosh |
| 0:00.33 | Impact: slowed sub boom with a crack layer, then a long low rumble |
| 0:02 | Granular powder hiss, panned outward |
| 0:05 | Heartbeat pulse at 60 BPM, slowed breath |
| 0:08 | Shimmer rises; the heartbeat speeds up |
| 0:10.6 | **Silence** |
| 0:11.1 | Real-time snap; room tone |
| 0:13.0 | Sonic logo: reversed whoosh (peel), boom plus crack (tack) |

**Edit**
- **Speed ramps:** use real speed for only 8 frames at the start and from 0:10.5. Everything else
  is extreme slow motion.
- **Cuts:** hard cuts, each landing on a particle peak or a heartbeat.
- **Grade:** crush the blacks to true black, push the powder's colour saturation, and keep the
  poster's own colours true to the file.

**Brand reveal.** The red line hits like the slap, with a tiny red powder burst, then the wordmark
and endline appear.

---

## 08 · 24 HOURS
*Dramatic lighting transitions · a day compressed into sound*

**Concept.** One locked frame: a poster on a wall beside a window. A whole day passes in 13
seconds, and the light performs. A blade of dawn through the blinds, dancing leaf shadows at noon,
molten golden hour, blue hour, neon from the street, a lightning flash, then darkness and a single
lamp. The poster is the hero in every kind of light.

- **Super:** "Looks right at every hour."
- **Best with:** posters with paper or cream tones, which take light beautifully. For paid ads,
  use a design you own (see section 5).
- **Visual identity:** architectural stillness. 35 mm, locked and symmetrical, in a minimal room:
  white plaster, oak floor, one chair, a tall window with blinds on the left. One barely
  perceptible push-in (about 3% over the whole film) keeps it alive. The grade follows the light:
  cool dawn, neutral noon, amber, blue, magenta and cyan neon, then tungsten.
- **Sound identity:** a day compressed. Dawn birds, then the city at noon with distant children,
  golden-hour swifts and cicadas, a tram bell at blue hour, night rain and the buzz of a neon sign,
  thunder, silence, a lamp click. Under it, an ambient synth pad whose filter and chord colour
  change with each light, so the music changes colour too.
- **Sonic logo:** a rising blind-cord rattle for the peel; a lamp click plus a low tone for the tack.
- **How to make it with AI:** build one master room shot with the poster composited in. Generate
  each light state as its own 2–3 s clip from that same shot ("same frame, only the light
  changes"), then blend the states with light-shaped wipes. Re-pin the real artwork on every state,
  with that state's light laid over it.
- **Loop:** the film ends in darkness and begins in darkness, so the night loops into dawn.

**Hook (0:00–0:02).** Black. A blind snaps open with a rattle, and a hard blade of dawn light slices
across the wall and lands exactly on the poster. Birds burst in.

**Master shot**, generated once and reused as the start frame for every state:
```
Locked-off symmetrical 35mm shot of a minimal room: a white plaster wall with [POSTER] hanging in the centre, a tall window with horizontal blinds on the left, an oak floor and a single wooden chair. Architectural stillness, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S1 · 0:00–0:02 · Dawn Blade**
- **SFX:** a blind rattle and snap at 0:00.4, then a burst of dawn birdsong; the pad starts cool and thin.
```
Same locked frame: darkness, then the blinds snap open and a single hard blade of cool pale dawn light slices across the wall and lands across the poster; dust floats in the beam. Only the light changes, the camera and room stay identical. Photorealistic, 9:16 vertical. + POSTER LOCK
```

**S2 · 0:02–0:04.5 · Noon Leaves**
- **SFX:** a gust of wind through leaves, distant city and children; the pad brightens.
```
Same locked frame at midday: hard bright sunlight through the window casts sharp, dancing shadows of tree leaves across the white wall and the poster, moving gently in the wind. Neutral daylight colour. Only the light changes. Photorealistic, 9:16 vertical. + POSTER LOCK
```

**S3 · 0:04.5–0:07 · Golden Hour**
- **SFX:** swifts screeching overhead and a cicada swell; the pad warms into a major chord.
```
Same locked frame at golden hour: low warm amber sunlight slides diagonally across the wall and the poster, the chair's shadow stretching long across the oak floor, glowing dust in the air. Only the light changes. Photorealistic, 9:16 vertical. + POSTER LOCK
```

**S4 · 0:07–0:09 · Blue Hour**
- **SFX:** a distant tram bell, the city cooling down; the pad drops to a minor colour.
```
Same locked frame at blue hour: soft, cool deep-blue ambient light fills the room, the window glowing deep blue, the poster softly lit. Calm and still. Only the light changes. Photorealistic, 9:16 vertical. + POSTER LOCK
```

**S5 · 0:09–0:11.5 · Neon Night**
- **SFX:** rain on the window, the buzz of a neon sign, a slow synth bass pulse.
```
Same locked frame at night: magenta and cyan light from a neon sign outside spills through the window and flickers softly across the wall and the poster; shadows of raindrops running down the window glass move over the wall. Only the light changes. Photorealistic, 9:16 vertical. + POSTER LOCK
```

**S6 · 0:11.5–0:13 · Storm & Lamp**
- **Action:** a lightning white-out for 2 frames, then darkness, then a lamp clicks on and a warm
  pool of light falls on the poster.
- **SFX:** a thunder crack at 0:11.6 rolling away, silence, a lamp click at 0:12.4.
- **Super (0:12.4):** "Looks right at every hour."
```
Same locked frame at night: a flash of lightning briefly floods the room with white light, then darkness, then a small warm tungsten lamp clicks on beside the chair and casts a soft pool of golden light across the poster. Only the light changes. Photorealistic, 9:16 vertical. + POSTER LOCK
```

**S7 · 0:13–0:15 · End card (Ink background).** In the dark, the last light is a thin horizontal
stripe through the blinds. It narrows and turns red: the line.

**Music and sound timeline**

| Time | Light | Sound |
|---|---|---|
| 0:00 | Dawn | Blind snap, birds; a thin cool pad |
| 0:02 | Noon | Wind in leaves, city; the pad brightens |
| 0:04.5 | Golden hour | Swifts and cicadas; the pad warms to major |
| 0:07 | Blue hour | Tram bell; the pad drops to minor |
| 0:09 | Neon night | Rain, neon buzz, synth bass pulse |
| 0:11.6 | Lightning | Thunder, then silence |
| 0:12.4 | Lamp | Lamp click, warm room tone |
| 0:13.0 | End | Sonic logo: blind-cord rattle (peel), lamp click and low tone (tack) |

**Edit**
- **No visible cuts:** blend the light states with wipes shaped like the light itself (the blind
  blade, the leaf shadows, the neon flicker), 8–12 frames each.
- **Locked frame:** stabilise any drift between generated clips so the room never moves. The only
  movement is the slow push-in, added in the edit.
- **The poster's own colours stay true in every state:** only the light on it changes.

**Brand reveal.** The blind's light stripe narrows to a red line, then the wordmark and endline
appear on Ink.

---

## 09 · RECOLOR
*Creative room transformation · the room builds its own song*

**Concept.** A grey, lifeless room: everything desaturated, flat light, near silence. A hand
presses the first poster onto the wall, and its colours bleed out into the room like ink in water.
The light warms, the cushions blush, the flowers open. A second poster sends a new colour wave
and shifts the mood again. With the third, the room is complete. Each poster also adds a layer to
the music (beat, then bass, then melody), so the room builds its own song.

- **Super:** "Change the wall. Change the room."
- **Best with:** a set of three posters in distinct colours, such as a red, blue and green series.
- **Visual identity:** wide 24 mm, symmetrical, with a slow continuous push-in across the film. It
  starts at 0% saturation in flat overcast light. Each poster sends a colour wave outward from where
  it sits on the wall: the coloured version of the shot is revealed through an animated,
  organic-edged mask, like ink spreading in water, alongside real prop and light changes. By the
  end the room is rich, saturated and sun-warm.
- **Sound identity:** it starts muffled, mono and almost silent, with a dull hum. Poster 1 adds a
  dry percussion groove (afro-house style, 118 BPM), poster 2 adds a warm bass line, and poster 3
  adds chords and a melody (electric piano plus a plucked synth). The mix opens from mono to wide
  stereo as colour fills the room.
- **Sonic logo:** an opening filter sweep for the peel; a full chord hit for the tack.
- **No removal claim:** posters are added and never taken down (see section 6).

**Hook (0:00–0:02).** A completely grey, colourless room. The only colour in frame is a poster in a
hand entering from the right. The contrast stops the scroll. It slaps onto the wall, and colour
starts bleeding out of it.

**S1 · 0:00–0:02 · Grey**
- **Camera:** wide 24 mm, symmetrical, with the slow push beginning.
- **SFX:** a muffled mono hum, then the hand's dry slap at 0:01.6 and a rising shimmer as the colour starts.
```
Wide symmetrical 24mm shot of a dull living room rendered completely grey and colourless: flat overcast light, beige-grey sofa, grey cushions, a bare plant, closed-off mood. A hand enters from the right holding [POSTER], the only colour in the frame, and presses it onto the centre-left of the wall. Slow push-in, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S2 · 0:02–0:05 · Wave One**
- **Action:** colour floods outward from the first poster like ink in water: the lamp warms,
  cushions turn its colour, and the light becomes sunset-warm.
- **SFX:** the percussion groove kicks in on the downbeat at 0:02.0.
```
Same wide symmetrical living room: colour spreads outward from a poster on the wall like ink in water, washing across the grey room; the lamp glows warm, the cushions and a throw blanket take on the poster's main colour, sunset-warm light fills the space while the far side of the room is still grey. Slow push-in, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S3 · 0:05–0:06.5 · Poster Two**
- **Action:** a cut on the slap: the second poster goes up beside the first.
- **SFX:** the slap lands on the downbeat.

**S4 · 0:06.5–0:09 · Wave Two**
- **Action:** a second colour wave: cool window light, a throw turning the second poster's colour,
  and light rippling across the ceiling like water.
- **SFX:** the warm bass line enters.
```
Same living room, now half in colour: a second poster is pressed onto the wall beside the first, and a new wave of its colour spreads across the room like ink in water; cool light through the window, a throw blanket shifting to the new colour, soft rippling water-like reflections dancing on the ceiling. Slow push-in, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S5 · 0:09–0:10 · Poster Three**
- **SFX:** the slap on the downbeat, with a drum fill leading into it.

**S6 · 0:10–0:12.5 · Wave Three, the Full Room**
- **Action:** the last wave: plants unfurl in time-lapse, dappled leaf light spreads, and the room
  is fully alive in colour. Three posters sit side by side.
- **SFX:** chords and melody enter and the mix opens to full stereo width.
- **Super (0:11.3):** "Change the wall. Change the room."
```
Same living room, now fully transformed: a third poster joins the other two on the wall and a final wave of colour sweeps the room; houseplants unfurl and grow in time-lapse, dappled leaf light, rich saturated warm colour everywhere, the three posters side by side as the centrepiece. Slow push-in, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S7 · 0:12.5–0:13 · Whip to wide.** A fast pull to the widest frame, the whole room alive.

**S8 · 0:13–0:15 · End card (Paper background).** The line draws in the three posters' colours
side by side, then settles into Signal Red.

**Music and sound timeline (118 BPM)**

| Time | Sound |
|---|---|
| 0:00 | Muffled mono hum, near silence |
| 0:01.6 | Slap and shimmer |
| 0:02.0 | **Layer 1:** dry percussion groove |
| 0:05.0 | Slap on the downbeat |
| 0:06.5 | **Layer 2:** warm bass line; the mix begins to widen |
| 0:09.0 | Drum fill, slap |
| 0:10.0 | **Layer 3:** chords and melody; full stereo width |
| 0:13.0 | Sonic logo: filter sweep (peel), full chord hit (tack) |

**Edit**
- **Colour waves:** the ink-in-water reveal is an animated mask between a fully desaturated and a
  fully graded version of each shot. Use an organic, fluid edge, never a hard wipe.
- **Cuts:** cut only on slaps, always on the downbeat.
- **Grade:** 0% saturation at the start and rich colour at the end. The posters themselves are
  always in true colour, from the first frame.

**Brand reveal.** The line draws in the three posters' colours, then becomes red, followed by the
wordmark and endline.

---

## 10 · MAISON
*Luxury editorial · solo cello, heels, silk*

**Concept.** Filmed like a couture house's campaign: a vast, empty Parisian-style apartment with
herringbone parquet, tall double doors and plaster mouldings. Everything is black and white except
the poster, the only colour in the film. A model in a sculptural black coat and white cotton
gloves presents the poster like a couture piece, removes the liner as if unveiling a gown, and
places it on the wall with one slow, perfect gesture. The film has three chapter titles.

- **Chapters:** "I. The Paper", "II. The Gesture", "III. The Wall" (or in French: *Le Papier*,
  *Le Geste*, *Le Mur*).
- **Best with:** a colourful graphic poster, because its contrast with the black-and-white world is
  the whole film.
- **Visual identity:** silver black and white with high contrast and a soft glow on highlights. The
  poster stays in full colour, isolated in the grade. 75 mm lens, slow sideways dollies and still
  tableaux, symmetrical lines of doorways, fashion lighting (one big soft source with deep
  falloff). Chapter titles in an elegant high-contrast serif, set against the Anton end card.
- **Sound identity:** a single solo cello phrase (slow and intimate, bowed over the fingerboard for
  a soft tone), heels on parquet with a long natural reverb, the rustle of a coat, a brass door
  latch, one breath. The liner peel sounds like slowed-down silk tearing.
- **Sonic logo:** a silk tear for the peel; a low cello pizzicato for the tack.
- **How to keep the poster in colour:** generate in full colour, then track a mask over the poster
  and turn everything else black and white in the grade. Don't ask the generator for "black and
  white except the poster". It won't hold.

**Hook (0:00–0:02).** A black-and-white extreme close-up: white-gloved fingers peel back the liner
from one corner, and pure colour floods in where the liner lifts. It's the first colour in a
black-and-white world, with a silk-tearing sound.

**S1 · 0:00–0:02.5 · The Paper**
- **Camera:** extreme close-up, 100 mm macro, slow push-in.
- **SFX:** the silk tear (slowed, close), a breath; the cello's first note at 0:01.0.
- **Chapter (0:00.6):** "I. The Paper"
```
Extreme close-up, slow push-in: fingers in white cotton gloves slowly peel back the glossy backing liner from one corner of [POSTER], revealing its printed colours. Elegant fashion lighting with a large soft source and deep falloff, silver tones, soft halation on highlights, couture campaign aesthetic, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S2 · 0:02.5–0:05.5 · The Walk**
- **Camera:** wide, symmetrical, 75 mm, a slow push down a line of three open double doors.
- **Action:** the model walks toward the camera holding the poster flat against her chest like a portfolio.
- **SFX:** heels on parquet with a long reverb, the coat rustling, the cello phrase continuing.
- **Chapter (0:03.0):** "II. The Gesture"
```
Wide symmetrical shot down an enfilade of three open double doors in a vast empty Parisian apartment with herringbone parquet and ornate plaster mouldings: a model in a sculptural black wool coat and white cotton gloves walks slowly toward camera, holding [POSTER] flat against her chest like a portfolio. Slow push-in, fashion lighting, soft window light, high-contrast editorial aesthetic, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S3 · 0:05.5–0:08.5 · The Gesture**
- **Camera:** side profile, medium shot, 75 mm, slow motion (about 50 fps).
- **Action:** she places the poster on a tall panelled wall and draws her gloved palm across it in
  one slow, elegant arc.
- **SFX:** the glove's soft hush across the paper, and a quiet press.
```
Side-profile medium shot in slow motion: a model in a black sculptural coat and white cotton gloves places [POSTER] on a tall panelled wall in an elegant Parisian apartment and smooths it with one slow, graceful arc of her gloved palm. Fashion lighting with a large soft source, deep falloff, high-contrast editorial aesthetic, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S4 · 0:08.5–0:11 · The Wall**
- **Camera:** wide, symmetrical, locked.
- **Action:** she steps back and out of frame, and the poster hangs alone on the vast panelled wall
  like a piece in a museum.
- **SFX:** footsteps going away; the cello holds one long note.
- **Chapter (0:08.8):** "III. The Wall"
```
Wide symmetrical locked shot of a vast, empty Parisian apartment room with herringbone parquet and tall panelled walls; [POSTER] hangs alone in the centre of the wall like a museum piece, a model in a black coat stepping back out of frame. Soft window light, deep falloff, high-contrast editorial aesthetic, photorealistic, 9:16 vertical. + POSTER LOCK
```

**S5 · 0:11–0:13 · The Glance**
- **Camera:** medium close-up, 85 mm, in a doorway.
- **Action:** she looks back over her shoulder at the wall, then exits.
- **SFX:** a brass door latch at 0:12.4; the cello phrase resolves.
```
Medium close-up in a tall doorway of an elegant Parisian apartment: a model in a sculptural black coat glances back over her shoulder toward the room with a calm, knowing expression, then turns to leave. Fashion lighting, soft halation, high-contrast editorial aesthetic, photorealistic, 9:16 vertical.
```

**S6 · 0:13–0:15 · End card (Ink background).** Still black and white. The red line is the second
colour in the whole film.

**Music and sound timeline**

| Time | Sound |
|---|---|
| 0:00 | Silk tear, breath |
| 0:01.0 | Solo cello enters (one slow phrase, bowed softly) |
| 0:02.5 | Heels on parquet, long reverb; coat rustle |
| 0:05.5 | Gloved palm across paper, soft press |
| 0:08.5 | Footsteps going away; cello holds a long note |
| 0:12.4 | Brass door latch; the cello resolves |
| 0:13.0 | Sonic logo: silk tear (peel), low cello pizzicato (tack) |

**Edit**
- **Pace:** few cuts, each shot allowed to breathe. Dissolve between chapters (10 frames).
- **Chapter titles:** small, centred in the upper third, fading in over 8 frames and out over 8.
- **Grade:** silver black and white with gentle highlight glow and rich mid-greys. The poster is
  tracked and kept in true colour in every shot.

**Brand reveal.** Black and white throughout, then the red line draws in, the first new colour
since the poster.

---

## Production order and testing

**Make these first.** They're cheap, shot on a phone, and show your real product:
1. **06 PERFECT FIT:** a phone, a tripod, a tiled wall, an afternoon.
2. **01 MICRON:** a phone in macro mode or a clip-on macro lens, one LED, a black cloth.
3. **05 THE MOVE-IN:** a phone, a tripod, a stop-motion app, a weekend.

**Then the AI-heavy films:** 08, 09, 03, 04, 07, 02 and 10, using the composite and tracking
workflow in section 1.

**Deliver from each film:**
- the 15 s master
- a 6 s cut-down: the hook plus the end card
- a still frame for the cover or thumbnail

**Testing:**
- **Run in batches:** 3–4 films at a time, each with the same budget.
- **Judge the hook by the 3-second view rate.** Low means the first 2 seconds aren't working.
- **Judge the ad by the click-through rate.**
- **Keep the winners** and build the next versions around their hooks.
