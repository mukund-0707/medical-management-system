"""
URL routes for Reports module.
Mounted at: /api/v1/reports/
"""

from django.urls import path
from .views import (
    SalesReportView,
    PurchaseReportView,
    InventoryReportView,
    LedgerReportView,
    ExpiryReportView,
    LowStockReportView,
    AdjustmentReportView,
    MedicineReportView,
    SupplierReportView,
)

app_name = 'reports'

urlpatterns = [
    path('sales/', SalesReportView.as_view(), name='sales'),
    path('purchases/', PurchaseReportView.as_view(), name='purchases'),
    path('inventory/', InventoryReportView.as_view(), name='inventory'),
    path('ledger/', LedgerReportView.as_view(), name='ledger'),
    path('expiry/', ExpiryReportView.as_view(), name='expiry'),
    path('low-stock/', LowStockReportView.as_view(), name='low-stock'),
    path('adjustments/', AdjustmentReportView.as_view(), name='adjustments'),
    path('medicines/', MedicineReportView.as_view(), name='medicines'),
    path('suppliers/', SupplierReportView.as_view(), name='suppliers'),
]
