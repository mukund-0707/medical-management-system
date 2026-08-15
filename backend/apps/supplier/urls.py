"""
URL routes for Supplier module.
Mounted at: /api/v1/suppliers/
"""

from django.urls import path
from .views import SupplierListCreateView, SupplierDetailView

app_name = 'supplier'

urlpatterns = [
    path('', SupplierListCreateView.as_view(), name='supplier-list-create'),
    path('<uuid:pk>/', SupplierDetailView.as_view(), name='supplier-detail'),
]
