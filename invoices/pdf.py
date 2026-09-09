"""Server-side invoice PDF.

Built with ReportLab (pure-Python wheel — no Cairo/Pango, so it installs on
shared cPanel hosting). Rendering here rather than through the browser's print
dialog keeps the page headers, URLs and "1/2" page numbers off the document,
and lets us guarantee a single page: the block layout is measured first and
scaled down if it would overflow.

Block order comes from `InvoiceSection`, so the admin controls it.
"""

from decimal import Decimal
from io import BytesIO

from django.contrib.staticfiles import finders

from reportlab.lib.colors import HexColor, Color
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as rl_canvas

from .models import InvoiceSection

# Brand palette — matches templates/invoices/invoice_detail.html
NAVY = HexColor('#211C46')
NAVY_2 = HexColor('#2C2560')
PURPLE = HexColor('#7B52E1')
INK = HexColor('#1F2233')
MUTED = HexColor('#6B7280')
LINE = HexColor('#E7E8EF')
SOFT = HexColor('#F6F5FC')
GREEN = HexColor('#16A34A')
RED = HexColor('#DC2626')
AMBER_BG = HexColor('#FFF8EC')
AMBER_LINE = HexColor('#FCD9A4')
AMBER_INK = HexColor('#7A5210')
AMBER_STRONG = HexColor('#B45309')
WHITE = HexColor('#FFFFFF')

PAGE_W, PAGE_H = A4
MARGIN = 34
CONTENT_W = PAGE_W - 2 * MARGIN

BOLD = 'Helvetica-Bold'
REG = 'Helvetica'

COMPANY_LINES = [
    'Mbeya, Tanzania  ·  info@kianvosoft.com  ·  www.kianvosoft.com',
    '0749 909 819 / 0753 177 709 / 0782 529 129',
]


def _fmt(currency, amount):
    """TSh 590,000 — no decimals, the way the shilling is quoted."""
    if amount is None:
        return ''
    return f"{currency} {Decimal(amount):,.0f}"


def _date(value):
    return value.strftime('%d %b %Y') if value else ''


def _wrap(text, font, size, max_width):
    """Greedy word wrap, returning a list of lines."""
    words = str(text or '').split()
    if not words:
        return ['']
    lines, current = [], words[0]
    for word in words[1:]:
        trial = f"{current} {word}"
        if stringWidth(trial, font, size) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


class InvoiceCanvas:
    """Draws blocks top-down, tracking `y`, so blocks can be reordered freely."""

    def __init__(self, canvas, invoice, scale=1.0):
        self.c = canvas
        self.inv = invoice
        self.s = scale
        self.y = PAGE_H - MARGIN

    # -- primitives ---------------------------------------------------------
    def f(self, size):
        """Scaled font size."""
        return size * self.s

    def gap(self, points):
        self.y -= points * self.s

    def text(self, x, y, value, font=REG, size=9, color=INK):
        self.c.setFillColor(color)
        self.c.setFont(font, self.f(size))
        self.c.drawString(x, y, str(value))

    def rtext(self, x, y, value, font=REG, size=9, color=INK):
        self.c.setFillColor(color)
        self.c.setFont(font, self.f(size))
        self.c.drawRightString(x, y, str(value))

    def rounded(self, x, y, w, h, fill=None, stroke=None, radius=7, left_bar=None):
        if fill is not None:
            self.c.setFillColor(fill)
        self.c.setStrokeColor(stroke or fill or WHITE)
        self.c.setLineWidth(0.8)
        self.c.roundRect(x, y, w, h, radius, stroke=1 if stroke else 0, fill=1 if fill else 0)
        if left_bar:
            self.c.setFillColor(left_bar)
            self.c.rect(x, y, 3.2, h, stroke=0, fill=1)

    def label(self, x, y, value, color=MUTED, size=7.2):
        """Small uppercase caption."""
        self.text(x, y, str(value).upper(), font=BOLD, size=size, color=color)

    # -- blocks -------------------------------------------------------------
    def header(self):
        inv = self.inv
        h = 108 * self.s
        top = self.y - h
        self.c.setFillColor(NAVY)
        self.c.roundRect(MARGIN, top, CONTENT_W, h, 10, stroke=0, fill=1)
        # Soft purple wash on the right, echoing the web header's glow. Clipped
        # to the header so it can't spill onto the white page.
        self.c.saveState()
        clip = self.c.beginPath()
        clip.roundRect(MARGIN, top, CONTENT_W, h, 10)
        self.c.clipPath(clip, stroke=0, fill=0)
        self.c.setFillColor(Color(PURPLE.red, PURPLE.green, PURPLE.blue, alpha=0.30))
        self.c.circle(MARGIN + CONTENT_W - 30, top + h - 4, 58 * self.s, stroke=0, fill=1)
        self.c.setFillColor(Color(NAVY_2.red, NAVY_2.green, NAVY_2.blue, alpha=0.55))
        self.c.circle(MARGIN + CONTENT_W - 96, top + h + 26, 52 * self.s, stroke=0, fill=1)
        self.c.restoreState()

        x = MARGIN + 20
        cursor = top + h - 26 * self.s

        logo = finders.find('assets/img/brand/logo.png')
        if logo:
            box = 38 * self.s
            self.c.setFillColor(WHITE)
            self.c.roundRect(x, cursor - box + 12 * self.s, box, box, 8, stroke=0, fill=1)
            try:
                self.c.drawImage(
                    ImageReader(logo), x + 3, cursor - box + 15 * self.s,
                    width=box - 6, height=box - 6,
                    preserveAspectRatio=True, mask='auto',
                )
            except Exception:
                pass  # a missing/unreadable logo must never break the invoice
            x += box + 12 * self.s

        self.text(x, cursor, 'KianvoSoft', font=BOLD, size=17, color=WHITE)
        self.text(x, cursor - 13 * self.s, "Innovating Africa's Digital Future",
                  size=8, color=HexColor('#C9C3E8'))

        right = MARGIN + CONTENT_W - 20
        self.rtext(right, cursor + 2 * self.s, 'INVOICE', font=BOLD, size=19, color=WHITE)
        self.rtext(right, cursor - 13 * self.s, inv.number, font=BOLD, size=9.5,
                   color=HexColor('#D8D3F0'))

        # Status pill
        paid = inv.is_paid
        text = 'FULLY PAID' if paid else inv.get_status_display().upper()
        size = 7.2
        w = stringWidth(text, BOLD, self.f(size)) + 16
        pill_y = cursor - 32 * self.s
        self.c.setFillColor(GREEN if paid else Color(1, 1, 1, alpha=0.18))
        self.c.setStrokeColor(GREEN if paid else Color(1, 1, 1, alpha=0.45))
        self.c.roundRect(right - w, pill_y, w, 13 * self.s, 6.5, stroke=1, fill=1)
        self.rtext(right - 8, pill_y + 4 * self.s, text, font=BOLD, size=size, color=WHITE)

        line_y = top + 26 * self.s
        for i, line in enumerate(COMPANY_LINES):
            self.text(MARGIN + 20, line_y - i * 10 * self.s, line, size=7.6,
                      color=HexColor('#B9B2DC'))

        self.y = top
        self.gap(14)

    def meta(self):
        """Billed to / Issued / For — three columns."""
        inv = self.inv
        col = CONTENT_W / 3
        top = self.y
        rows = []

        # Each entry is (text, strong) — a wrapped title stays bold throughout.
        billed = [(inv.client.name, True)]
        for extra in (inv.client.contact_person, inv.client.phone,
                      inv.client.email, inv.client.address):
            if extra:
                billed.append((extra, False))

        issued = [(_date(inv.issue_date), True)]
        if inv.due_date:
            issued.append((f"Due {_date(inv.due_date)}", False))

        for_lines = [(inv.project_title, True),
                     (inv.get_project_type_display(), False)]
        if inv.is_subscription and inv.period_label:
            for_lines.append(
                (f"{inv.get_billing_cycle_display()} · {inv.period_label}", False)
            )

        rows.append(('Billed To', billed))
        rows.append(('Issued', issued))
        rows.append(('For', for_lines))

        depth = 0
        for i, (title, lines) in enumerate(rows):
            x = MARGIN + i * col
            y = top - 10 * self.s
            self.label(x, y, title)
            y -= 12 * self.s
            for line, strong in lines:
                font = BOLD if strong else REG
                size = 9.5 if strong else 8.2
                for piece in _wrap(line, font, self.f(size), col - 14):
                    self.text(x, y, piece, font=font, size=size,
                              color=NAVY if strong else MUTED)
                    y -= 11 * self.s
            depth = max(depth, top - y)

        self.y = top - depth
        self.gap(6)

    def subscription(self):
        inv = self.inv
        if not inv.is_subscription or not inv.period_label:
            return
        h = 34 * self.s
        top = self.y - h
        self.rounded(MARGIN, top, CONTENT_W, h, fill=SOFT, stroke=LINE, left_bar=PURPLE)
        title = 'Subscription'
        if inv.plan_name:
            title += f" — {inv.plan_name}"
        self.label(MARGIN + 14, top + h - 13 * self.s, title, color=MUTED)
        self.text(MARGIN + 14, top + 9 * self.s, inv.period_label, font=BOLD,
                  size=10, color=NAVY)
        if inv.next_period_start:
            right = MARGIN + CONTENT_W - 14
            self.rtext(right, top + h - 13 * self.s, 'RENEWS ON / INAENDELEA',
                       font=BOLD, size=7.2, color=MUTED)
            self.rtext(right, top + 9 * self.s, _date(inv.next_period_start),
                       font=BOLD, size=10, color=NAVY)
        self.y = top
        self.gap(10)

    def items(self):
        inv = self.inv
        head_h = 17 * self.s
        x_qty = MARGIN + CONTENT_W * 0.60
        x_price = MARGIN + CONTENT_W * 0.80
        x_amount = MARGIN + CONTENT_W
        desc_w = CONTENT_W * 0.57

        top = self.y - head_h
        self.c.setFillColor(SOFT)
        self.c.rect(MARGIN, top, CONTENT_W, head_h, stroke=0, fill=1)
        base = top + 5.5 * self.s
        self.label(MARGIN + 8, base, 'Description', color=NAVY)
        self.rtext(x_qty, base, 'QTY', font=BOLD, size=7.2, color=NAVY)
        self.rtext(x_price, base, 'UNIT PRICE', font=BOLD, size=7.2, color=NAVY)
        self.rtext(x_amount - 8, base, 'AMOUNT', font=BOLD, size=7.2, color=NAVY)
        self.y = top

        for item in inv.items.all():
            lines = _wrap(item.description, BOLD, self.f(8.8), desc_w)
            row_h = (10 + 11 * len(lines)) * self.s
            top = self.y - row_h
            y = top + row_h - 12 * self.s
            for k, line in enumerate(lines):
                self.text(MARGIN + 8, y, line, font=BOLD, size=8.8, color=INK)
                y -= 11 * self.s
            first = top + row_h - 12 * self.s
            qty = item.quantity.normalize() if item.quantity else 0
            self.rtext(x_qty, first, f"{qty}", size=8.8, color=MUTED)
            self.rtext(x_price, first, _fmt(inv.currency, item.unit_price), size=8.8, color=MUTED)
            self.rtext(x_amount - 8, first, _fmt(inv.currency, item.line_total),
                       font=BOLD, size=8.8, color=INK)
            self.c.setStrokeColor(LINE)
            self.c.setLineWidth(0.6)
            self.c.line(MARGIN, top, MARGIN + CONTENT_W, top)
            self.y = top

        self.gap(8)

    def totals(self):
        inv = self.inv
        rows = [('Subtotal', _fmt(inv.currency, inv.subtotal), REG, INK)]
        if inv.discount:
            rows.append(('Discount', '- ' + _fmt(inv.currency, inv.discount), REG, INK))
        rows.append(('Total', _fmt(inv.currency, inv.total), BOLD, NAVY))
        if inv.amount_paid:
            rows.append(('Paid', '- ' + _fmt(inv.currency, inv.amount_paid), REG, GREEN))
        rows.append(('Balance Due', _fmt(inv.currency, inv.balance_due), BOLD, RED))

        box_w = CONTENT_W * 0.46
        x = MARGIN + CONTENT_W - box_w
        h = (len(rows) * 14 + 10) * self.s
        top = self.y - h
        y = top + h - 13 * self.s
        for name, value, font, color in rows:
            big = font is BOLD
            self.text(x, y, name, font=font, size=9.6 if big else 8.8,
                      color=color if big else MUTED)
            self.rtext(MARGIN + CONTENT_W, y, value, font=font,
                       size=10.4 if big else 8.8, color=color)
            if name == 'Total':
                self.c.setStrokeColor(LINE)
                self.c.line(x, y - 4 * self.s, MARGIN + CONTENT_W, y - 4 * self.s)
            y -= 14 * self.s
        self.y = top
        self.gap(8)

    def payment(self):
        inv = self.inv
        rows = [
            ('Account name', inv.account_name),
            ('Bank', inv.bank_name),
            ('Account number', inv.account_number),
        ]
        call = inv.payment_call
        h = (30 + len(rows) * 13 + (26 if call else 0)) * self.s
        top = self.y - h
        self.rounded(MARGIN, top, CONTENT_W, h, fill=SOFT, stroke=LINE)
        self.label(MARGIN + 14, top + h - 14 * self.s, 'Payment Details / Malipo', color=NAVY)

        y = top + h - 30 * self.s
        for name, value in rows:
            self.text(MARGIN + 14, y, name, size=8.4, color=MUTED)
            self.rtext(MARGIN + CONTENT_W - 14, y, value or '—', font=BOLD, size=8.8, color=INK)
            y -= 13 * self.s

        if call:
            bar_h = 20 * self.s
            bar_y = top + 8 * self.s
            self.c.setFillColor(NAVY)
            self.c.roundRect(MARGIN + 12, bar_y, CONTENT_W - 24, bar_h, 6, stroke=0, fill=1)
            self.text(MARGIN + 22, bar_y + 6 * self.s, call['label'], size=8.2, color=WHITE)
            self.rtext(MARGIN + CONTENT_W - 22, bar_y + 5.5 * self.s,
                       _fmt(inv.currency, call['amount']),
                       font=BOLD, size=10, color=WHITE)
        self.y = top
        self.gap(10)

    def next_payment(self):
        inv = self.inv
        if not inv.next_period_start:
            return
        covers = inv.renewal_covers
        body = (
            f"This invoice covers "
            f"{inv.period_label if inv.is_subscription and inv.period_label else 'the work listed above'}. "
            f"From {_date(inv.next_period_start)} the amount payable is "
            f"{_fmt(inv.currency, inv.next_payment_amount)} for {covers}."
        )
        if inv.has_price_change:
            body += " This differs from the amount on this invoice — kiasi cha malipo kitabadilika."

        text_w = CONTENT_W * 0.66
        lines = _wrap(body, REG, self.f(8.4), text_w - 28)
        h = (30 + len(lines) * 10.5) * self.s
        top = self.y - h
        self.rounded(MARGIN, top, CONTENT_W, h, fill=AMBER_BG, stroke=AMBER_LINE)
        self.label(MARGIN + 14, top + h - 14 * self.s, 'Next Payment / Malipo Yajayo',
                   color=AMBER_STRONG)
        y = top + h - 27 * self.s
        for line in lines:
            self.text(MARGIN + 14, y, line, size=8.4, color=AMBER_INK)
            y -= 10.5 * self.s

        right = MARGIN + CONTENT_W - 14
        self.rtext(right, top + h - 26 * self.s, f"FROM {_date(inv.next_period_start).upper()}",
                   font=BOLD, size=7.2, color=AMBER_STRONG)
        self.rtext(right, top + h - 42 * self.s, _fmt(inv.currency, inv.next_payment_amount),
                   font=BOLD, size=14, color=AMBER_STRONG)
        self.y = top
        self.gap(10)

    def notes(self):
        inv = self.inv
        body = inv.notes or (
            'Asante kwa kufanya kazi na KianvoSoft. Thank you for your business.'
        )
        lines = []
        for paragraph in str(body).splitlines() or ['']:
            lines.extend(_wrap(paragraph, REG, self.f(8.4), CONTENT_W - 28))
        h = (26 + len(lines) * 10.5) * self.s
        top = self.y - h
        self.rounded(MARGIN, top, CONTENT_W, h, fill=WHITE, stroke=LINE)
        self.label(MARGIN + 14, top + h - 14 * self.s, 'Notes', color=NAVY)
        y = top + h - 26 * self.s
        for line in lines:
            self.text(MARGIN + 14, y, line, size=8.4, color=MUTED)
            y -= 10.5 * self.s
        self.y = top
        self.gap(10)

    def footer(self):
        h = 40 * self.s
        # Sit just under the last block, but never below the page margin, so a
        # short invoice doesn't leave a lake of white in the middle.
        top = max(MARGIN, self.y - 14 * self.s - h)
        self.c.setFillColor(SOFT)
        self.c.roundRect(MARGIN, top, CONTENT_W, h, 8, stroke=0, fill=1)
        centre = MARGIN + CONTENT_W / 2
        self.c.setFillColor(NAVY)
        self.c.setFont(BOLD, self.f(10.5))
        self.c.drawCentredString(centre, top + h - 16 * self.s, 'Asante! / Thank you')
        self.c.setFillColor(MUTED)
        self.c.setFont(REG, self.f(7.6))
        self.c.drawCentredString(
            centre, top + h - 27 * self.s,
            "Issued by KianvoSoft · Innovating Africa's Digital Future",
        )
        self.c.drawCentredString(
            centre, top + h - 36 * self.s,
            'Questions? info@kianvosoft.com · 0753 177 709',
        )

    # -- driver -------------------------------------------------------------
    BLOCKS = {
        InvoiceSection.SUBSCRIPTION: subscription,
        InvoiceSection.ITEMS: items,
        InvoiceSection.TOTALS: totals,
        InvoiceSection.PAYMENT: payment,
        InvoiceSection.NEXT_PAYMENT: next_payment,
        InvoiceSection.NOTES: notes,
    }

    def draw(self, keys):
        self.header()
        self.meta()
        for key in keys:
            block = self.BLOCKS.get(key)
            if block:
                block(self)
        self.footer()
        return self.y


def _measure(invoice, keys, scale):
    """Lay the invoice out on a throwaway canvas to see where it ends."""
    probe = rl_canvas.Canvas(BytesIO(), pagesize=A4)
    return InvoiceCanvas(probe, invoice, scale).draw(keys)


def render_invoice_pdf(invoice):
    """Return the invoice as single-page PDF bytes."""
    keys = InvoiceSection.ordered_keys()

    # Shrink until everything clears the footer. Long invoices (many line
    # items) compress rather than spilling onto a second page.
    floor = MARGIN + 48
    scale = 1.0
    for _ in range(14):
        if _measure(invoice, keys, scale) >= floor:
            break
        scale -= 0.05
        if scale <= 0.55:
            scale = 0.55
            break

    buffer = BytesIO()
    canvas = rl_canvas.Canvas(buffer, pagesize=A4)
    canvas.setTitle(f"Invoice {invoice.number} — KianvoSoft")
    canvas.setAuthor('KianvoSoft')
    canvas.setSubject(invoice.project_title)
    InvoiceCanvas(canvas, invoice, scale).draw(keys)
    canvas.showPage()   # exactly one page, always
    canvas.save()
    return buffer.getvalue()
