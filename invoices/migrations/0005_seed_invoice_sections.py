from django.db import migrations


DEFAULT_ORDER = [
    'subscription',
    'items',
    'totals',
    'payment',
    'next_payment',
    'notes',
]


def seed(apps, schema_editor):
    InvoiceSection = apps.get_model('invoices', 'InvoiceSection')
    for position, key in enumerate(DEFAULT_ORDER, start=1):
        InvoiceSection.objects.get_or_create(
            key=key, defaults={'position': position, 'visible': True},
        )


def unseed(apps, schema_editor):
    InvoiceSection = apps.get_model('invoices', 'InvoiceSection')
    InvoiceSection.objects.filter(key__in=DEFAULT_ORDER).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_invoicesection'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
