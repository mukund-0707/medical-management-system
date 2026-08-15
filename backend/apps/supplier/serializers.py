"""
Supplier Serializers.
Input validation and output formatting only.
No business logic here.
"""

import re
from rest_framework import serializers
from .models import Supplier


class SupplierCreateSerializer(serializers.ModelSerializer):
    """Used for POST — create new supplier."""

    class Meta:
        model = Supplier
        fields = [
            'name', 'mobile', 'email', 'contact_person',
            'gst_number', 'drug_license_number',
            'address', 'city', 'state', 'pincode', 'remarks',
        ]

    def validate_name(self, value):
        return value.strip()

    def validate_mobile(self, value):
        value = value.strip()
        if not re.match(r'^\+?[\d\s\-]{7,15}$', value):
            raise serializers.ValidationError('Enter a valid mobile number.')
        return value

    def validate_gst_number(self, value):
        value = value.strip().upper()
        if value and not re.match(r'^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$', value):
            raise serializers.ValidationError('Enter a valid GST number (e.g. 27AAPFU0939F1ZV).')
        return value

    def validate_email(self, value):
        return value.strip().lower()

    def validate_address(self, value):
        return value.strip()


class SupplierUpdateSerializer(serializers.ModelSerializer):
    """Used for PUT/PATCH — update supplier details."""

    class Meta:
        model = Supplier
        fields = [
            'name', 'mobile', 'email', 'contact_person',
            'gst_number', 'drug_license_number',
            'address', 'city', 'state', 'pincode',
            'remarks', 'status',
        ]

    def validate_mobile(self, value):
        value = value.strip()
        if not re.match(r'^\+?[\d\s\-]{7,15}$', value):
            raise serializers.ValidationError('Enter a valid mobile number.')
        return value

    def validate_gst_number(self, value):
        value = value.strip().upper()
        if value and not re.match(r'^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$', value):
            raise serializers.ValidationError('Enter a valid GST number.')
        return value


class SupplierListSerializer(serializers.ModelSerializer):
    """Compact serializer for list views."""

    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'mobile', 'email', 'contact_person',
            'gst_number', 'city', 'status', 'created_at',
        ]


class SupplierDetailSerializer(serializers.ModelSerializer):
    """Full serializer for detail/retrieve views."""

    class Meta:
        model = Supplier
        fields = '__all__'
