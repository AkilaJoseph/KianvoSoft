from django.urls import path

from . import views

app_name = 'invoices'

urlpatterns = [
    path('i/<uuid:token>/', views.public_invoice, name='public_invoice'),
    path('i/<uuid:token>/pdf/', views.invoice_pdf, name='invoice_pdf'),
    path('r/<uuid:token>/', views.public_receipt, name='public_receipt'),
    path('r/<uuid:token>/pdf/', views.receipt_pdf, name='receipt_pdf'),
]
