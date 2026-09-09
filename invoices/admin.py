from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Client, Invoice, InvoiceItem, InvoiceSection


def _fmt(currency, amount):
    return f"{currency} {amount:,.0f}"


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email', 'invoice_count')
    search_fields = ('name', 'contact_person', 'phone', 'email')
    ordering = ('name',)

    @admin.display(description='Invoices')
    def invoice_count(self, obj):
        return obj.invoices.count()


@admin.register(InvoiceSection)
class InvoiceSectionAdmin(admin.ModelAdmin):
    """Reorder the blocks on every invoice — the web page and the PDF both."""
    list_display = ('block', 'position', 'visible')
    list_editable = ('position', 'visible')
    ordering = ('position', 'id')

    @admin.display(description='Block', ordering='position')
    def block(self, obj):
        return obj.get_key_display()

    def has_add_permission(self, request):
        return False       # the six blocks are fixed; only their order changes

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return ('key',)


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 3
    fields = ('description', 'quantity', 'unit_price', 'line_total_display', 'order')
    readonly_fields = ('line_total_display',)

    @admin.display(description='Line total')
    def line_total_display(self, obj):
        if obj.pk:
            return f"{obj.invoice.currency} {obj.line_total:,.0f}"
        return "—"


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline]
    list_display = (
        'number', 'client', 'project_title', 'billing_type', 'period_column',
        'issue_date', 'total_display', 'balance_display', 'status', 'view_link',
    )
    list_filter = ('billing_type', 'status', 'project_type', 'billing_cycle', 'issue_date')
    search_fields = ('number', 'client__name', 'project_title', 'plan_name')
    date_hierarchy = 'issue_date'
    autocomplete_fields = ('client', 'previous_invoice')
    actions = ['renew_subscriptions']
    readonly_fields = (
        'number', 'created_at', 'updated_at', 'public_token',
        'summary_panel', 'view_link',
    )
    fieldsets = (
        ('Invoice', {
            'fields': ('number', 'client', 'project_title', 'project_type',
                       ('issue_date', 'due_date'), 'status'),
        }),
        ('Subscription (SaaS / recurring)', {
            'description': "Set Billing type to <b>Subscription</b> to bill a SaaS plan "
                           "per period. Period end and due date fill in automatically.",
            'fields': ('billing_type', 'plan_name', 'billing_cycle',
                       ('period_start', 'period_end'), 'auto_renew', 'previous_invoice'),
        }),
        ('Next payment (price change)', {
            'description': "Fill these in when the client pays a different amount next "
                           "time — e.g. build now, hosting &amp; support from next year. "
                           "It prints on the invoice, and the renewal is billed at this price.",
            'fields': ('renewal_amount', 'renewal_date', 'renewal_label'),
        }),
        ('Money', {
            'fields': ('currency', 'discount', 'deposit_percentage',
                       'amount_paid', 'summary_panel'),
        }),
        ('Payment details (prints on invoice)', {
            'fields': ('account_name', 'bank_name', 'account_number'),
        }),
        ('Note to client', {'fields': ('notes',)}),
        ('Share', {'fields': ('view_link', 'public_token')}),
        ('System', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )

    @admin.display(description='Period')
    def period_column(self, obj):
        return obj.period_label or '—'

    @admin.action(description='Renew — create next period invoice')
    def renew_subscriptions(self, request, queryset):
        created, skipped = [], 0
        for invoice in queryset:
            renewal = invoice.create_next_period_invoice()
            if renewal:
                created.append(renewal.number)
            else:
                skipped += 1
        if created:
            self.message_user(request, f"Created: {', '.join(created)}.")
        if skipped:
            self.message_user(
                request,
                f"{skipped} skipped — not a renewable subscription "
                "(needs Billing type = Subscription, auto-renew on, and a period end).",
                level='warning',
            )

    @admin.display(description='Total')
    def total_display(self, obj):
        return _fmt(obj.currency, obj.total)

    @admin.display(description='Balance')
    def balance_display(self, obj):
        colour = '#16a34a' if obj.is_paid else '#dc2626'
        label = 'PAID' if obj.is_paid else _fmt(obj.currency, obj.balance_due)
        return format_html('<b style="color:{}">{}</b>', colour, label)

    @admin.display(description='Invoice')
    def view_link(self, obj):
        if not obj.pk:
            return "— save first —"
        page = reverse('invoices:public_invoice', args=[obj.public_token])
        pdf = reverse('invoices:invoice_pdf', args=[obj.public_token])
        style = ('color:#fff;padding:4px 10px;border-radius:6px;'
                 'text-decoration:none;margin-right:6px;')
        return format_html(
            '<a class="button" href="{}" target="_blank" style="background:#5b3fd6;{}">'
            'Open &nearr;</a>'
            '<a class="button" href="{}?download=1" style="background:#0f766e;{}">'
            'PDF &darr;</a>',
            page, style, pdf, style,
        )

    @admin.display(description='Summary')
    def summary_panel(self, obj):
        if not obj.pk:
            return "Save the invoice to see totals."
        rows = [
            ('Subtotal', _fmt(obj.currency, obj.subtotal)),
            ('Discount', _fmt(obj.currency, obj.discount)),
            ('Total', _fmt(obj.currency, obj.total)),
        ]
        if obj.is_subscription:
            rows.append((f'Period ({obj.get_billing_cycle_display()})', obj.period_label or '—'))
        if obj.next_period_start:
            rows.append((
                'Next payment',
                f"{_fmt(obj.currency, obj.next_payment_amount)} on "
                f"{obj.next_period_start.strftime('%d %b %Y')}",
            ))
        if not obj.is_subscription:
            rows.append(
                (f'Deposit ({obj.deposit_percentage}%)', _fmt(obj.currency, obj.deposit_amount))
            )
        rows += [
            ('Paid so far', _fmt(obj.currency, obj.amount_paid)),
            ('Balance due', _fmt(obj.currency, obj.balance_due)),
        ]
        html = ''.join(
            f'<tr><td style="padding:2px 14px 2px 0;color:#555">{k}</td>'
            f'<td style="padding:2px 0;font-weight:600;text-align:right">{v}</td></tr>'
            for k, v in rows
        )
        return format_html('<table>{}</table>', format_html(html))
