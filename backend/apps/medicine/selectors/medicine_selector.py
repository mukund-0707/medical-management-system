"""
Medicine Selectors.
Read-only database queries for Medicine module.
Selectors never update, create, or delete data.
"""

from django.db.models import Q
from ..models import Medicine
from ..constants import MedicineStatus


class MedicineSelector:

    @staticmethod
    def get_all(status=None):
        """Return all medicines, optionally filtered by status."""
        qs = Medicine.objects.all()
        if status:
            qs = qs.filter(status=status)
        return qs

    @staticmethod
    def get_by_id(medicine_id: str) -> Medicine | None:
        """Return medicine by UUID, or None."""
        try:
            return Medicine.objects.get(id=medicine_id)
        except Medicine.DoesNotExist:
            return None

    @staticmethod
    def get_by_barcode(barcode: str) -> Medicine | None:
        """Fast indexed lookup by barcode."""
        try:
            return Medicine.objects.get(barcode=barcode.strip())
        except Medicine.DoesNotExist:
            return None

    @staticmethod
    def search(query: str):
        """
        Search medicines by name, generic name, barcode, or manufacturer.
        Case-insensitive, partial match.
        """
        if not query:
            return Medicine.objects.all()

        return Medicine.objects.filter(
            Q(name__icontains=query) |
            Q(generic_name__icontains=query) |
            Q(barcode__icontains=query) |
            Q(manufacturer__icontains=query) |
            Q(category__icontains=query)
        )

    @staticmethod
    def barcode_exists(barcode: str, exclude_id=None) -> bool:
        """Check if barcode already exists (for duplicate validation)."""
        qs = Medicine.objects.filter(barcode=barcode.strip())
        if exclude_id:
            qs = qs.exclude(id=exclude_id)
        return qs.exists()

    @staticmethod
    def has_transaction_history(medicine_id: str) -> bool:
        """
        Check if medicine has any purchase or sale history.
        Used to determine if identity fields are locked.
        """
        from apps.purchase.models import PurchaseItem
        return PurchaseItem.objects.filter(medicine_id=medicine_id).exists()
