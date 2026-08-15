"""
Inventory Filters.
"""

import django_filters
from .models import InventoryBatch, InventoryLedger
from .constants import BatchStatus, LedgerMovementType


class InventoryBatchFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=BatchStatus.CHOICES)
    medicine = django_filters.UUIDFilter(field_name='medicine__id')
    expiry_before = django_filters.DateFilter(field_name='expiry_date', lookup_expr='lte')
    expiry_after = django_filters.DateFilter(field_name='expiry_date', lookup_expr='gte')
    low_stock = django_filters.BooleanFilter(method='filter_low_stock')

    class Meta:
        model = InventoryBatch
        fields = ['status', 'medicine']

    def filter_low_stock(self, queryset, name, value):
        from .constants import LOW_STOCK_THRESHOLD
        if value:
            return queryset.filter(quantity__lte=LOW_STOCK_THRESHOLD, quantity__gt=0)
        return queryset


class InventoryLedgerFilter(django_filters.FilterSet):
    movement_type = django_filters.ChoiceFilter(choices=LedgerMovementType.CHOICES)
    medicine = django_filters.UUIDFilter(field_name='medicine__id')
    date_from = django_filters.DateFilter(field_name='created_at__date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at__date', lookup_expr='lte')

    class Meta:
        model = InventoryLedger
        fields = ['movement_type', 'medicine']
