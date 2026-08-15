"""
Sales Filters.
"""

import django_filters
from .models import Sale
from .constants import SaleStatus, PaymentMode


class SaleFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=SaleStatus.CHOICES)
    payment_mode = django_filters.ChoiceFilter(choices=PaymentMode.CHOICES)
    date_from = django_filters.DateFilter(field_name='sale_date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='sale_date', lookup_expr='lte')
    sale_date = django_filters.DateFilter()

    class Meta:
        model = Sale
        fields = ['status', 'payment_mode', 'sale_date']
