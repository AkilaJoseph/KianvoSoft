# KianvoSoft Invoices

A small billing app built into the KianvoSoft admin. Create a client, add line
items, and get a branded, print-ready invoice with a private link you can send
to the customer on WhatsApp.

## One-time setup (local and on cPanel)

```bash
pip install -r requirements.txt            # brings in reportlab, used for the PDF
python manage.py migrate
python manage.py collectstatic --noinput   # production only, so the logo loads
```

ReportLab is a pure-Python wheel with no system libraries behind it, so it
installs on shared cPanel hosting (WeasyPrint would need Cairo/Pango and does
not).

`django.contrib.humanize` and the `invoices` app are already added to
`INSTALLED_APPS`, and `/invoices/` is wired into the URLs.

## How to raise an invoice

1. Admin → **Invoices & Billing → Invoices → Add**.
2. Pick (or add) the **Client**, set the **Project title** and **type**.
3. Add **line items** (description, qty, unit price) — totals compute automatically.
4. Set **Deposit %** (default 75). Set 100 for a pay-in-full invoice.
5. Save, then press **Download PDF**.

The invoice number (e.g. `KVS-2026-0001`) is generated automatically.

## The PDF

`/invoices/i/<token>/pdf/` builds the file **on the server** with ReportLab —
never through the browser's print dialog. That matters because printing from
the browser stamps the page URL, the date and "1/2" page numbers onto the
document, and splits it across two sheets.

The server-built PDF:

- is **always a single page** — the layout is measured first and scaled down
  if a long invoice would overflow, so 20 line items still fit on one sheet;
- carries no URLs, timestamps or page numbering;
- opens inline for previewing, or add `?download=1` to save it.

Buttons: **Download PDF** in the portal and in the admin list, plus
**Download / View PDF** on the client-facing page itself.

## Rearranging the invoice (admin)

Admin → **Invoices & Billing → Invoice layout**. Six blocks, each with a
**position** and a **visible** tick:

| Block | Default position |
| --- | --- |
| Subscription band (plan & period) | 1 |
| Line items table | 2 |
| Totals | 3 |
| Payment details / Malipo | 4 |
| Next payment notice | 5 |
| Notes to the client | 6 |

Lower positions print first. Change a number, save, and both the web page and
the PDF follow the new order — untick **visible** to drop a block from every
invoice. Blocks can't be added or deleted, only reordered.

## Subscription invoices (SaaS plans)

Use these for systems you host and bill per period — school systems, POS,
hosting/domain renewals, anything recurring.

1. Portal → **New Invoice** → under *What are you billing?* pick
   **Subscription / recurring**.
2. Fill the **Subscription period** card:
   - **Plan name** — e.g. `Standard — 200 students`
   - **Billing cycle** — Monthly / Quarterly / Half-yearly / Yearly / Custom
   - **Period start** — the period end fills in automatically from the cycle
     (change it for a custom period), and the due date defaults to the start.
   - **Auto-renew** — leave on while the client is still subscribed.
3. Add line items (the *Quick subscription lines* buttons pre-fill the common
   ones), then save.

Differences from a one-off invoice:

- A period is always billed **in full** — deposit % is forced to 100 and the
  deposit block is hidden on the printed invoice.
- The printed invoice shows a **Subscription** band with the plan, the period
  being billed, and the renewal date.

### Renewing

On a saved subscription invoice, press **Renew — next period** (or select
invoices in the admin and run *Renew — create next period invoice*). That
creates a fresh draft invoice for the next period with the same line items,
a new number, `Amount paid` reset to 0, and a link back to the period it
followed. Renewal chains are shown on the edit page in both directions.

Renewing is skipped for invoices that aren't subscriptions, have auto-renew
off, or have no period end (custom cycle without an end date).

## "This year you pay X, from next year Y"

Very common: the client pays for the build now, then a different (usually
smaller, sometimes larger) amount every year for hosting, domain and support.
Tell them up front on the same invoice using the **Next payment** card:

| Field | Example |
| --- | --- |
| Next amount | `250000` |
| Payable from | `01/08/2027` |
| Then repeats every | `Yearly` |
| What it covers | `Hosting, domain & support (1 year)` |

The printed invoice then carries an amber notice under the totals:

> **Next payment / Malipo yajayo** — This invoice covers the work listed above.
> From **01 Aug 2027** the amount payable is **TSh 250,000** for **Hosting,
> domain & support (1 year)**. This is different from the amount on this
> invoice — kiasi cha malipo kitabadilika.

The portal form previews that sentence live as you type, so you can see exactly
what the client will read.

When the date arrives, press **Renew — next period**. The new invoice is billed
at the *next amount* on a single line (not a copy of the build line items), and
it schedules the year after that at the same rate — so the price steps up once
and then holds. This works on one-off and subscription invoices alike; leave
**Next amount** blank whenever the price simply stays the same.

## Recording payments

Update the **Amount paid** field as money comes in. The invoice recomputes:

- **Balance due** = Total − Amount paid
- **Deposit** = Total × Deposit %
- Status pill shows *Deposit paid / Fully paid* etc.

Set the **Status** dropdown to match (Sent, Deposit paid, Fully paid…).

## Payment details on the invoice

Defaults (Selcom · `0753177709` · account name *KianvoSoft*) are set in
`invoices/models.py` and can be overridden per invoice under **Payment details**.
To change the default for all future invoices, edit the three
`DEFAULT_*` constants at the top of `models.py`.

## The share link

Each invoice has an unguessable link: `/invoices/i/<token>/`. It carries
`noindex` and is disallowed in `robots.txt`, so it won't be found by search
engines — only people you send it to can open it.

## Receipts — recording a payment

Once a client has paid (all or part of an invoice), issue a receipt so they
have proof of payment. A receipt is what **moves the money** — creating one
adds its amount to the invoice's `amount_paid` and updates the status pill
automatically; you don't edit `Amount paid` by hand once receipts are in use.

**From the portal:** open the invoice and press **Record Payment** (shown
whenever a balance is still owed). It opens a receipt form with the invoice
and the amount still owed already filled in — adjust the amount if the
client paid a different sum, pick the payment method, add a reference (e.g.
the Selcom transaction code), and save. The invoice page then lists every
receipt issued against it under **Payments received**.

**From the admin:** Admin → **Invoices & Billing → Receipts → Add**. Pick the
invoice, enter the amount and method, save.

Either way, the receipt:

- gets its own number (e.g. `KVS-RCT-2026-0001`) and an unguessable share
  link, same pattern as an invoice (`/invoices/r/<token>/`);
- freezes a **balance before / balance after** snapshot at the moment it's
  issued, so it stays accurate even if the invoice changes later;
- moves the invoice to **Deposit paid**, **Partially paid**, or **Fully
  paid** depending on how much has now been paid in total (never touches a
  **Cancelled** invoice).

**Amount, invoice and payment date are locked once the receipt is saved** —
correcting a mistake means deleting the receipt (which reverses the payment
it applied) and issuing a new one, rather than editing figures that have
already been counted. Only the reference, payment method, "received by" and
notes can still be changed afterwards.

### The receipt PDF

Same approach as the invoice — built on the server with ReportLab, always a
single page, no browser headers or URLs. `/invoices/r/<token>/pdf/` to
preview, `?download=1` to save. Buttons: **Download PDF** on the receipt's
own page, and **PDF ↓** next to each receipt in the admin.

## Tests

```bash
python manage.py test invoices
```
