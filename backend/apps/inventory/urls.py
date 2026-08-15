"""
URL routes for Inventory module.
Mounted at: /api/v1/inventory/
"""

from django.urls import path
from .views import (
    InventoryBatchListView,
    InventoryBatchDetailView,
    InventoryAdjustView,
    InventoryMarkExpiredView,
    InventoryLedgerListView,
    MedicineStockView,
)

app_name = 'inventory'

urlpatterns = [
    path('batches/', InventoryBatchListView.as_view(), name='batch-list'),
    path('batches/<uuid:pk>/', InventoryBatchDetailView.as_view(), name='batch-detail'),
    path('batches/<uuid:pk>/mark-expired/', InventoryMarkExpiredView.as_view(), name='batch-mark-expired'),
    path('adjust/', InventoryAdjustView.as_view(), name='adjust'),
    path('ledger/', InventoryLedgerListView.as_view(), name='ledger'),
    path('stock/<uuid:medicine_id>/', MedicineStockView.as_view(), name='medicine-stock'),
]
