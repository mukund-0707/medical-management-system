"""
URL routes for Dashboard module.
Mounted at: /api/v1/dashboard/
"""

from django.urls import path
from .views import (
    DashboardKPIView,
    DashboardSalesView,
    DashboardPurchaseView,
    DashboardInventoryView,
    DashboardAlertsView,
)

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardKPIView.as_view(), name='kpi'),
    path('sales/', DashboardSalesView.as_view(), name='sales'),
    path('purchases/', DashboardPurchaseView.as_view(), name='purchases'),
    path('inventory/', DashboardInventoryView.as_view(), name='inventory'),
    path('alerts/', DashboardAlertsView.as_view(), name='alerts'),
]
