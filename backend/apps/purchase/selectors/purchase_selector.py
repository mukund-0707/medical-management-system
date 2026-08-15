"""
Purchase Selectors — read-only queries.
"""

from django.db.models import Q
from ..models import Purchase, PurchaseItem
from ..constants import PurchaseStatus


class PurchaseSelector:

    @staticmethod
    def get_all(status=None, supplier_id=None):
        qs = Purchase.objects.select_related('supplier').prefetch_related('items__medicine')
        if status:
            qs = qs.filter(status=status)
        if supplier_id:
            qs = qs.filter(supplier_id=supplier_id)
        return qs

    @staticmethod
    def get_by_id(purchase_id: str) -> Purchase | None:
        try:
            return Purchase.objects.select_related('supplier').prefetch_related(
                'items__medicine'
            ).get(id=purchase_id)
        except Purchase.DoesNotExist:
            return None

    @staticmethod
    def invoice_exists(supplier_id: str, invoice_number: str, exclude_id=None) -> bool:
        """Invoice number uniqueness is per supplier."""
        qs = Purchase.objects.filter(
            supplier_id=supplier_id,
            invoice_number=invoice_number.strip().upper(),
        )
        if exclude_id:
            qs = qs.exclude(id=exclude_id)
        return qs.exists()

    @staticmethod
    def get_finalized_for_medicine(medicine_id: str):
        """All finalized purchase items for a medicine — used by inventory."""
        return PurchaseItem.objects.filter(
            medicine_id=medicine_id,
            purchase__status=PurchaseStatus.FINALIZED,
        ).select_related('purchase', 'medicine')
