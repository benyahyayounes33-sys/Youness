# Quality-control and rights report: 30 uploaded images

_Measured on 15/11/2026 with Python (Pillow + NumPy). Labels: ✅ fact · 🔶 assumption or judgement · ❌ not suitable._

## 1. Summary

| Question | Answer |
|---|---|
| How many files reach **300 DPI** at A5, A4 or A3? | **0 of 30** |
| How many reach even the **150 DPI** minimum at A5? | **0 of 30** (best: 126 DPI at A5) |
| Why? | Every file is **609–736 px wide**. 736 px is the standard Pinterest preview width ✅: these are previews, not originals. |
| How many can be **sold legally** as they are? | **0 of 30**. 29 contain someone else’s copyright, trademarks or likeness. The 30th (Mona Lisa) shows a public-domain painting, but the file is another designer’s layout. |
| What was produced? | A legal **“Chefs-d’œuvre” series of 6 posters** (public-domain masterpieces, high-resolution sources): A5 / A4 / A3, trim size + 3 mm bleed = **36 PDFs, all verified at 300 DPI**. See section 4. |

## 2. Image by image

DPI = effective resolution if the image fills the page (cover fit). Fit loss = % of the image cut off to match A proportions (1 : 1.414). JPEG q = estimated JPEG quality. Blocking > 1.2 = visible 8×8 compression blocks.

| # | File | Subject | Pixels | Fit loss | JPEG q / blocking | DPI A5 / A4 / A3 | Print verdict | Rights and trademarks (main problems) | Sell? |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 157540.jpg | Porsche (ink splash) | 736×1472 | 29.3% | 89 / 1.1 | 126 / 89 / 63 | ❌ not even A5 | Porsche crest + wordmark (Porsche trademarks). Signed **“© ArkosPC.2025. Tous droits réservés”** + APC logo: the designer explicitly reserves all rights. | ❌ needs licences |
| 2 | 157538.jpg | Porsche 911 GT3 RS green | 736×1307 | 20.4% | 89 / 1.28 | 126 / 89 / 63 | ❌ not even A5 | Porsche crest + wordmark, “911 GT3 RS”. Car photo (owner unknown). Designer signature **“D.M”**. | ❌ needs licences |
| 3 | 157535.jpg | Porsche 911 GT3RS yellow | 736×1044 | 0.3% | 80 / 1.12 | 126 / 89 / 63 | ❌ not even A5 | Porsche crest + wordmark, “911 GT3RS”. Car photos (owner unknown, likely press photos). | ❌ needs licences |
| 4 | 157537.jpg | Porsche 911 GT3 black | 735×1044 | 0.4% | 80 / 1.14 | 126 / 89 / 63 | ❌ not even A5 | Porsche crest + logotype. Car photo (owner unknown, likely dealer/press). | ❌ needs licences |
| 5 | 157536.jpg | Porsche 992 GT3 RS silver | 736×1060 | 1.8% | 89 / 1.37 | 126 / 89 / 63 | ❌ not even A5 | Porsche logotype, “992 GT3 RS”. Car image. The ✦ mark in the corner looks like the visible watermark some AI image tools add 🔶. | ❌ needs licences |
| 6 | 157390.jpg | Luffy Gear 5 emblem | 736×1104 | 5.7% | 80 / 1.04 | 126 / 89 / 63 | ❌ not even A5 | One Piece: Luffy Gear 5 + Straw Hat Jolly Roger (Eiichiro Oda / Shueisha / Toei Animation). | ❌ needs licences |
| 7 | 157391.jpg | Solo Leveling – Shadow Monarch | 736×1308 | 20.4% | 80 / 1.05 | 126 / 89 / 63 | ❌ not even A5 | Solo Leveling characters + quote (webtoon and anime rights holders). | ❌ needs licences |
| 8 | 157392.jpg | Luffy Gear 5 streetwear | 736×1308 | 20.4% | 89 / 1.07 | 126 / 89 / 63 | ❌ not even A5 | One Piece: Luffy. “NIKA” shoe imitating Nike’s swoosh (Nike trademark). | ❌ needs licences |
| 9 | 157260.jpg | Porsche 911 GT3 blue (Manthey) | 736×920 | 11.6% | 80 / 0.89 | 111 / 79 / 56 | ❌ not even A5 | Porsche crest + wordmark, “911 GT3 (992.2)”, Manthey logos. Car images (owner unknown). | ❌ needs licences |
| 10 | 157258.jpg | Porsche GT3 RS Manthey light blue | 736×981 | 5.8% | 89 / 1.43 | 119 / 84 / 59 | ❌ not even A5 | Porsche + Manthey logos, “GT3 RS”. Car photo (owner unknown). Small designer mark at the bottom. | ❌ needs licences |
| 11 | 157257.jpg | Venom | 736×1313 | 20.7% | 89 / 1.1 | 126 / 89 / 63 | ❌ not even A5 | Venom: Marvel character. | ❌ needs licences |
| 12 | 157259.jpg | Porsche 911 teal collage | 736×1308 | 20.4% | 89 / 1.21 | 126 / 89 / 63 | ❌ not even A5 | Porsche crest + wordmarks, model names. Another designer’s collage. | ❌ needs licences |
| 13 | 157261.jpg | Mona Lisa | 736×1041 | 0.0% | 80 / 1.12 | 126 / 89 / 63 | ❌ not even A5 | **Painting = public domain ✅** (Leonardo da Vinci died 1519). But this file is another designer’s layout + a journalist’s quote, and it is low resolution. | ⚠️ rebuilt legally (see §4) |
| 14 | 157255.jpg | Messi – Argentina 2026 | 736×1204 | 13.5% | 89 / 1.25 | 126 / 89 / 63 | ❌ not even A5 | Lionel Messi’s likeness (image rights). AFA crest, FIFA World Cup trophy emblem, Adidas marks. | ❌ needs licences |
| 15 | 157256.jpg | Messi – smoke | 735×1315 | 21.0% | 89 / 1.13 | 126 / 89 / 63 | ❌ not even A5 | Lionel Messi’s likeness (image rights). Designer signature. AFA/Adidas on the shirt. | ❌ needs licences |
| 16 | 157251.jpg | Dodge Viper GT | 736×920 | 11.6% | 80 / 1.09 | 111 / 79 / 56 | ❌ not even A5 | “Viper GT” (Dodge / Stellantis trademark). Designer mark **“OnTheRun Automotive Design”**. Car photos. | ❌ needs licences |
| 17 | 157254.jpg | BLUR magazine | 736×981 | 5.8% | 89 / 1.23 | 119 / 84 / 59 | ❌ not even A5 | Photo of a real person (photographer’s copyright + model’s image rights). Another designer’s magazine-style layout. | ❌ needs licences |
| 18 | 157252.jpg | UNSEEN 007 | 736×1041 | 0.0% | 89 / 1.23 | 126 / 89 / 63 | ❌ not even A5 | Designer signature **“@VIREAKRITH108”**. “007” (James Bond trademark). Photo (owner unknown). | ❌ needs licences |
| 19 | 157195.jpg | Billie Eilish collage | 736×1104 | 5.7% | 80 / 1.18 | 126 / 89 / 63 | ❌ not even A5 | Photos of Billie Eilish (photographers’ copyright + her image rights). | ❌ needs licences |
| 20 | 157199.jpg | Porsche GT3 RS black | 736×915 | 12.1% | 89 / 1.19 | 111 / 78 / 55 | ❌ not even A5 | Porsche wordmark, “GT3 RS”. Designer mark **“ABC.DESIGN”**. Text copied from a press article. | ❌ needs licences |
| 21 | 156460.jpg | Porsche GT3 RS yellow (rear) | 736×1150 | 9.5% | 89 / 1.22 | 126 / 89 / 63 | ❌ not even A5 | Porsche crest + wordmark, “911 GT3 RS”. Car image (owner unknown). | ❌ needs licences |
| 22 | 156435.jpg | Iron Man | 609×913 | 5.7% | 80 / 1.14 | 105 / 74 / 52 | ❌ not even A5 | *Iron Man* film still (Marvel / Disney). Robert Downey Jr.’s likeness. | ❌ needs licences |
| 23 | 156430.jpg | The Queen's Gambit | 736×1104 | 5.7% | 80 / 1.05 | 126 / 89 / 63 | ❌ not even A5 | *The Queen’s Gambit* still (Netflix). Anya Taylor-Joy’s likeness. | ❌ needs licences |
| 24 | 156426.jpg | Peaky Blinders | 661×991 | 5.7% | 80 / 0.94 | 113 / 80 / 57 | ❌ not even A5 | *Peaky Blinders* still (BBC). Cillian Murphy’s likeness. | ❌ needs licences |
| 25 | 156424.jpg | The Godfather – Great Men | 736×981 | 5.8% | 89 / 1.13 | 119 / 84 / 59 | ❌ not even A5 | *The Godfather* still (Paramount). Marlon Brando’s likeness. Designer signature **“@AKOTSK.AR”**. | ❌ needs licences |
| 26 | 156437.jpg | Solo Leveling – The Movie | 735×1041 | 0.1% | 89 / 1.33 | 126 / 89 / 63 | ❌ not even A5 | *Solo Leveling* movie poster with A-1 Pictures + Crunchyroll logos. | ❌ needs licences |
| 27 | 156436.jpg | Luffy – red | 736×1169 | 11.0% | 80 / 1.22 | 126 / 89 / 63 | ❌ not even A5 | One Piece: Luffy (Oda / Shueisha) drawn by a fan artist (also their copyright). | ❌ needs licences |
| 28 | 156421.jpg | The Dark Knight | 735×1040 | 0.1% | 89 / 1.13 | 126 / 89 / 63 | ❌ not even A5 | *The Dark Knight* stills (Warner Bros. / DC), Batman logo, actors’ likenesses, film quote. | ❌ needs licences |
| 29 | 156464.jpg | Billie Eilish – Happier Than Ever | 735×1040 | 0.1% | 80 / 1.15 | 126 / 89 / 63 | ❌ not even A5 | Billie Eilish *Happier Than Ever* album photo, lyrics and tracklist. | ❌ needs licences |
| 30 | 156461.jpg | Mercedes-AMG GT Black Series | 736×1307 | 20.4% | 89 / 1.22 | 126 / 89 / 63 | ❌ not even A5 | Mercedes star, AMG + Affalterbach logos (Mercedes-Benz trademarks). Car photos (owner unknown). | ❌ needs licences |

**Reading the numbers 🔶 (print-industry rules of thumb):** 300 DPI = sharp up close · 200 = good · 150 = minimum for a wall poster seen from 1 m · below 150 = visibly soft or pixelated. Phone-wallpaper formats (9:16, fit loss ≈ 20%) also lose part of the design when cut to A size: text and logos at the edges get cropped.

## 3. What I did NOT do, and why

| Requested step | Done? | Reason |
|---|---|---|
| Analyse every image | ✅ | Section 2. |
| AI upscaling to A4/A3 | ❌ | Going from 736 px to 3508 px (A3) means **inventing about 95% of the pixels**. That contradicts your own rule “do not create fake details”: faces, emblem lettering and fine text would be made up. And upscaling changes nothing about who owns the image. |
| Print-ready PDFs of images 1–12 and 14–30 | ❌ | You plan to sell them. They contain other designers’ signed work (ArkosPC “Tous droits réservés”, D.M, ABC.DESIGN, OnTheRun, @VIREAKRITH108, @AKOTSK.AR…), Porsche / Mercedes / Dodge / Nike trademarks, film studios’ stills, and real people’s faces. Making sale files would mean producing counterfeit goods, which is also exactly what you asked me to avoid. |
| PDF/X-4 + CMYK | ⏸ | Needs your print shop’s output profile (you were right not to want blind conversion). The PDFs are sRGB, which digital print shops generally accept 🔶. Send me the shop’s profile name and I’ll convert. |
| Adhesive versions | ✅ same files | Adhesive paper uses the same artwork. See `06 ADHESIVE PRINT FILES/README.md`. |

**If one of these designs is actually yours** (you made it from scratch), tell me which one and send me the original high-resolution file (not a Pinterest download). I’ll process it, after removing any brand logos, names or real people’s faces.

## 4. Produced: the “Chefs-d’œuvre” series (Collection 01)

Each poster is built from a **high-resolution source of a public-domain work** (the Mona Lisa replaces your Pinterest file #13). All sources are larger than the A3 artwork needs, so everything is **downsampled only**: no upscaling, no AI, no invented detail.

| Poster | Artist (copyright basis) | Source (Wikimedia Commons, 3840 px standard rendition) | Source px | Colour | Note |
|---|---|---|---|---|---|
| MONA-LISA | Leonardo da Vinci, died 1519 ✅ | Wikimedia Commons, 'Mona Lisa, by Leonardo da Vinci, from C2RMF retouched.jpg', 3840 px standard rendition (https://commons.wikimedia.org/wiki/File:Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg) | 3840×5723 | no embedded profile - treated as sRGB |  |
| STARRY-NIGHT | Vincent van Gogh, died 1890 ✅ | Wikimedia Commons 'Van Gogh - Starry Night - Google Art Project.jpg', 3840 px standard rendition (https://commons.wikimedia.org/wiki/File:Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg) | 3759×3016 | no embedded profile - treated as sRGB |  |
| THE-KISS | Gustav Klimt, died 1918 ✅ | Wikimedia Commons 'The Kiss - Gustav Klimt - Google Cultural Institute.jpg', 3840 px standard rendition (https://commons.wikimedia.org/wiki/File:The_Kiss_-_Gustav_Klimt_-_Google_Cultural_Institute.jpg) | 3840×3853 | no embedded profile - treated as sRGB |  |
| GREAT-WAVE | Katsushika Hokusai, died 1849 ✅ | Wikimedia Commons 'Great Wave off Kanagawa2.jpg', 3840 px standard rendition (https://commons.wikimedia.org/wiki/File:Great_Wave_off_Kanagawa2.jpg) | 3840×2628 | no embedded profile - treated as sRGB |  |
| PEARL-EARRING | Johannes Vermeer, died 1675 ✅ | Wikimedia Commons '1665 Girl with a Pearl Earring.jpg', 3840 px standard rendition (https://commons.wikimedia.org/wiki/File:1665_Girl_with_a_Pearl_Earring.jpg) | 3840×4548 | embedded ICC profile converted to sRGB |  |
| IMPRESSION-SUNRISE | Claude Monet, died 1926 ✅ | Wikimedia Commons 'Monet - Impression, Sunrise.jpg', 3840 px standard rendition (https://commons.wikimedia.org/wiki/File:Monet_-_Impression,_Sunrise.jpg) | 3840×2979 | embedded ICC profile converted to sRGB |  |

- **Rights:** each artist died more than 70 years ago, so the works are in the public domain in Morocco (copyright = life + 70 years ✅). The digital files are faithful photographic reproductions of these works. Many countries treat such reproductions as public domain; Moroccan law has no clear position on this type of photo 🔶. Low risk, but not zero.
- **Not mentioned on the posters:** museum names (the Louvre, MoMA, the Belvedere… protect their names as trademarks 🔶).
- **Processing (identical for all):** Lanczos downsampling to exactly 300 DPI at printed size; UnsharpMask radius 0.8 px, 45 %, threshold 2 (output sharpening for print). No colour, contrast or content changes. No upscaling, no AI generation.
- **Layout:** original minimalist museum design (not copied from any Pinterest layout). English title + French title and details. 5 colour swatches sampled from each painting. Font: Inter (SIL Open Font License ✅). No logo or watermark. Text = facts only (title, artist, date, medium, dimensions).

### Checks run on every PDF (read back from the finished files)

| File | Page (mm) | Embedded image (px) | Effective DPI | Proportions | Re-compression | Safe zone | Result |
|---|---|---|---|---|---|---|---|
| MONA-LISA_A5_300DPI_PRINT.pdf | 148.0 × 210.0 | 1145×1706 | 299.9 | kept | none | ok | ✅ PASS |
| MONA-LISA_A5_300DPI_PRINT_BLEED3MM.pdf | 154.0 × 216.0 | 1145×1706 | 299.9 | kept | none | ok | ✅ PASS |
| MONA-LISA_A4_300DPI_PRINT.pdf | 210.0 × 297.0 | 1625×2421 | 300.0 | kept | none | ok | ✅ PASS |
| MONA-LISA_A4_300DPI_PRINT_BLEED3MM.pdf | 216.0 × 303.0 | 1625×2421 | 300.0 | kept | none | ok | ✅ PASS |
| MONA-LISA_A3_300DPI_PRINT.pdf | 297.0 × 420.0 | 2298×3424 | 300.0 | kept | none | ok | ✅ PASS |
| MONA-LISA_A3_300DPI_PRINT_BLEED3MM.pdf | 303.0 × 426.0 | 2298×3424 | 300.0 | kept | none | ok | ✅ PASS |
| STARRY-NIGHT_A5_300DPI_PRINT.pdf | 148.0 × 210.0 | 1515×1216 | 300.0 | kept | none | ok | ✅ PASS |
| STARRY-NIGHT_A5_300DPI_PRINT_BLEED3MM.pdf | 154.0 × 216.0 | 1515×1216 | 300.0 | kept | none | ok | ✅ PASS |
| STARRY-NIGHT_A4_300DPI_PRINT.pdf | 210.0 × 297.0 | 2150×1725 | 300.0 | kept | none | ok | ✅ PASS |
| STARRY-NIGHT_A4_300DPI_PRINT_BLEED3MM.pdf | 216.0 × 303.0 | 2150×1725 | 300.0 | kept | none | ok | ✅ PASS |
| STARRY-NIGHT_A3_300DPI_PRINT.pdf | 297.0 × 420.0 | 3040×2439 | 300.0 | kept | none | ok | ✅ PASS |
| STARRY-NIGHT_A3_300DPI_PRINT_BLEED3MM.pdf | 303.0 × 426.0 | 3040×2439 | 300.0 | kept | none | ok | ✅ PASS |
| THE-KISS_A5_300DPI_PRINT.pdf | 148.0 × 210.0 | 1415×1420 | 300.0 | kept | none | ok | ✅ PASS |
| THE-KISS_A5_300DPI_PRINT_BLEED3MM.pdf | 154.0 × 216.0 | 1415×1420 | 300.0 | kept | none | ok | ✅ PASS |
| THE-KISS_A4_300DPI_PRINT.pdf | 210.0 × 297.0 | 2008×2015 | 300.0 | kept | none | ok | ✅ PASS |
| THE-KISS_A4_300DPI_PRINT_BLEED3MM.pdf | 216.0 × 303.0 | 2008×2015 | 300.0 | kept | none | ok | ✅ PASS |
| THE-KISS_A3_300DPI_PRINT.pdf | 297.0 × 420.0 | 2840×2849 | 300.0 | kept | none | ok | ✅ PASS |
| THE-KISS_A3_300DPI_PRINT_BLEED3MM.pdf | 303.0 × 426.0 | 2840×2849 | 300.0 | kept | none | ok | ✅ PASS |
| GREAT-WAVE_A5_300DPI_PRINT.pdf | 148.0 × 210.0 | 1515×1037 | 300.0 | kept | none | ok | ✅ PASS |
| GREAT-WAVE_A5_300DPI_PRINT_BLEED3MM.pdf | 154.0 × 216.0 | 1515×1037 | 300.0 | kept | none | ok | ✅ PASS |
| GREAT-WAVE_A4_300DPI_PRINT.pdf | 210.0 × 297.0 | 2150×1471 | 300.0 | kept | none | ok | ✅ PASS |
| GREAT-WAVE_A4_300DPI_PRINT_BLEED3MM.pdf | 216.0 × 303.0 | 2150×1471 | 300.0 | kept | none | ok | ✅ PASS |
| GREAT-WAVE_A3_300DPI_PRINT.pdf | 297.0 × 420.0 | 3040×2081 | 300.0 | kept | none | ok | ✅ PASS |
| GREAT-WAVE_A3_300DPI_PRINT_BLEED3MM.pdf | 303.0 × 426.0 | 3040×2081 | 300.0 | kept | none | ok | ✅ PASS |
| PEARL-EARRING_A5_300DPI_PRINT.pdf | 148.0 × 210.0 | 1282×1518 | 300.0 | kept | none | ok | ✅ PASS |
| PEARL-EARRING_A5_300DPI_PRINT_BLEED3MM.pdf | 154.0 × 216.0 | 1282×1518 | 300.0 | kept | none | ok | ✅ PASS |
| PEARL-EARRING_A4_300DPI_PRINT.pdf | 210.0 × 297.0 | 1819×2154 | 300.0 | kept | none | ok | ✅ PASS |
| PEARL-EARRING_A4_300DPI_PRINT_BLEED3MM.pdf | 216.0 × 303.0 | 1819×2154 | 300.0 | kept | none | ok | ✅ PASS |
| PEARL-EARRING_A3_300DPI_PRINT.pdf | 297.0 × 420.0 | 2572×3047 | 299.9 | kept | none | ok | ✅ PASS |
| PEARL-EARRING_A3_300DPI_PRINT_BLEED3MM.pdf | 303.0 × 426.0 | 2572×3047 | 299.9 | kept | none | ok | ✅ PASS |
| IMPRESSION-SUNRISE_A5_300DPI_PRINT.pdf | 148.0 × 210.0 | 1515×1175 | 299.9 | kept | none | ok | ✅ PASS |
| IMPRESSION-SUNRISE_A5_300DPI_PRINT_BLEED3MM.pdf | 154.0 × 216.0 | 1515×1175 | 299.9 | kept | none | ok | ✅ PASS |
| IMPRESSION-SUNRISE_A4_300DPI_PRINT.pdf | 210.0 × 297.0 | 2150×1668 | 300.1 | kept | none | ok | ✅ PASS |
| IMPRESSION-SUNRISE_A4_300DPI_PRINT_BLEED3MM.pdf | 216.0 × 303.0 | 2150×1668 | 300.1 | kept | none | ok | ✅ PASS |
| IMPRESSION-SUNRISE_A3_300DPI_PRINT.pdf | 297.0 × 420.0 | 3040×2358 | 299.9 | kept | none | ok | ✅ PASS |
| IMPRESSION-SUNRISE_A3_300DPI_PRINT_BLEED3MM.pdf | 303.0 × 426.0 | 3040×2358 | 299.9 | kept | none | ok | ✅ PASS |

Visual check: real paint detail at 100% (cracks, brushstrokes, gold leaf), no halos or artificial texture. Comparison: `07 PREVIEW IMAGES/WHY-SOURCE-RESOLUTION-MATTERS_A3_100pct.png`.

**Before selling:** print **one A4** of the darkest poster (Girl with a Pearl Earring or The Starry Night) at your chosen shop and check it against the test-sheet checklist. Dark backgrounds are the first thing a poor print ruins.

## 5. Legal alternatives for the themes you like

| Your images | Legal route |
|---|---|
| Porsche / Mercedes / Viper (12 images) | Original designs of **fictional cars** with no badges or model names (designs #1–#4 in the launch plan). The brands’ official licensing is not realistic at your size 🔶. |
| Anime (5 images) | No unlicensed fan art for sale. Make your own **original characters / universe** if you draw, or skip this category. |
| Films, series and Venom (6 images) | **Fake film posters** for films that don’t exist (designs #5–#6), or classic films whose rights have expired. Check each one: a film’s copyright and its actors’ likeness are separate questions 🔶. |
| Music artists (2 images) | Instruments, eras, invented tracklists (design #7). No photos of artists and no lyrics. |
| Football (2 images) | Custom tactics board, Moroccan colours, no crests or players (design #8). |
| Art (Mona Lisa) | ✅ **Done: “Chefs-d’œuvre” Collection 01, 6 posters** (section 4). For more: same method, after checking the artist’s date of death (life + 70 years ✅). |
