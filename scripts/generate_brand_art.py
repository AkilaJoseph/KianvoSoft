"""Generate KianvoSoft's brand artwork as SVG (plus the one PNG that must be raster).

Everything here is vector art authored in code against the site's own CSS
tokens, so the images can never drift from the brand:

    --ks-cyan #00f0ff   --ks-purple #8b5cf6   --ks-blue #3b82f6
    --ks-bg-primary #0a0e1a   hero gradient #0a0e1a -> #1a103d -> #0f172a

Run it any time; it is deterministic — the same slug always produces the same
picture, so re-running never churns the repo.

    python scripts/generate_brand_art.py

Output: static/assets/img/generated/

Note on fonts: an SVG loaded through <img> cannot use the page's webfonts, so
the little text in these files falls back to a system sans stack on purpose.
The social card is a PNG because WhatsApp, Facebook and LinkedIn do not render
SVG for og:image.
"""

import hashlib
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'static' / 'assets' / 'img' / 'generated'

CYAN = '#00f0ff'
PURPLE = '#8b5cf6'
BLUE = '#3b82f6'
GREEN = '#10b981'
ORANGE = '#f59e0b'
PINK = '#ec4899'
BG_1 = '#0a0e1a'
BG_2 = '#1a103d'
BG_3 = '#0f172a'
TEXT = '#f1f5f9'
MUTED = '#94a3b8'

SANS = "'Segoe UI',Roboto,Helvetica,Arial,sans-serif"

# Accent pairs cycled per subject, so a wall of covers reads as one family
# without every tile looking identical.
ACCENTS = [
    (CYAN, PURPLE),
    (PURPLE, PINK),
    (BLUE, CYAN),
    (GREEN, CYAN),
    (ORANGE, PINK),
    (PINK, PURPLE),
]


def _seed(slug):
    """Stable pseudo-random integer for a slug."""
    return int(hashlib.md5(slug.encode()).hexdigest()[:8], 16)


def accents_for(slug):
    return ACCENTS[_seed(slug) % len(ACCENTS)]


def esc(text):
    return (str(text).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


# ---------------------------------------------------------------------------
# Shared background: gradient ground, grid, glow, circuitry
# ---------------------------------------------------------------------------

def defs(slug, w, h, a1, a2):
    uid = f"g{_seed(slug) % 100000}"
    return uid, f'''  <defs>
    <linearGradient id="{uid}bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{BG_1}"/>
      <stop offset="52%" stop-color="{BG_2}"/>
      <stop offset="100%" stop-color="{BG_3}"/>
    </linearGradient>
    <radialGradient id="{uid}glowA" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{a1}" stop-opacity=".55"/>
      <stop offset="100%" stop-color="{a1}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="{uid}glowB" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{a2}" stop-opacity=".45"/>
      <stop offset="100%" stop-color="{a2}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="{uid}stroke" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{a1}"/>
      <stop offset="100%" stop-color="{a2}"/>
    </linearGradient>
    <pattern id="{uid}grid" width="34" height="34" patternUnits="userSpaceOnUse">
      <path d="M34 0H0V34" fill="none" stroke="{TEXT}" stroke-opacity=".045" stroke-width="1"/>
    </pattern>
  </defs>'''


def ground(uid, w, h, slug):
    """Gradient + grid + two glows + a few circuit traces."""
    rnd = _seed(slug)
    gx1, gy1 = (rnd % 40) / 100 + 0.08, ((rnd >> 3) % 30) / 100 + 0.05
    gx2, gy2 = ((rnd >> 6) % 35) / 100 + 0.58, ((rnd >> 9) % 35) / 100 + 0.5

    traces = []
    for i in range(4):
        r = (rnd >> (i * 5)) % 1000
        y = h * (0.18 + 0.2 * i) + (r % 30) - 15
        x0 = -20 + (r % 90)
        step = w / 3.4
        d = (f"M{x0:.0f} {y:.0f} h{step * 0.55:.0f} "
             f"l{h * 0.055:.0f} {-h * 0.055:.0f} h{step * 0.5:.0f} "
             f"l{h * 0.05:.0f} {h * 0.05:.0f} h{step:.0f}")
        traces.append(
            f'<path d="{d}" fill="none" stroke="url(#{uid}stroke)" '
            f'stroke-opacity=".22" stroke-width="1.5" stroke-linecap="round"/>'
        )
        traces.append(
            f'<circle cx="{x0 + step * 0.55:.0f}" cy="{y:.0f}" r="3" '
            f'fill="url(#{uid}stroke)" fill-opacity=".5"/>'
        )

    return f'''  <rect width="{w}" height="{h}" fill="url(#{uid}bg)"/>
  <rect width="{w}" height="{h}" fill="url(#{uid}grid)"/>
  <ellipse cx="{w * gx1:.0f}" cy="{h * gy1:.0f}" rx="{w * .42:.0f}" ry="{h * .5:.0f}" fill="url(#{uid}glowA)"/>
  <ellipse cx="{w * gx2:.0f}" cy="{h * gy2:.0f}" rx="{w * .38:.0f}" ry="{h * .46:.0f}" fill="url(#{uid}glowB)"/>
  {chr(10).join('  ' + t for t in traces)}'''


# ---------------------------------------------------------------------------
# Motifs — drawn on a 100x100 grid, scaled and centred by the caller
# ---------------------------------------------------------------------------

def _m(body):
    return body


MOTIFS = {
    # </>
    'code': _m('''<path d="M34 30 12 50l22 20" /><path d="M66 30l22 20-22 20"/>
                  <path d="M58 22 42 78" stroke-opacity=".65"/>'''),
    'web': _m('''<rect x="10" y="20" width="80" height="60" rx="7"/>
                 <path d="M10 36h80"/><circle cx="21" cy="28" r="2.6" fill="currentColor" stroke="none"/>
                 <circle cx="30" cy="28" r="2.6" fill="currentColor" stroke="none"/>
                 <path d="M26 52h20M26 63h34M56 52h18" stroke-opacity=".6"/>'''),
    'mobile': _m('''<rect x="32" y="12" width="36" height="76" rx="8"/>
                    <path d="M44 21h12"/><circle cx="50" cy="78" r="3.4"/>
                    <path d="M40 36h20M40 46h20M40 56h13" stroke-opacity=".6"/>'''),
    'ai': _m('''<circle cx="22" cy="30" r="7"/><circle cx="22" cy="70" r="7"/>
                <circle cx="50" cy="50" r="9"/><circle cx="78" cy="30" r="7"/>
                <circle cx="78" cy="70" r="7"/>
                <path d="M29 33l13 12M29 67l13-13M58 45l13-12M58 55l13 12" stroke-opacity=".6"/>'''),
    'automation': _m('''<circle cx="38" cy="42" r="16"/><circle cx="38" cy="42" r="6"/>
                        <circle cx="68" cy="66" r="11"/><circle cx="68" cy="66" r="4"/>
                        <path d="M38 20v-8M38 64v8M16 42H8M60 42h8M23 27l-6-6M53 57l6 6"
                              stroke-opacity=".75"/>'''),
    'academy': _m('''<path d="M10 38 50 20l40 18-40 18z"/>
                     <path d="M26 46v20c0 6 11 10 24 10s24-4 24-10V46" stroke-opacity=".7"/>
                     <path d="M84 42v20" stroke-opacity=".7"/>'''),
    'consulting': _m('''<path d="M12 22h48a6 6 0 016 6v22a6 6 0 01-6 6H32L16 68V56h-4a6 6 0 01-6-6V28a6 6 0 016-6z"
                             transform="translate(6,2)"/>
                        <path d="M34 36h22M34 46h14" stroke-opacity=".6"/>'''),
    'saas': _m('''<path d="M28 62a16 16 0 011-31 22 22 0 0142-6 15 15 0 01-1 37z"/>
                  <path d="M50 50v22M50 72l-8-8M50 72l8-8" stroke-opacity=".75"/>'''),
    'product': _m('''<path d="M50 12l34 19v38L50 88 16 69V31z"/>
                     <path d="M16 31l34 19 34-19M50 50v38" stroke-opacity=".55"/>'''),
    'training': _m('''<path d="M14 22h30a8 8 0 018 8v50a8 8 0 00-8-6H14z"/>
                      <path d="M86 22H56a8 8 0 00-8 8v50a8 8 0 018-6h30z"/>'''),
    'research': _m('''<path d="M40 12v26L20 74a8 8 0 007 12h46a8 8 0 007-12L60 38V12"/>
                      <path d="M34 12h32" /><path d="M30 58h40" stroke-opacity=".6"/>
                      <circle cx="43" cy="68" r="3.2" fill="currentColor" stroke="none"/>
                      <circle cx="57" cy="74" r="4" fill="currentColor" stroke="none"/>'''),
    'outreach': _m('''<path d="M18 44v12a4 4 0 004 4h10l24 16V24L32 40H22a4 4 0 00-4 4z"/>
                      <path d="M68 34a22 22 0 010 32M78 24a34 34 0 010 52" stroke-opacity=".65"/>'''),
    'security': _m('''<path d="M50 10l32 12v26c0 22-14 34-32 42-18-8-32-20-32-42V22z"/>
                      <path d="M36 50l10 10 20-20" stroke-opacity=".85"/>'''),
    'cloud': _m('''<path d="M30 68a16 16 0 011-32 22 22 0 0142-6 15 15 0 01-1 38z"/>
                   <path d="M40 78h20M34 88h32" stroke-opacity=".5"/>'''),
    'news': _m('''<rect x="10" y="22" width="66" height="56" rx="5"/>
                  <path d="M76 36h12v36a6 6 0 01-12 0z" stroke-opacity=".7"/>
                  <path d="M20 36h30M20 48h46M20 58h46M20 68h30" stroke-opacity=".6"/>'''),
    'innovation': _m('''<path d="M50 8c14 12 22 26 22 40a22 22 0 01-44 0c0-14 8-28 22-40z"/>
                        <circle cx="50" cy="46" r="9"/>
                        <path d="M34 74l-10 16 18-6M66 74l10 16-18-6" stroke-opacity=".7"/>'''),
    'devops': _m('''<rect x="14" y="16" width="72" height="20" rx="5"/>
                    <rect x="14" y="42" width="72" height="20" rx="5"/>
                    <rect x="14" y="68" width="72" height="18" rx="5"/>
                    <circle cx="26" cy="26" r="3" fill="currentColor" stroke="none"/>
                    <circle cx="26" cy="52" r="3" fill="currentColor" stroke="none"/>
                    <circle cx="26" cy="77" r="3" fill="currentColor" stroke="none"/>'''),
    'spark': _m('''<path d="M50 10l9 27 27 9-27 9-9 27-9-27-27-9 27-9z"/>
                   <circle cx="80" cy="24" r="5" stroke-opacity=".7"/>'''),
}


def motif(name, cx, cy, size, color, width=3.4, opacity=1.0):
    """Place a motif centred on (cx, cy), scaled so 100 units -> `size`."""
    body = MOTIFS.get(name, MOTIFS['spark'])
    k = size / 100.0
    x, y = cx - size / 2, cy - size / 2
    return (f'  <g transform="translate({x:.1f},{y:.1f}) scale({k:.4f})" '
            f'fill="none" stroke="{color}" color="{color}" stroke-width="{width / k:.2f}" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}">'
            f'{body}</g>')


# ---------------------------------------------------------------------------
# Compositions
# ---------------------------------------------------------------------------

def cover(slug, label, kicker, motif_name, w=1200, h=630):
    """Wide cover art — blog posts, categories, announcements, OG-style tiles."""
    a1, a2 = accents_for(slug)
    uid, d = defs(slug, w, h, a1, a2)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img" aria-label="{esc(label)}">',
        d, ground(uid, w, h, slug),
        motif(motif_name, w * 0.78, h * 0.5, min(w, h) * 0.52, f'url(#{uid}stroke)', 4.2, 0.9),
    ]
    # Accent rule + wordmark block on the left
    parts.append(f'  <rect x="{w * .066:.0f}" y="{h * .30:.0f}" width="4" '
                 f'height="{h * .30:.0f}" rx="2" fill="url(#{uid}stroke)"/>')
    if kicker:
        parts.append(
            f'  <text x="{w * .10:.0f}" y="{h * .36:.0f}" font-family="{SANS}" '
            f'font-size="{h * .038:.0f}" font-weight="700" letter-spacing="3" '
            f'fill="{a1}">{esc(kicker.upper())}</text>')
    # Wrap the label onto at most three lines
    words, lines, cur = str(label).split(), [], ''
    for word in words:
        trial = f"{cur} {word}".strip()
        if len(trial) > 22 and cur:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    lines.append(cur)
    lines = lines[:3]
    fs = h * (0.115 if len(lines) < 3 else 0.095)
    for i, line in enumerate(lines):
        parts.append(
            f'  <text x="{w * .10:.0f}" y="{h * .50 + i * fs * 1.12:.0f}" '
            f'font-family="{SANS}" font-size="{fs:.0f}" font-weight="800" '
            f'fill="{TEXT}">{esc(line)}</text>')
    parts.append(
        f'  <text x="{w * .10:.0f}" y="{h * .88:.0f}" font-family="{SANS}" '
        f'font-size="{h * .036:.0f}" font-weight="600" letter-spacing="2" '
        f'fill="{MUTED}">KIANVOSOFT</text>')
    parts.append('</svg>')
    return '\n'.join(parts)


def tile(slug, motif_name, size=640):
    """Square-ish service / product tile: motif on brand ground, no text."""
    a1, a2 = accents_for(slug)
    w = h = size
    uid, d = defs(slug, w, h, a1, a2)
    return '\n'.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img" aria-label="{esc(slug)}">',
        d, ground(uid, w, h, slug),
        f'  <rect x="{w * .12:.0f}" y="{h * .12:.0f}" width="{w * .76:.0f}" '
        f'height="{h * .76:.0f}" rx="{w * .07:.0f}" fill="{TEXT}" fill-opacity=".03" '
        f'stroke="url(#{uid}stroke)" stroke-opacity=".35" stroke-width="2"/>',
        motif(motif_name, w / 2, h / 2, size * 0.44, f'url(#{uid}stroke)', 4.0),
        '</svg>',
    ])


def banner(slug, motif_name, w=1600, h=700):
    """Wide page/hero band — motif right, soft geometry left."""
    a1, a2 = accents_for(slug)
    uid, d = defs(slug, w, h, a1, a2)
    rings = ''.join(
        f'<circle cx="{w * .30:.0f}" cy="{h * .5:.0f}" r="{h * (.16 + i * .11):.0f}" '
        f'fill="none" stroke="url(#{uid}stroke)" stroke-opacity="{.30 - i * .07:.2f}" '
        f'stroke-width="1.6"/>'
        for i in range(3)
    )
    return '\n'.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img" aria-label="{esc(slug)}">',
        d, ground(uid, w, h, slug),
        '  ' + rings,
        motif(motif_name, w * .30, h * .5, h * .26, f'url(#{uid}stroke)', 3.6),
        motif('code' if motif_name != 'code' else 'web', w * .68, h * .46,
              h * .52, f'url(#{uid}stroke)', 4.4, .9),
        '</svg>',
    ])


def monogram(text, slug, size=320):
    """Initials badge — the honest stand-in where a real logo or photo is
    missing. Never pretends to be someone's mark or face."""
    a1, a2 = accents_for(slug)
    uid, d = defs(slug, size, size, a1, a2)
    initials = ''.join(w[0] for w in str(text).split()[:2]).upper() or '?'
    return '\n'.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
        f'width="{size}" height="{size}" role="img" aria-label="{esc(text)}">',
        d,
        f'  <rect width="{size}" height="{size}" rx="{size * .18:.0f}" fill="url(#{uid}bg)"/>',
        f'  <rect width="{size}" height="{size}" rx="{size * .18:.0f}" fill="url(#{uid}grid)"/>',
        f'  <ellipse cx="{size * .3:.0f}" cy="{size * .25:.0f}" rx="{size * .5:.0f}" '
        f'ry="{size * .5:.0f}" fill="url(#{uid}glowA)"/>',
        f'  <rect x="1" y="1" width="{size - 2}" height="{size - 2}" rx="{size * .18:.0f}" '
        f'fill="none" stroke="url(#{uid}stroke)" stroke-opacity=".45" stroke-width="2"/>',
        f'  <text x="50%" y="50%" text-anchor="middle" dominant-baseline="central" '
        f'font-family="{SANS}" font-size="{size * .36:.0f}" font-weight="800" '
        f'fill="url(#{uid}stroke)">{esc(initials)}</text>',
        '</svg>',
    ])


def error_404():
    w, h = 1000, 620
    slug = '404'
    a1, a2 = CYAN, PURPLE
    uid, d = defs(slug, w, h, a1, a2)
    return '\n'.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img" aria-label="Page not found">',
        d, ground(uid, w, h, slug),
        f'  <text x="50%" y="46%" text-anchor="middle" font-family="{SANS}" '
        f'font-size="230" font-weight="800" fill="url(#{uid}stroke)" '
        f'fill-opacity=".92" letter-spacing="8">404</text>',
        motif('spark', w * .5, h * .46, 520, f'url(#{uid}stroke)', 2.2, .18),
        f'  <text x="50%" y="63%" text-anchor="middle" font-family="{SANS}" '
        f'font-size="30" font-weight="600" letter-spacing="3" fill="{MUTED}">'
        f'PAGE NOT FOUND</text>',
        f'  <path d="M{w * .34:.0f} {h * .70:.0f}h{w * .32:.0f}" stroke="url(#{uid}stroke)" '
        f'stroke-opacity=".5" stroke-width="2"/>',
        '</svg>',
    ])


# ---------------------------------------------------------------------------
# The social card has to be a raster — SVG is not honoured for og:image
# ---------------------------------------------------------------------------

def social_card(path):
    from PIL import Image, ImageDraw, ImageFont

    W, H = 1200, 630
    img = Image.new('RGB', (W, H), BG_1)
    draw = ImageDraw.Draw(img, 'RGBA')

    def hexrgb(value):
        value = value.lstrip('#')
        return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))

    c1, c2, c3 = hexrgb(BG_1), hexrgb(BG_2), hexrgb(BG_3)
    for y in range(H):                       # diagonal-ish three-stop ground
        t = y / H
        if t < 0.52:
            k = t / 0.52
            row = tuple(int(c1[i] + (c2[i] - c1[i]) * k) for i in range(3))
        else:
            k = (t - 0.52) / 0.48
            row = tuple(int(c2[i] + (c3[i] - c2[i]) * k) for i in range(3))
        draw.line([(0, y), (W, y)], fill=row)

    for x in range(0, W, 34):                # grid
        draw.line([(x, 0), (x, H)], fill=(241, 245, 249, 10))
    for y in range(0, H, 34):
        draw.line([(0, y), (W, y)], fill=(241, 245, 249, 10))

    cyan, purple = hexrgb(CYAN), hexrgb(PURPLE)
    # Kept low-alpha and pushed off-canvas: a glow behind the wordmark or the
    # URL washes the text out.
    for r in range(430, 0, -6):
        a = int(34 * (1 - r / 430) ** 2)
        draw.ellipse([980 - r, 90 - r, 980 + r, 90 + r], fill=(*purple, a))
    for r in range(300, 0, -6):
        a = int(16 * (1 - r / 300) ** 2)
        draw.ellipse([-40 - r, 690 - r, -40 + r, 690 + r], fill=(*cyan, a))

    for i in range(3):                       # concentric rings, right side
        r = 150 + i * 62
        draw.ellipse([930 - r, 330 - r, 930 + r, 330 + r],
                     outline=(*cyan, 70 - i * 18), width=2)

    def font(size, bold=True):
        for name in (('segoeuib.ttf', 'arialbd.ttf') if bold
                     else ('segoeui.ttf', 'arial.ttf')):
            try:
                return ImageFont.truetype(name, size)
            except OSError:
                continue
        return ImageFont.load_default()

    logo = ROOT / 'static' / 'assets' / 'img' / 'brand' / 'logo.png'
    x = 96
    if logo.exists():
        side = 104
        mark = Image.open(logo).convert('RGBA').resize((side, side))
        plate = Image.new('RGBA', (side, side), (255, 255, 255, 255))
        plate.alpha_composite(mark)
        # The logo file has its own opaque white ground, so the rounding has to
        # be a mask over the finished plate rather than a shape beneath it.
        mask = Image.new('L', (side, side), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            [0, 0, side - 1, side - 1], radius=24, fill=255)
        plate.putalpha(mask)
        img.paste(plate, (x, 92), plate)
        x += 132

    draw.text((x, 104), 'KianvoSoft', font=font(60), fill=hexrgb(TEXT))
    draw.text((x, 172), "Innovating Africa's Digital Future",
              font=font(27, False), fill=hexrgb(MUTED))

    draw.rectangle([96, 300, 100, 452], fill=cyan)
    draw.text((132, 296), 'Software that solves', font=font(58), fill=hexrgb(TEXT))
    draw.text((132, 366), 'real problems.', font=font(58), fill=cyan)
    draw.text((132, 452), 'Web  ·  Mobile  ·  AI  ·  SaaS  ·  Consultancy',
              font=font(26, False), fill=hexrgb(MUTED))

    draw.line([(96, 546), (1104, 546)], fill=(*cyan, 90), width=2)
    draw.text((96, 566), 'kianvosoft.com', font=font(26), fill=hexrgb(TEXT))
    draw.text((900, 566), 'Mbeya, Tanzania', font=font(26, False), fill=hexrgb(MUTED))

    img.save(path, 'PNG', optimize=True)


# ---------------------------------------------------------------------------
# What to build
# ---------------------------------------------------------------------------

# Keys are the live Service.slug values — check with:
#   Service.objects.values_list('slug', flat=True)
SERVICE_MOTIFS = {
    'custom-software-development': 'code',
    'software': 'product',                 # Software Product Development
    'training': 'training',                # Technical Training & Capacity Building
    'web-application-development': 'web',
    'research': 'research',                # Applied AI Research
    'mobile-app-development': 'mobile',
    'ai-machine-learning': 'ai',
    'consulting': 'outreach',              # Technology Consultancy & Outreach
    'automation-systems': 'automation',
    'academy': 'academy',                  # KianvoSoft Academy
    'it-consulting-support': 'consulting',
    'saas-products': 'saas',               # SaaS Product Suite
}

# Keyed by slugify(ActiveProduct.name) so the template can ask with
# {% brand_art 'product' product.name|slugify %}.
PRODUCT_MOTIFS = {
    'imforia': 'saas',                     # pharmacy management
    'mjenzi': 'product',                   # POS & inventory
    'shopmanagerpro': 'product',
    'fleetlink': 'outreach',               # fleet / cargo tracking
    'ims': 'devops',                       # impact management
    'kianvo-meet': 'outreach',             # video conferencing
    'kianvo-classroom': 'academy',
    'help': 'training',                    # health education portal
}

CATEGORY_MOTIFS = {
    'ai-technology': ('ai', 'AI & Technology'),
    'cloud-devops': ('devops', 'Cloud & DevOps'),
    'company-news': ('news', 'Company News'),
    'mobile-development': ('mobile', 'Mobile Development'),
    'security': ('security', 'Security'),
    'tech': ('spark', 'Tech'),
    'tech-innovation': ('innovation', 'Tech & Innovation'),
    'tech-news': ('news', 'Tech News'),
    'web-development': ('web', 'Web Development'),
}

# Fallbacks used by templates when a record has no image of its own.
GENERIC = {
    'blog': ('spark', 'Insights', 'From the KianvoSoft team'),
    'project': ('product', 'Project', 'Built by KianvoSoft'),
    'announcement': ('news', 'Announcement', 'KianvoSoft'),
    'product': ('saas', 'Product', 'KianvoSoft'),
    'service': ('code', 'Service', 'KianvoSoft'),
}


def write(name, content):
    path = OUT / name
    path.write_text(content, encoding='utf-8')
    return path


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    made = []

    for slug, motif_name in SERVICE_MOTIFS.items():
        made.append(write(f'service-{slug}.svg', tile(slug, motif_name)))

    for slug, motif_name in PRODUCT_MOTIFS.items():
        made.append(write(f'product-{slug}.svg', tile(f'p-{slug}', motif_name, 720)))

    for slug, (motif_name, label) in CATEGORY_MOTIFS.items():
        made.append(write(f'blog-{slug}.svg', cover(slug, label, 'Article', motif_name)))

    for key, (motif_name, label, kicker) in GENERIC.items():
        made.append(write(f'fallback-{key}.svg', cover(f'fb-{key}', label, kicker, motif_name)))

    made.append(write('hero-services.svg', banner('services-hero', 'saas')))
    made.append(write('hero-about.svg', banner('about-hero', 'innovation')))
    made.append(write('404.svg', error_404()))
    made.append(write('monogram-partner.svg', monogram('Partner', 'partner-generic')))
    made.append(write('monogram-client.svg', monogram('Client', 'client-generic')))

    png = OUT / 'og-image.png'
    social_card(png)
    made.append(png)

    total = sum(p.stat().st_size for p in made)
    for p in sorted(made):
        print(f"  {p.relative_to(ROOT).as_posix():58} {p.stat().st_size / 1024:7.1f} KB")
    print(f"\n{len(made)} files, {total / 1024:.0f} KB total")


if __name__ == '__main__':
    main()
