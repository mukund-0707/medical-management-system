"""
Medicine Filters.
Used by list API for filtering and searching.
"""

import django_filters
from .models import Medicine
from .constants import MedicineStatus, DosageForm


class MedicineFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=MedicineStatus.CHOICES)
    dosage_form = django_filters.ChoiceFilter(choices=DosageForm.CHOICES)
    category = django_filters.CharFilter(lookup_expr='icontains')
    manufacturer = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Medicine
        fields = ['status', 'dosage_form', 'category', 'manufacturer']
