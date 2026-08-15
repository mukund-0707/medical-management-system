"""
Purchase Filters.
"""

import django_filters
from .models import Purchase
from .constants import PurchaseStatus


class PurchaseFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=PurchaseStatus.CHOICES)
    supplier = django_filters.UUIDFilter(field_name='supplier__id')
    invoice_date = django_filters.DateFilter()
    invoice_date_from = django_filters.DateFilter(field_name='invoice_date', lookup_expr='gte')
    invoice_date_to = django_filters.DateFilter(field_name='invoice_date', lookup_expr='lte')

    class Meta:
        model = Purchase
        fields = ['status', 'supplier', 'invoice_date']
