"""Build print-ready poster PDFs (A5 / A4 / A3, trim size + optional 3 mm bleed) from ONE high-resolution
artwork that you have the right to sell (your own design, a licensed image, or a public-domain work).

What it does, honestly:
  * colour-manages the source to sRGB (if it carries an ICC profile)
  * DOWNSAMPLES the artwork to exactly 300 DPI at its printed size (Lanczos) + light output sharpening
  * refuses to upscale: if the source is too small for a size, that size is skipped and reported
  * lays out a minimalist museum-style poster with vector text (Inter, SIL Open Font License)
  * writes trim-size PDFs and separate +3 mm bleed PDFs, embeds the JPEG without re-compressing it
  * verifies every PDF (page size, effective DPI of the embedded image, no recompression) -> qc.json

Usage:  python3 make_art_print.py spec.json
"""
import json, os, sys, shutil, subprocess
import numpy as np
from PIL import Image, ImageCms, ImageFilter
from reportlab import rl_config
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

Image.MAX_IMAGE_PIXELS = 300_000_000
rl_config.useA85 = 0  # embed JPEG bytes as-is (no ASCII85 wrapper)
SIZES = {"A5": (148, 210), "A4": (210, 297), "A3": (297, 420)}
DPI = 300
BLEED = 3  # mm, only for the *_BLEED3MM files


def mm2px(v):
    return int(round(v / 25.4 * DPI))


def load_srgb(path):
    im = Image.open(path)
    icc = im.info.get("icc_profile")
    im = im.convert("RGB") if im.mode not in ("RGB",) else im
    note = "no embedded profile - treated as sRGB"
    if icc:
        import io
        src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
        im = ImageCms.profileToProfile(im, src, ImageCms.createProfile("sRGB"), outputMode="RGB",
                                       renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC)
        note = "embedded ICC profile converted to sRGB (relative colorimetric)"
    return im, note


def swatches(im, k=5, seed=0):
    small = np.asarray(im.resize((160, int(160 * im.height / im.width)), Image.LANCZOS), float).reshape(-1, 3)
    lum = small @ [0.299, 0.587, 0.114]
    centers = np.array([small[(lum >= np.quantile(lum, q0)) & (lum <= np.quantile(lum, q1))].mean(0)
                        for q0, q1 in zip(np.linspace(0, .8, k), np.linspace(.2, 1, k))])
    for _ in range(25):
        lab = ((small[:, None, :] - centers[None]) ** 2).sum(-1).argmin(1)
        centers = np.array([small[lab == i].mean(0) if (lab == i).any() else centers[i] for i in range(k)])
    centers = centers[np.argsort(centers @ [0.299, 0.587, 0.114])]
    return ["#%02X%02X%02X" % tuple(int(round(c)) for c in col) for col in centers]


def layout(W, H, art_ratio):
    """All values in mm, measured from the TOP-LEFT of the trim box. Scales with the A-series."""
    s = W / 210.0
    top, max_h, max_w = 18 * s, 205 * s, W - 2 * 28 * s
    ah = min(max_h, max_w * art_ratio)
    aw = ah / art_ratio
    L = {"s": s, "art": ((W - aw) / 2, top, aw, ah)}
    y = top + ah + 12 * s
    L["title"] = (y + 40 * s * 0.3528 * 0.73, max(14, 40 * s))       # baseline, font size pt
    L["subtitle"] = (L["title"][0] + 7 * s, max(6.5, 9.5 * s))
    L["details"] = (L["subtitle"][0] + 5.5 * s, max(5.5, 7 * s))
    L["sw_top"], L["sw"], L["sw_gap"] = L["details"][0] + 8 * s, 6 * s, 2.5 * s
    L["bottom_used"] = L["sw_top"] + L["sw"]
    return L


def centered(c, text, font, size, x_mid, y, char_space=0.0):
    width = pdfmetrics.stringWidth(text, font, size) + char_space * (len(text) - 1)
    t = c.beginText()
    t.setFont(font, size)
    t.setCharSpace(char_space)
    t.setTextOrigin(x_mid - width / 2, y)
    t.textLine(text)
    c.drawText(t)


def build_pdf(path, size_name, art_jpg, art_ratio, spec, palette, bleed):
    W, H = SIZES[size_name]
    off = BLEED if bleed else 0
    PW, PH = W + 2 * off, H + 2 * off
    c = canvas.Canvas(path, pagesize=(PW * mm, PH * mm), pageCompression=1)
    c.setTitle(f'{spec["title"]} - {size_name} - 300 DPI print' + (" (3 mm bleed)" if bleed else ""))
    c.setCreator("make_art_print.py")
    L = layout(W, H, art_ratio)
    s = L["s"]
    X = lambda v: (off + v) * mm
    Y = lambda v: (off + H - v) * mm  # v = mm from top of trim
    c.setFillColor(HexColor(spec["background"]))
    c.rect(0, 0, PW * mm, PH * mm, stroke=0, fill=1)
    ax, ay, aw, ah = L["art"]
    c.drawImage(art_jpg, X(ax), Y(ay + ah), aw * mm, ah * mm)
    c.setFillColor(HexColor(spec["ink"]))
    mid = (off + W / 2) * mm
    centered(c, spec["title"], "InterDisplay-Bold", L["title"][1], mid, Y(L["title"][0]), 1.5 * s)
    centered(c, spec["subtitle"], "Inter-Medium", L["subtitle"][1], mid, Y(L["subtitle"][0]), 1.6 * s)
    centered(c, spec["details"], "Inter-Regular", L["details"][1], mid, Y(L["details"][0]), 0.9 * s)
    n = len(palette)
    total = n * L["sw"] + (n - 1) * L["sw_gap"]
    x0 = W / 2 - total / 2
    for i, col in enumerate(palette):
        c.setFillColor(HexColor(col))
        c.rect(X(x0 + i * (L["sw"] + L["sw_gap"])), Y(L["sw_top"] + L["sw"]), L["sw"] * mm, L["sw"] * mm, stroke=0, fill=1)
    c.showPage()
    c.save()
    return L


def verify(pdf_path, size_name, bleed, L, art_px, art_file):
    from pypdf import PdfReader
    W, H = SIZES[size_name]
    off = BLEED if bleed else 0
    r = PdfReader(pdf_path)
    page = r.pages[0]
    pw = float(page.mediabox.width) / 72 * 25.4
    ph = float(page.mediabox.height) / 72 * 25.4
    imgs = []
    for name, obj in page["/Resources"]["/XObject"].items():
        o = obj.get_object()
        if o.get("/Subtype") == "/Image":
            imgs.append((int(o["/Width"]), int(o["/Height"]), str(o.get("/Filter")), len(o._data)))
    iw, ih, filt, nbytes = imgs[0]
    ax, ay, aw, ah = L["art"]
    dpi_w, dpi_h = iw / (aw / 25.4), ih / (ah / 25.4)
    checks = {
        "page_mm": [round(pw, 2), round(ph, 2)],
        "expected_mm": [W + 2 * off, H + 2 * off],
        "page_size_ok": abs(pw - (W + 2 * off)) < 0.1 and abs(ph - (H + 2 * off)) < 0.1,
        "image_px": [iw, ih],
        "effective_dpi": round(min(dpi_w, dpi_h), 1),
        "dpi_ok": min(dpi_w, dpi_h) >= 299.5,
        "aspect_preserved": abs((ih / iw) - (ah / aw)) < 0.002,
        "embedded_as": filt,
        "no_recompression": filt.strip("[]'") == "/DCTDecode" and nbytes == os.path.getsize(art_file),
        "content_inside_safe_zone": L["bottom_used"] <= H - 5 and L["art"][1] >= 5,
        "pages": len(r.pages),
    }
    checks["PASS"] = all(v for k, v in checks.items() if k.endswith("_ok") or k in (
        "aspect_preserved", "no_recompression", "content_inside_safe_zone"))
    return checks


def main(spec_path):
    spec = json.load(open(spec_path))
    root = spec["out_dir"]
    slug = spec["slug"]
    for n in ("InterDisplay-Bold", "Inter-Medium", "Inter-Regular"):
        pdfmetrics.registerFont(TTFont(n, os.path.join(spec["font_dir"], n + ".ttf")))
    folders = {k: os.path.join(root, v) for k, v in {
        "orig": "01 ORIGINAL IMAGES", "enh": "02 ENHANCED IMAGES", "A5": "03 A5 PRINT READY PDF",
        "A4": "04 A4 PRINT READY PDF", "A3": "05 A3 PRINT READY PDF", "adh": "06 ADHESIVE PRINT FILES",
        "prev": "07 PREVIEW IMAGES", "qc": "08 QUALITY CONTROL REPORT"}.items()}
    for f in folders.values():
        os.makedirs(f, exist_ok=True)

    im, colour_note = load_srgb(spec["source"])
    if spec.get("crop"):  # fractions l, t, r, b
        l, t, r_, b = spec["crop"]
        im = im.crop((int(l * im.width), int(t * im.height), int(r_ * im.width), int(b * im.height)))
    art_ratio = im.height / im.width
    palette = spec.get("palette") or swatches(im)
    srgb = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    report = {"source": spec["source_info"], "source_px": [im.width, im.height], "colour": colour_note,
              "processing": "Lanczos downsampling to exactly 300 DPI at printed size; UnsharpMask radius 0.8 px, "
                            "45 %, threshold 2 (output sharpening for print). No colour, contrast or content changes. "
                            "No upscaling, no AI generation.",
              "palette": palette, "files": {}}

    for size_name, (W, H) in SIZES.items():
        L = layout(W, H, art_ratio)
        aw, ah = L["art"][2], L["art"][3]
        need = (mm2px(aw), mm2px(ah))
        if im.width < need[0] or im.height < need[1]:
            report["files"][size_name] = {"skipped": f"source too small: needs {need} px, has {im.size}. Refusing to upscale."}
            continue
        art = im.resize(need, Image.LANCZOS, reducing_gap=3.0)
        art = art.filter(ImageFilter.UnsharpMask(radius=0.8, percent=45, threshold=2))
        art_file = os.path.join(folders["enh"], f"{slug}_ARTWORK_{size_name}_300DPI_sRGB.jpg")
        art.save(art_file, "JPEG", quality=95, subsampling=0, optimize=True, icc_profile=srgb, dpi=(DPI, DPI))
        for bleed in (False, True):
            name = f"{slug}_{size_name}_300DPI_PRINT" + ("_BLEED3MM" if bleed else "") + ".pdf"
            sub = folders[size_name] if not bleed else os.path.join(folders[size_name], "with 3mm bleed (only if the shop asks)")
            os.makedirs(sub, exist_ok=True)
            pdf = os.path.join(sub, name)
            build_pdf(pdf, size_name, art_file, art_ratio, spec, palette, bleed)
            report["files"][name] = verify(pdf, size_name, bleed, L, need, art_file)
        prev = os.path.join(folders["prev"], f"{slug}_{size_name}_preview")
        subprocess.run(["pdftoppm", "-r", "60" if size_name == "A3" else "85", "-png", "-singlefile",
                        os.path.join(folders[size_name], f"{slug}_{size_name}_300DPI_PRINT.pdf"), prev], check=True)
    json.dump(report, open(os.path.join(folders["qc"], f"{slug}_qc.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(report, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
