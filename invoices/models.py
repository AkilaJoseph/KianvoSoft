import calendar
import datetime
import uuid
from decimal import Decimal, ROUND_HALF_UP

from django.db import models
from django.urls import reverse
from django.utils import timezone


# ---------------------------------------------------------------------------
# Company payment defaults (edit here, or override per-invoice in the admin)
# ---------------------------------------------------------------------------
DEFAULT_ACCOUNT_NAME = 'KianvoSoft'
DEFAULT_BANK_NAME = 'Selcom'
DEFAULT_ACCOUNT_NUMBER = '0753177709'


def _money(value):
    """Round to 2 decimal places, the safe way for currency."""
    return Decimal(value or 0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def _add_months(date, months):
    """Same day-of-month `months` later, clamped to the end of short months."""
    month_index = date.month - 1 + months
    year = date.year + month_index // 12
    month = month_index % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    return date.replace(year=year, month=month, day=day)


class InvoiceSection(models.Model):
    """Order of the blocks on the printed invoice — HTML page and PDF alike.

    Rows are seeded by a migration; the admin reorders them by changing
    `position`, or hides a block by unticking `visible`.
    """
    SUBSCRIPTION = 'subscription'
    ITEMS = 'items'
    TOTALS = 'totals'
    PAYMENT = 'payment'
    NEXT_PAYMENT = 'next_payment'
    NOTES = 'notes'

    KEY_CHOICES = [
        (SUBSCRIPTION, 'Subscription band (plan & period)'),
        (ITEMS, 'Line items table'),
        (TOTALS, 'Totals'),
        (PAYMENT, 'Payment details / Malipo'),
        (NEXT_PAYMENT, 'Next payment notice'),
        (NOTES, 'Notes to the client'),
    ]
    # Order used when the table is empty, and by the seeding migration.
    DEFAULT_ORDER = [SUBSCRIPTION, ITEMS, TOTALS, PAYMENT, NEXT_PAYMENT, NOTES]

    key = models.CharField(max_length=30, unique=True, choices=KEY_CHOICES)
    position = models.PositiveIntegerField(
        default=0, help_text="Lower numbers print first.",
    )
    visible = models.BooleanField(
        default=True, help_text="Untick to leave this block off every invoice.",
    )

    class Meta:
        ordering = ['position', 'id']
        verbose_name = 'Invoice layout block'
        verbose_name_plural = 'Invoice layout'

    def __str__(self):
        return self.get_key_display()

    @classmethod
    def ordered_keys(cls):
        """Visible block keys in print order, falling back to the default."""
        keys = list(cls.objects.filter(visible=True).values_list('key', flat=True))
        known = [k for k in keys if k in dict(cls.KEY_CHOICES)]
        return known or list(cls.DEFAULT_ORDER)


class Client(models.Model):
    """A customer KianvoSoft builds for (website, system, poster, etc.)."""
    name = models.CharField(
        max_length=200,
        help_text="Business or person the invoice is addressed to.",
    )
    contact_person = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(
        max_length=255, blank=True,
        help_text="City / region, e.g. 'Mbeya, Tanzania'.",
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Invoice(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_SENT = 'sent'
    STATUS_DEPOSIT = 'deposit_paid'
    STATUS_PARTIAL = 'partially_paid'
    STATUS_PAID = 'paid'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_SENT, 'Sent — awaiting payment'),
        (STATUS_DEPOSIT, 'Deposit paid'),
        (STATUS_PARTIAL, 'Partially paid'),
        (STATUS_PAID, 'Fully paid'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    PROJECT_TYPES = [
        ('website', 'Website'),
        ('system', 'System / Software'),
        ('saas', 'SaaS Subscription'),
        ('hosting', 'Hosting / Domain'),
        ('poster', 'Poster / Design'),
        ('mobile_app', 'Mobile App'),
        ('maintenance', 'Maintenance / Support'),
        ('consultancy', 'Consultancy'),
        ('other', 'Other'),
    ]

    # -- billing model ------------------------------------------------------
    BILLING_ONE_OFF = 'one_off'
    BILLING_SUBSCRIPTION = 'subscription'
    BILLING_TYPE_CHOICES = [
        (BILLING_ONE_OFF, 'One-off project'),
        (BILLING_SUBSCRIPTION, 'Subscription / recurring'),
    ]

    CYCLE_MONTHLY = 'monthly'
    CYCLE_QUARTERLY = 'quarterly'
    CYCLE_SEMI_ANNUAL = 'semi_annual'
    CYCLE_ANNUAL = 'annual'
    CYCLE_CUSTOM = 'custom'
    BILLING_CYCLE_CHOICES = [
        (CYCLE_MONTHLY, 'Monthly'),
        (CYCLE_QUARTERLY, 'Quarterly (3 months)'),
        (CYCLE_SEMI_ANNUAL, 'Half-yearly (6 months)'),
        (CYCLE_ANNUAL, 'Yearly'),
        (CYCLE_CUSTOM, 'Custom period'),
    ]
    CYCLE_MONTHS = {
        CYCLE_MONTHLY: 1,
        CYCLE_QUARTERLY: 3,
        CYCLE_SEMI_ANNUAL: 6,
        CYCLE_ANNUAL: 12,
    }

    # Identity
    number = models.CharField(
        max_length=30, unique=True, blank=True,
        help_text="Auto-generated if left blank, e.g. KVS-2026-0001.",
    )
    public_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Who / what
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, related_name='invoices',
    )
    project_title = models.CharField(
        max_length=255,
        help_text="What this is for, e.g. 'Company Website — design, hosting & domain'.",
    )
    project_type = models.CharField(
        max_length=20, choices=PROJECT_TYPES, default='website',
    )

    # Subscription / recurring billing
    billing_type = models.CharField(
        max_length=20, choices=BILLING_TYPE_CHOICES, default=BILLING_ONE_OFF,
        help_text="One-off for project work; Subscription for SaaS / recurring plans.",
    )
    plan_name = models.CharField(
        max_length=120, blank=True,
        help_text="Subscription only, e.g. 'Starter', 'Pro — 10 users'.",
    )
    billing_cycle = models.CharField(
        max_length=20, choices=BILLING_CYCLE_CHOICES, default=CYCLE_MONTHLY,
        help_text="Subscription only. How often this plan is billed.",
    )
    period_start = models.DateField(
        null=True, blank=True,
        help_text="Subscription only. First day of the period being billed.",
    )
    period_end = models.DateField(
        null=True, blank=True,
        help_text="Subscription only. Auto-filled from the cycle if left blank.",
    )
    auto_renew = models.BooleanField(
        default=True,
        help_text="Subscription only. Tick if the plan continues after this period.",
    )
    previous_invoice = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='renewals',
        help_text="Set automatically when an invoice is renewed for the next period.",
    )

    # Next payment (tells the client up front what the renewal will cost).
    # Use it when the first payment differs from what follows — e.g. build now,
    # hosting & support from next year.
    renewal_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="What the client pays NEXT time, if it differs from this invoice. "
                  "Leave blank if the amount stays the same.",
    )
    renewal_date = models.DateField(
        null=True, blank=True,
        help_text="When that next payment is due. Subscriptions use the day after "
                  "the period ends if left blank.",
    )
    renewal_label = models.CharField(
        max_length=200, blank=True,
        help_text="What the next payment covers, e.g. 'Hosting, domain & support "
                  "(1 year)'. Printed on the invoice.",
    )

    # Dates
    issue_date = models.DateField(default=timezone.localdate)
    due_date = models.DateField(
        null=True, blank=True,
        help_text="Optional. When full payment or the balance is expected.",
    )

    # Money
    currency = models.CharField(max_length=8, default='TSh')
    discount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'),
        help_text="Optional discount applied to the subtotal.",
    )
    deposit_percentage = models.PositiveIntegerField(
        default=75,
        help_text="Deposit expected up front (e.g. 75). Set 100 for full payment invoices.",
    )
    amount_paid = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'),
        help_text="Total the client has paid so far. Update as payments come in.",
    )

    # Payment destination (prints on the invoice)
    account_name = models.CharField(max_length=120, default=DEFAULT_ACCOUNT_NAME)
    bank_name = models.CharField(max_length=120, default=DEFAULT_BANK_NAME)
    account_number = models.CharField(max_length=60, default=DEFAULT_ACCOUNT_NUMBER)

    # Extras
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    notes = models.TextField(
        blank=True,
        help_text="Shown to the client, e.g. terms or a thank-you note (Swahili is fine).",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-issue_date', '-id']

    def __str__(self):
        return f"{self.number} — {self.client}"

    # -- numbering ----------------------------------------------------------
    def _generate_number(self):
        year = (self.issue_date or timezone.localdate()).year
        prefix = f"KVS-{year}-"
        last = (
            Invoice.objects.filter(number__startswith=prefix)
            .order_by('-number').first()
        )
        seq = 1
        if last and last.number:
            try:
                seq = int(last.number.split('-')[-1]) + 1
            except (ValueError, IndexError):
                seq = Invoice.objects.filter(number__startswith=prefix).count() + 1
        return f"{prefix}{seq:04d}"

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self._generate_number()
        if self.billing_type == self.BILLING_SUBSCRIPTION:
            # A subscription period is billed in full — there is no deposit.
            self.deposit_percentage = 100
            if not self.period_start:
                self.period_start = self.issue_date or timezone.localdate()
            if not self.period_end:
                self.period_end = self._period_end_for(self.period_start)
            if not self.due_date:
                self.due_date = self.period_start
        super().save(*args, **kwargs)

    # -- subscription -------------------------------------------------------
    def _period_end_for(self, start):
        """Last day covered by one cycle starting at `start`. None if custom."""
        months = self.CYCLE_MONTHS.get(self.billing_cycle)
        if not start or not months:
            return None
        return _add_months(start, months) - datetime.timedelta(days=1)

    @property
    def is_subscription(self):
        return self.billing_type == self.BILLING_SUBSCRIPTION

    @property
    def period_label(self):
        """e.g. '01 Aug 2026 — 31 Aug 2026'. Empty for one-off invoices."""
        if not self.is_subscription or not self.period_start:
            return ''
        if not self.period_end:
            return self.period_start.strftime('%d %b %Y')
        return (
            f"{self.period_start.strftime('%d %b %Y')} — "
            f"{self.period_end.strftime('%d %b %Y')}"
        )

    @property
    def next_period_start(self):
        """When the client pays again — the renewal date.

        Taken from `renewal_date` if it was set by hand; otherwise, for a
        subscription, the day after this period ends. None if nothing is due
        again (one-off with no renewal date, or auto-renew switched off).
        """
        if self.is_subscription and not self.auto_renew:
            return None
        if self.renewal_date:
            return self.renewal_date
        if self.is_subscription and self.period_end:
            return self.period_end + datetime.timedelta(days=1)
        return None

    @property
    def has_price_change(self):
        """True when the next payment is a different amount from this one."""
        return (
            self.renewal_amount is not None
            and self.next_period_start is not None
            and _money(self.renewal_amount) != self.total
        )

    @property
    def next_payment_amount(self):
        """What the client will be billed next time."""
        if not self.next_period_start:
            return None
        if self.renewal_amount is not None:
            return _money(self.renewal_amount)
        return self.total

    @property
    def renewal_covers(self):
        """Label for the next payment, with a sensible fallback."""
        if self.renewal_label:
            return self.renewal_label
        if self.is_subscription:
            return f"{self.plan_name or self.project_title} — {self.get_billing_cycle_display().lower()}"
        return f"{self.project_title} — renewal"

    def create_next_period_invoice(self):
        """Build the next invoice for this client — the renewal.

        Carries the line items over, or replaces them with a single line at
        `renewal_amount` when the price changes after the first payment.
        Returns the new invoice, or None if nothing is due again.
        """
        start = self.next_period_start
        if not start:
            return None

        # Where the one after that falls due, so the chain keeps going.
        next_due = None
        if self.is_subscription:
            period_end = self._period_end_for(start)
        else:
            period_end = None
            months = self.CYCLE_MONTHS.get(self.billing_cycle)
            if months and self.renewal_date:
                next_due = _add_months(start, months)

        renewal = Invoice(
            client=self.client,
            project_title=self.project_title,
            project_type=self.project_type,
            billing_type=self.billing_type,
            plan_name=self.plan_name,
            billing_cycle=self.billing_cycle,
            period_start=start if self.is_subscription else None,
            period_end=period_end,
            auto_renew=self.auto_renew,
            previous_invoice=self,
            issue_date=start,
            due_date=start,
            currency=self.currency,
            # A price-change renewal is a fresh amount, not this invoice's total,
            # so this invoice's discount must not follow it across.
            discount=Decimal('0.00') if self.renewal_amount is not None else self.discount,
            deposit_percentage=100 if self.is_subscription else self.deposit_percentage,
            amount_paid=Decimal('0.00'),
            account_name=self.account_name,
            bank_name=self.bank_name,
            account_number=self.account_number,
            status=self.STATUS_DRAFT,
            notes=self.notes,
            # The new price becomes the standing price from here on.
            renewal_amount=self.renewal_amount,
            renewal_date=next_due,
            renewal_label=self.renewal_label,
        )
        renewal.save()

        if self.renewal_amount is not None:
            InvoiceItem.objects.create(
                invoice=renewal,
                description=self.renewal_covers,
                quantity=Decimal('1'),
                unit_price=_money(self.renewal_amount),
                order=0,
            )
        else:
            InvoiceItem.objects.bulk_create([
                InvoiceItem(
                    invoice=renewal,
                    description=item.description,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    order=item.order,
                )
                for item in self.items.all()
            ])
        return renewal

    # -- computed money -----------------------------------------------------
    @property
    def subtotal(self):
        return _money(sum((item.line_total for item in self.items.all()), Decimal('0')))

    @property
    def total(self):
        return _money(self.subtotal - (self.discount or Decimal('0')))

    @property
    def deposit_amount(self):
        return _money(self.total * Decimal(self.deposit_percentage) / Decimal('100'))

    @property
    def balance_due(self):
        return _money(self.total - (self.amount_paid or Decimal('0')))

    @property
    def is_paid(self):
        return self.balance_due <= Decimal('0.00') and self.total > 0

    @property
    def amount_outstanding_now(self):
        """What the client still owes toward the deposit (or the whole balance)."""
        target = self.total if self.deposit_percentage >= 100 else self.deposit_amount
        owed = _money(target - (self.amount_paid or Decimal('0')))
        return owed if owed > 0 else Decimal('0.00')

    @property
    def payment_call(self):
        """The 'pay this now' bar: what to ask for, and how much.

        Before the deposit lands, that is the deposit. Once it is covered the
        deposit is history — what is still owed is the rest of the money, so
        the bar switches to the balance instead of sitting at zero.
        Returns None when there is nothing left to ask for.
        """
        if self.total <= 0 or self.is_paid:
            return None
        if self.deposit_percentage < 100 and self.amount_outstanding_now > 0:
            return {
                'label': f"Deposit ({self.deposit_percentage}%) to start / kuanzia",
                'amount': self.amount_outstanding_now,
            }
        return {
            'label': 'Balance to complete / Salio lililobaki',
            'amount': self.balance_due,
        }

    def get_absolute_url(self):
        return reverse('invoices:public_invoice', args=[self.public_token])


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(
        max_length=255,
        help_text="e.g. 'Website design & development', 'Domain (1 year)', 'Hosting (1 year)'.",
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1'))
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.description

    @property
    def line_total(self):
        return _money((self.quantity or Decimal('0')) * (self.unit_price or Decimal('0')))
