"""
Inventory Selectors — read-only queries.
All stock reads go through here.
Never update data in selectors.
"""

from datetime import date
from django.db.models import Sum, Q
from ..models import InventoryBatch, InventoryLedger
from ..constants import BatchStatus, LOW_STOCK_THRESHOLD


class InventorySelector:

    # ─────────────────────────────────────────────
    # Batch queries
    # ─────────────────────────────────────────────

    @staticmethod
    def get_available_batches(medicine_id: str):
        """
        Return available batches for a medicine ordered by expiry (FEFO).
        Only batches with quantity > 0 and status = AVAILABLE.
        """
        return InventoryBatch.objects.filter(
            medicine_id=medicine_id,
            status=BatchStatus.AVAILABLE,
            quantity__gt=0,
        ).order_by('expiry_date', 'created_at')   # FEFO — nearest expiry first

    @staticmethod
    def get_total_available_quantity(medicine_id: str) -> int:
        """Total available quantity across all batches for a medicine."""
        result = InventoryBatch.objects.filter(
            medicine_id=medicine_id,
            status=BatchStatus.AVAILABLE,
            quantity__gt=0,
        ).aggregate(total=Sum('quantity'))
        return result['total'] or 0

    @staticmethod
    def get_batch_by_id(batch_id: str) -> InventoryBatch | None:
        try:
            return InventoryBatch.objects.select_related('medicine').get(id=batch_id)
        except InventoryBatch.DoesNotExist:
            return None

    @staticmethod
    def get_batches_for_medicine(medicine_id: str):
        """All batches (all statuses) for a medicine."""
        return InventoryBatch.objects.filter(
            medicine_id=medicine_id
        ).select_related('medicine').order_by('expiry_date')

    @staticmethod
    def get_all_batches(status=None, medicine_id=None):
        qs = InventoryBatch.objects.select_related('medicine')
        if status:
            qs = qs.filter(status=status)
        if medicine_id:
            qs = qs.filter(medicine_id=medicine_id)
        return qs

    @staticmethod
    def get_low_stock_batches():
        """Batches where quantity <= LOW_STOCK_THRESHOLD."""
        return InventoryBatch.objects.filter(
            status=BatchStatus.AVAILABLE,
            quantity__lte=LOW_STOCK_THRESHOLD,
            quantity__gt=0,
        ).select_related('medicine').order_by('quantity')

    @staticmethod
    def get_expiring_soon(days: int = 30):
        """Batches expiring within given days."""
        from datetime import timedelta
        threshold = date.today() + timedelta(days=days)
        return InventoryBatch.objects.filter(
            status=BatchStatus.AVAILABLE,
            quantity__gt=0,
            expiry_date__lte=threshold,
            expiry_date__gte=date.today(),
        ).select_related('medicine').order_by('expiry_date')

    @staticmethod
    def get_expired_batches():
        """Batches that are past expiry date but still have quantity."""
        return InventoryBatch.objects.filter(
            expiry_date__lt=date.today(),
            status=BatchStatus.AVAILABLE,
            quantity__gt=0,
        ).select_related('medicine').order_by('expiry_date')

    @staticmethod
    def batch_has_sales(batch_number: str, medicine_id: str) -> bool:
        """
        Check if any sale has consumed from this batch.
        Used by purchase cancellation check.
        """
        from apps.inventory.constants import LedgerMovementType
        return InventoryLedger.objects.filter(
            inventory_batch__batch_number=batch_number,
            inventory_batch__medicine_id=medicine_id,
            movement_type=LedgerMovementType.SALE,
        ).exists()

    # ─────────────────────────────────────────────
    # Ledger queries
    # ─────────────────────────────────────────────

    @staticmethod
    def get_ledger_for_batch(batch_id: str):
        """Full movement history for a batch."""
        return InventoryLedger.objects.filter(
            inventory_batch_id=batch_id
        ).select_related('medicine', 'created_by').order_by('-created_at')

    @staticmethod
    def get_ledger_for_medicine(medicine_id: str):
        """Full movement history for a medicine across all batches."""
        return InventoryLedger.objects.filter(
            medicine_id=medicine_id
        ).select_related('inventory_batch', 'created_by').order_by('-created_at')

    @staticmethod
    def get_all_ledger(movement_type=None):
        qs = InventoryLedger.objects.select_related(
            'medicine', 'inventory_batch', 'created_by'
        )
        if movement_type:
            qs = qs.filter(movement_type=movement_type)
        return qs.order_by('-created_at')
