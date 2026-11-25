#!/usr/bin/env python3
"""Render the GTA Landlord Solutions ad flyer: 1080x1350 PNG and letter-size PDF."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas as pdfcanvas

OUT = Path(__file__).resolve().parent
MONT = "/usr/share/fonts/truetype/sand-box/google/Montserrat/Montserrat-VariableFont_wght.ttf"
INTER = "/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf"

INK = (26, 20, 8)
BRAND = (245, 166, 35)
CREAM = (255, 244, 224)
WHITE = (255, 255, 255)
MUTED = (58, 46, 24)

SITE_URL = "https://ssbrain.github.io/gta-landlord-solutions/"
SITE_DISPLAY = "ssbrain.github.io/gta-landlord-solutions"
FEE = "One month's rent + HST"
PHONE = "647-891-8658"

W, H = 1080, 1350


def font(path, size, weight=400, opsz=None):
    f = ImageFont.truetype(path, size)
    try:
        axes = f.get_variation_axes()
        vals = []
        for a in axes:
            name = a["name"]
            if name in (b"Weight", b"wght", "Weight", "wght"):
                vals.append(float(weight))
            elif name in (b"Optical size", b"opsz", "Optical size", "opsz"):
                vals.append(float(opsz if opsz is not None else a["default"]))
            else:
                vals.append(float(a["default"]))
        if vals:
            f.set_variation_by_axes(vals)
    except Exception:
        pass
    return f


def mont(size, weight=800):
    return font(MONT, size, weight)


def inter(size, weight=500):
    return font(INTER, size, weight, opsz=min(32, max(14, size)))


def text_size(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def wrap_lines(draw, text, fnt, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def make_qr(size):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(SITE_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color=INK, back_color=WHITE).convert("RGB")
    return img.resize((size, size), Image.Resampling.NEAREST)


def draw_logo(draw, cx, y, scale=1.0):
    """Draw the house+sun icon centered at (cx, y) top. Returns bottom y."""
    s = scale
    # sun
    r = int(16 * s)
    sun = (cx + int(22 * s), y + int(14 * s))
    draw.ellipse((sun[0] - r, sun[1] - r, sun[0] + r, sun[1] + r), fill=BRAND)
    # roof
    top = (cx, y + int(8 * s))
    left = (cx - int(36 * s), y + int(38 * s))
    right = (cx + int(36 * s), y + int(38 * s))
    draw.line([left, top, right], fill=INK, width=max(3, int(5 * s)))
    # walls
    wl = (cx - int(28 * s), y + int(36 * s))
    wr = (cx + int(28 * s), y + int(36 * s))
    bl = (cx - int(28 * s), y + int(72 * s))
    br = (cx + int(28 * s), y + int(72 * s))
    draw.line([wl, bl, br, wr], fill=INK, width=max(3, int(5 * s)))
    # door
    dw = int(12 * s)
    dh = int(22 * s)
    door_top = y + int(50 * s)
    draw.rounded_rectangle(
        (cx - dw // 2, door_top, cx + dw // 2, door_top + dh),
        radius=max(1, int(2 * s)),
        fill=INK,
    )
    return y + int(80 * s)


def render_png():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    bar = 14
    d.rectangle((0, 0, W, bar), fill=BRAND)
    d.rectangle((0, H - bar, W, H), fill=BRAND)

    y = 44
    y = draw_logo(d, W // 2, y, scale=1.15)
    brand_f = mont(20, 700)
    label = "GTA LANDLORD SOLUTIONS"
    # letter-spacing via per-char draw
    spacing = 6
    widths = [d.textlength(ch, font=brand_f) for ch in label]
    total = sum(widths) + spacing * (len(label) - 1)
    x = (W - total) / 2
    for ch, ww in zip(label, widths):
        d.text((x, y), ch, font=brand_f, fill=INK)
        x += ww + spacing
    _, bh = text_size(d, label, brand_f)
    y += bh + 14
    rule_w = 72
    d.rectangle(((W - rule_w) // 2, y, (W + rule_w) // 2, y + 5), fill=BRAND)
    y += 36

    head_f = mont(64, 800)
    head_lines = ["Every empty day", "is lost rent."]
    for line in head_lines:
        d.text((W / 2, y), line, font=head_f, fill=INK, anchor="mt")
        y += 76
    y += 8

    sub_f = mont(30, 700)
    sub_lines = ["We turn vacancies into", "signed leases — fast."]
    for line in sub_lines:
        d.text((W / 2, y), line, font=sub_f, fill=INK, anchor="mt")
        y += 42
    y += 28

    bullets = [
        "Qualified, screened tenants",
        "You approve every tenant",
        "Skip the no-shows and dead applications",
    ]
    bullet_f = inter(26, 600)
    # measure block width to left-align as a group
    max_tw = max(d.textlength(t, font=bullet_f) for t in bullets)
    circle_r = 14
    gap = 16
    block_w = circle_r * 2 + gap + max_tw
    bx = (W - block_w) / 2
    for t in bullets:
        cy = y + 16
        d.ellipse((bx, y, bx + circle_r * 2, y + circle_r * 2), fill=BRAND)
        d.text((bx + circle_r, cy), "✓", font=inter(20, 800), fill=INK, anchor="mm")
        d.text((bx + circle_r * 2 + gap, cy), t, font=bullet_f, fill=INK, anchor="lm")
        y += 48
    y += 22

    # price band
    band_top = y
    band_h = 200
    d.rectangle((0, band_top, W, band_top + band_h), fill=INK)
    lab_f = mont(16, 700)
    fee_f = mont(44, 800)
    note_f = inter(20, 500)
    cy = band_top + band_h / 2
    d.text((W / 2, cy - 62), "LEASING FEE", font=lab_f, fill=BRAND, anchor="mt")
    # letter-space the label a bit
    d.text((W / 2, cy - 18), FEE, font=fee_f, fill=BRAND, anchor="mt")
    d.text((W / 2, cy + 44), "Paid only when the lease is signed", font=note_f, fill=WHITE, anchor="mt")
    y = band_top + band_h + 28

    phone_f = mont(40, 800)
    d.text((W / 2, y), PHONE, font=phone_f, fill=INK, anchor="mt")
    y += 54

    # bottom: QR + URL + CTA button
    qr_size = 168
    qr = make_qr(qr_size)
    url_f = inter(18, 600)
    cta_f = mont(20, 700)
    cta = "Tell us about your unit"
    url_w = d.textlength(SITE_DISPLAY, font=url_f)
    cta_w = d.textlength(cta, font=cta_f)
    pad_x, pad_y = 20, 14
    btn_w, btn_h = cta_w + pad_x * 2, 20 + pad_y * 2
    text_w = max(url_w, btn_w)
    group_w = qr_size + 28 + text_w
    gx = (W - group_w) / 2
    remain = (H - bar - 16) - y
    gy = y + max(8, (remain - qr_size) * 0.35)
    img.paste(qr, (int(gx), int(gy)))
    d.rectangle((gx - 1, gy - 1, gx + qr_size, gy + qr_size), outline=INK, width=2)
    tx = gx + qr_size + 28
    ty = gy + qr_size / 2
    d.text((tx, ty - 36), SITE_DISPLAY, font=url_f, fill=MUTED, anchor="lm")
    bx, by = tx, ty + 2
    d.rounded_rectangle((bx, by, bx + btn_w, by + btn_h), radius=10, fill=BRAND)
    d.text((bx + btn_w / 2, by + btn_h / 2), cta, font=cta_f, fill=INK, anchor="mm")

    return img


def write_letter_pdf(png_img, pdf_path):
    """Place the 4:5 flyer on a letter page, cream margins, 300 dpi."""
    page_w, page_h = letter  # 612 x 792 points
    # Use a high-res raster of the flyer, scaled to page width with small side margin.
    margin = 18  # points
    draw_w = page_w - 2 * margin
    draw_h = draw_w * (H / W)
    if draw_h > page_h - 2 * margin:
        draw_h = page_h - 2 * margin
        draw_w = draw_h * (W / H)
    x = (page_w - draw_w) / 2
    y = (page_h - draw_h) / 2

    c = pdfcanvas.Canvas(str(pdf_path), pagesize=letter)
    # cream page background
    c.setFillColorRGB(CREAM[0] / 255, CREAM[1] / 255, CREAM[2] / 255)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    c.drawImage(ImageReader(png_img), x, y, width=draw_w, height=draw_h, mask="auto")
    c.setTitle("GTA Landlord Solutions")
    c.setAuthor("GTA Landlord Solutions")
    c.showPage()
    c.save()


def main():
    img = render_png()
    png_path = OUT / "gta-landlord-solutions-flyer.png"
    pdf_path = OUT / "gta-landlord-solutions-flyer.pdf"
    img.save(png_path, "PNG", optimize=True)
    write_letter_pdf(img, pdf_path)
    print("wrote", png_path, img.size, png_path.stat().st_size)
    print("wrote", pdf_path, pdf_path.stat().st_size)


if __name__ == "__main__":
    main()
