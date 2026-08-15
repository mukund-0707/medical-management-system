"""
Purchase Serializers.
Input validation and output formatting only.
No business logic here.
"""

from datetime import date
from rest_framework import serializers
from .models import Purchase, PurchaseItem


class PurchaseItemCreateSerializer(serializers.Serializer):
    """Validates a single item inside a purchase."""
    medicine_id = serializers.UUIDField()
    batch_number = serializers.CharField(max_length=100)
    expiry_date = serializers.DateField()
    purchase_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    mrp = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(min_value=1)
    gst_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, default=0)

    def validate_batch_number(self, value):
        return value.strip().upper()

    def validate_expiry_date(self, value):
        if value <= date.today():
            raise serializers.ValidationError('Expiry date must be in the future.')
        return value

    def validate_purchase_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Purchase price must be greater than 0.')
        return value

    def validate_mrp(self, value):
        if value <= 0:
            raise serializers.ValidationError('MRP must be greater than 0.')
        return value


class PurchaseCreateSerializer(serializers.Serializer):
    """Validates purchase header + items together."""
    supplier_id = serializers.UUIDField()
    invoice_number = serializers.CharField(max_length=100)
    invoice_date = serializers.DateField()
    remarks = serializers.CharField(required=False, allow_blank=True, default='')
    items = PurchaseItemCreateSerializer(many=True, min_length=1)

    def validate_invoice_number(self, value):
        return value.strip().upper()

    def validate_items(self, items):
        # Check duplicate batch numbers within same request
        batch_numbers = [item['batch_number'].strip().upper() for item in items]
        if len(batch_numbers) != len(set(batch_numbers)):
            raise serializers.ValidationError(
                'Duplicate batch numbers found in the same purchase.'
            )
        return items


class PurchaseUpdateSerializer(serializers.Serializer):
    """Allows updating only draft purchases."""
    invoice_number = serializers.CharField(max_length=100, required=False)
    invoice_date = serializers.DateField(required=False)
    remarks = serializers.CharField(required=False, allow_blank=True)

    def validate_invoice_number(self, value):
        return value.strip().upper()


# ── Output Serializers ────────────────────────────────────────

class PurchaseItemDetailSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    medicine_barcode = serializers.CharField(source='medicine.barcode', read_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = PurchaseItem
        fields = [
            'id', 'medicine', 'medicine_name', 'medicine_barcode',
            'batch_number', 'expiry_date',
            'purchase_price', 'mrp', 'gst_percentage', 'discount_percentage',
            'quantity', 'total_amount', 'created_at',
        ]


class PurchaseListSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = [
            'id', 'supplier', 'supplier_name', 'invoice_number',
            'invoice_date', 'status', 'item_count', 'created_at',
        ]

    def get_item_count(self, obj):
        return obj.items.count()


class PurchaseDetailSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    items = PurchaseItemDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Purchase
        fields = [
            'id', 'supplier', 'supplier_name', 'invoice_number',
            'invoice_date', 'remarks', 'status',
            'items', 'created_at', 'updated_at',
            'finalized_at', 'cancelled_at', 'created_by',
        ]
