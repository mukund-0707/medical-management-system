"""
Billing Session Serializers.
"""

from rest_framework import serializers
from .models import BillingSession, BillingSessionItem


class BillingSessionItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    medicine_barcode = serializers.CharField(source='medicine.barcode', read_only=True)

    class Meta:
        model = BillingSessionItem
        fields = [
            'id', 'medicine', 'medicine_name', 'medicine_barcode',
            'quantity', 'unit_price', 'discount_percentage',
            'gst_percentage', 'line_total',
        ]


class BillingSessionSerializer(serializers.ModelSerializer):
    items = BillingSessionItemSerializer(many=True, read_only=True)
    item_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = BillingSession
        fields = [
            'id', 'status', 'item_count',
            'subtotal', 'discount_amount', 'gst_amount', 'grand_total',
            'items', 'created_at', 'updated_at',
        ]


class AddItemSerializer(serializers.Serializer):
    """Input for adding a medicine to the session."""
    medicine_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)
    discount_percentage = serializers.DecimalField(
        max_digits=5, decimal_places=2, default=0, required=False
    )


class UpdateItemSerializer(serializers.Serializer):
    """Input for updating quantity of an existing item."""
    quantity = serializers.IntegerField(min_value=1)
    discount_percentage = serializers.DecimalField(
        max_digits=5, decimal_places=2, required=False
    )
