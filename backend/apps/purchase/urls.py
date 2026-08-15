"""
URL routes for Purchase module.
Mounted at: /api/v1/purchases/
"""

from django.urls import path
from .views import PurchaseListCreateView, PurchaseDetailView, PurchaseFinalizeView, PurchaseCancelView

app_name = 'purchase'

urlpatterns = [
    path('', PurchaseListCreateView.as_view(), name='purchase-list-create'),
    path('<uuid:pk>/', PurchaseDetailView.as_view(), name='purchase-detail'),
    path('<uuid:pk>/finalize/', PurchaseFinalizeView.as_view(), name='purchase-finalize'),
    path('<uuid:pk>/cancel/', PurchaseCancelView.as_view(), name='purchase-cancel'),
]
