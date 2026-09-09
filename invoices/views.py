from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Invoice, InvoiceSection
from .pdf import render_invoice_pdf


def _get_invoice(token):
    return get_object_or_404(
        Invoice.objects.select_related('client').prefetch_related('items'),
        public_token=token,
    )


def public_invoice(request, token):
    """Client-facing invoice, opened via its unguessable token link."""
    invoice = _get_invoice(token)
    return render(request, 'invoices/invoice_detail.html', {
        'invoice': invoice,
        'sections': InvoiceSection.ordered_keys(),
    })


def invoice_pdf(request, token):
    """The invoice as a real PDF, built on the server.

    Generated here rather than through the browser's print dialog so the file
    carries no page URL, timestamp or "1/2" page numbering, and always comes
    out as a single page. `?download=1` saves instead of previewing.
    """
    invoice = _get_invoice(token)
    pdf = render_invoice_pdf(invoice)

    response = HttpResponse(pdf, content_type='application/pdf')
    disposition = 'attachment' if request.GET.get('download') else 'inline'
    filename = f"Invoice-{invoice.number}-KianvoSoft.pdf"
    response['Content-Disposition'] = f'{disposition}; filename="{filename}"'
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response
