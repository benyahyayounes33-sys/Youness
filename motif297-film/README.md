# MOTIF 297 — Brand Film: "Walls With a Point of View"

A 28-second vertical brand film for MOTIF 297 (premium A4 adhesive art posters), built from the
seven supplied poster designs, with an original score and sound design.

## Deliverables (`deliverables/`)

| # | File | What it is |
|---|---|---|
| 1 | `MOTIF297_BrandFilm_9x16_Master.mp4` | **Final film.** 1080×1920, 30 fps, H.264 High (CRF 17), AAC 320 kb/s, BT.709. |
| 2 | `MOTIF297_BrandFilm_9x16_Clean_NoText.mp4` | Textless version: no typography, no tags, no wordmark (graphic lines kept) for re-versioning. |
| 3 | `MOTIF297_BrandFilm_9x16_Captions.mp4` + `MOTIF297_BrandFilm_Captions_SDH.srt` | Burned-in SDH captions (the film has no dialogue, so captions describe sound), plus a sidecar SRT for platform upload. |
| 4 | `audio/MOTIF297_Mix_Stereo_48k24.wav`, `audio/MOTIF297_Stem_Music_48k24.wav`, `audio/MOTIF297_Stem_SFX_48k24.wav` | Full mix plus music and SFX stems (24-bit / 48 kHz). The stems sum exactly to the mix. −14.0 LUFS, −1.2 dBTP. |
| 5 | `timeline/MOTIF297_cue_sheet.md`, `timeline/MOTIF297_timeline.json` + `src/` | Edit decision list / cue sheet with timecodes, transitions and sound cues. The `src/` scripts are the procedural project: they re-render everything bit-for-bit. |
| 6 | `MOTIF297_Thumbnail_1080x1920.jpg`, `MOTIF297_Thumbnail_GridCrop_1080x1440.jpg` | Cover frame, plus a 3:4 crop for the profile grid. |

Docs: `docs/CREATIVE_TREATMENT.md` (concept, structure, transitions, sound, QC review, limitations) ·
`docs/FILMING_PLAN.md` (the live-action shots that don't exist yet, with exact slots in this edit, and a rights note).

## Things to know before publishing

- **The wordmark is a placeholder.** No MOTIF 297 logo file was supplied, so the end card sets "MOTIF / 297" in Jost. Swap in the official logo in the end card when it's available.
- **Collection tags are placeholders** (ART / AUTOMOTIVE / SPORT / CINEMA). Replace them with real collection names in `text_layer()`.
- **No physical-product footage existed**, so the film shows the designs (never redrawn or altered) through a virtual camera and a virtual wall. Real macro, hands, adhesive peel and wall shots are planned in `docs/FILMING_PLAN.md`.
- **The source files are ~700 px wide.** The 1080p master holds up, but there's no 4K master: the sources don't support one.
- **Rights.** The designs include third-party trademarks, a real athlete's likeness, a TV series and other designers' credits. Check the rights before using the film as paid advertising.

## Re-render

```bash
pip install opencv-python-headless scipy numpy pillow
cd src
python3 film.py        # picture: master, clean, captions (≈20 min on 4 cores)
python3 audio.py       # score + SFX + mastering
python3 package.py     # SRT, timeline, thumbnail, audio mux
python3 film.py stills 0 18 594 762   # QC stills (STILLS=/path env var)
```

Fonts: Jost (SIL Open Font License, `assets/fonts/JOST_OFL_LICENSE.txt`).
