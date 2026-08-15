"""
Supplier Filters.
Used by list API for filtering.
"""

import django_filters
from .models import Supplier
from .constants import SupplierStatus


class SupplierFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=SupplierStatus.CHOICES)
    city = django_filters.CharFilter(lookup_expr='icontains')
    state = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Supplier
        fields = ['status', 'city', 'state']
