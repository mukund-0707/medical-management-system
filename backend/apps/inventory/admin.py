from django.contrib import admin
from .models import InventoryBatch, InventoryLedger


@admin.register(InventoryBatch)
class InventoryBatchAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'batch_number', 'expiry_date', 'quantity', 'status', 'mrp']
    list_filter = ['status', 'expiry_date']
    search_fields = ['medicine__name', 'batch_number']
    readonly_fields = ['id', 'created_at', 'updated_at', 'purchase_item']
    ordering = ['expiry_date']


@admin.register(InventoryLedger)
class InventoryLedgerAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'movement_type', 'quantity', 'quantity_before', 'quantity_after', 'created_at']
    list_filter = ['movement_type', 'created_at']
    search_fields = ['medicine__name', 'reference_id']
    readonly_fields = list(
        ['id', 'inventory_batch', 'medicine', 'movement_type',
         'quantity', 'quantity_before', 'quantity_after',
         'reference_id', 'reference_type', 'reason',
         'created_at', 'created_by']
    )

    def has_add_permission(self, request):
        return False   # Ledger is append-only

    def has_change_permission(self, request, obj=None):
        return False   # Ledger is immutable

    def has_delete_permission(self, request, obj=None):
        return False   # Ledger is never deleted
