"""
Medicine Serializers.
Input validation and output formatting only.
No business logic here.
"""

from rest_framework import serializers
from .models import Medicine
from .constants import MedicineStatus


class MedicineCreateSerializer(serializers.ModelSerializer):
    """Used for POST — create new medicine."""

    class Meta:
        model = Medicine
        fields = [
            'name', 'barcode', 'generic_name', 'manufacturer',
            'strength', 'dosage_form', 'category', 'description',
            'storage_instruction', 'hsn_code', 'gst_percentage',
        ]
        # Remove auto unique validator from barcode — service handles it
        # and returns proper 409 Conflict instead of 400 Bad Request
        extra_kwargs = {
            'barcode': {'validators': []},
        }

    def validate_name(self, value):
        return value.strip()

    def validate_barcode(self, value):
        return value.strip()

    def validate_manufacturer(self, value):
        return value.strip()

    def validate_generic_name(self, value):
        return value.strip()


class MedicineUpdateSerializer(serializers.ModelSerializer):
    """
    Used for PUT/PATCH — update medicine.
    Identity fields (barcode, name, strength, manufacturer) are
    read-only once the medicine has transaction history.
    That check happens in the service layer.
    """

    class Meta:
        model = Medicine
        fields = [
            'name', 'barcode', 'generic_name', 'manufacturer',
            'strength', 'dosage_form', 'category', 'description',
            'storage_instruction', 'hsn_code', 'gst_percentage', 'status',
        ]

    def validate_name(self, value):
        return value.strip()

    def validate_manufacturer(self, value):
        return value.strip()


class MedicineListSerializer(serializers.ModelSerializer):
    """Compact serializer for list views."""

    class Meta:
        model = Medicine
        fields = [
            'id', 'name', 'barcode', 'generic_name', 'manufacturer',
            'strength', 'dosage_form', 'category', 'status',
            'gst_percentage', 'created_at',
        ]


class MedicineDetailSerializer(serializers.ModelSerializer):
    """Full serializer for detail/retrieve views."""

    class Meta:
        model = Medicine
        fields = '__all__'
