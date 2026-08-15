"""
Inventory Serializers.
"""

from rest_framework import serializers
from .models import InventoryBatch, InventoryLedger
from .constants import AdjustmentReason


class InventoryBatchSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    medicine_barcode = serializers.CharField(source='medicine.barcode', read_only=True)
    total_available = serializers.SerializerMethodField()

    class Meta:
        model = InventoryBatch
        fields = [
            'id', 'medicine', 'medicine_name', 'medicine_barcode',
            'batch_number', 'expiry_date',
            'purchase_price', 'mrp', 'gst_percentage',
            'quantity', 'damaged_quantity', 'expired_quantity',
            'status', 'total_available',
            'created_at', 'updated_at',
        ]

    def get_total_available(self, obj):
        from .selectors.inventory_selector import InventorySelector
        return InventorySelector.get_total_available_quantity(str(obj.medicine_id))


class InventoryLedgerSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    batch_number = serializers.CharField(source='inventory_batch.batch_number', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = InventoryLedger
        fields = [
            'id', 'medicine', 'medicine_name', 'batch_number',
            'movement_type', 'quantity', 'quantity_before', 'quantity_after',
            'reference_id', 'reference_type', 'reason',
            'created_at', 'created_by', 'created_by_username',
        ]


class AdjustmentSerializer(serializers.Serializer):
    """Input for manual stock adjustment."""
    batch_id = serializers.UUIDField()
    new_quantity = serializers.IntegerField(min_value=0)
    reason = serializers.CharField(min_length=3, max_length=500)
    adjustment_reason_code = serializers.ChoiceField(choices=AdjustmentReason.CHOICES)
