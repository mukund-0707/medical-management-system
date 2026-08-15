"""
Sales Serializers.
"""

from rest_framework import serializers
from .models import Sale, SaleItem
from .constants import PaymentMode


class CheckoutSerializer(serializers.Serializer):
    """Input for checkout — session ID + payment mode."""
    session_id = serializers.UUIDField()
    payment_mode = serializers.ChoiceField(choices=PaymentMode.CHOICES)
    remarks = serializers.CharField(required=False, allow_blank=True, default='')


class SaleItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    batch_number = serializers.CharField(
        source='inventory_batch.batch_number', read_only=True, default=''
    )

    class Meta:
        model = SaleItem
        fields = [
            'id', 'medicine', 'medicine_name', 'batch_number',
            'quantity', 'unit_price', 'discount_percentage',
            'gst_percentage', 'line_total',
        ]


class SaleListSerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = [
            'id', 'invoice_number', 'sale_date', 'payment_mode',
            'grand_total', 'status', 'item_count', 'created_at',
        ]

    def get_item_count(self, obj):
        return obj.items.count()


class SaleDetailSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = [
            'id', 'invoice_number', 'sale_date', 'payment_mode',
            'subtotal', 'discount_amount', 'gst_amount', 'grand_total',
            'status', 'remarks', 'billing_session_id',
            'items', 'created_at', 'updated_at', 'cancelled_at', 'created_by',
        ]
