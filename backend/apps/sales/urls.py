"""
URL routes for Sales module.
Mounted at: /api/v1/sales/
"""

from django.urls import path
from .views import CheckoutView, SaleListView, SaleDetailView, SaleByInvoiceView, SaleCancelView

app_name = 'sales'

urlpatterns = [
    path('', SaleListView.as_view(), name='sale-list'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('<uuid:pk>/', SaleDetailView.as_view(), name='sale-detail'),
    path('<uuid:pk>/cancel/', SaleCancelView.as_view(), name='sale-cancel'),
    path('invoice/<str:invoice_number>/', SaleByInvoiceView.as_view(), name='sale-by-invoice'),
]
