"""
URL routes for Billing Session module.
Mounted at: /api/v1/billing/
"""

from django.urls import path
from .views import (
    BillingSessionCreateView,
    BillingSessionDetailView,
    BillingSessionItemView,
    BillingSessionItemDetailView,
)

app_name = 'billing'

urlpatterns = [
    path('sessions/', BillingSessionCreateView.as_view(), name='session-create'),
    path('sessions/<uuid:pk>/', BillingSessionDetailView.as_view(), name='session-detail'),
    path('sessions/<uuid:pk>/items/', BillingSessionItemView.as_view(), name='session-add-item'),
    path('sessions/<uuid:pk>/items/<uuid:item_pk>/', BillingSessionItemDetailView.as_view(), name='session-item-detail'),
]
