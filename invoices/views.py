from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Invoice, InvoiceSection, Receipt
from .pdf import render_invoice_pdf, render_receipt_pdf


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


def _get_receipt(token):
    return get_object_or_404(
        Receipt.objects.select_related('invoice', 'invoice__client'),
        public_token=token,
    )


def public_receipt(request, token):
    """Client-facing receipt, opened via its unguessable token link."""
    receipt = _get_receipt(token)
    return render(request, 'invoices/receipt_detail.html', {'receipt': receipt})


def receipt_pdf(request, token):
    """The receipt as a real PDF, built on the server — same approach as
    the invoice PDF, for the same reasons (see invoice_pdf above)."""
    receipt = _get_receipt(token)
    pdf = render_receipt_pdf(receipt)

    response = HttpResponse(pdf, content_type='application/pdf')
    disposition = 'attachment' if request.GET.get('download') else 'inline'
    filename = f"Receipt-{receipt.number}-KianvoSoft.pdf"
    response['Content-Disposition'] = f'{disposition}; filename="{filename}"'
    response['X-Robots-Tag'] = 'noindex, nofollow'
    return response
