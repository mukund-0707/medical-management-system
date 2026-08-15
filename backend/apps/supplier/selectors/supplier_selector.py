"""
Supplier Selectors.
Read-only database queries. Never update data here.
"""

from django.db.models import Q
from ..models import Supplier
from ..constants import SupplierStatus


class SupplierSelector:

    @staticmethod
    def get_all(status=None):
        """Return all suppliers, optionally filtered by status."""
        qs = Supplier.objects.all()
        if status:
            qs = qs.filter(status=status)
        return qs

    @staticmethod
    def get_by_id(supplier_id: str) -> Supplier | None:
        """Return supplier by UUID, or None."""
        try:
            return Supplier.objects.get(id=supplier_id)
        except Supplier.DoesNotExist:
            return None

    @staticmethod
    def search(query: str):
        """
        Search suppliers by name, mobile, gst_number, contact_person.
        Case-insensitive partial match.
        """
        if not query:
            return Supplier.objects.all()

        return Supplier.objects.filter(
            Q(name__icontains=query) |
            Q(mobile__icontains=query) |
            Q(gst_number__icontains=query) |
            Q(contact_person__icontains=query) |
            Q(city__icontains=query)
        )

    @staticmethod
    def gst_exists(gst_number: str, exclude_id=None) -> bool:
        """Check if GST number already exists (for duplicate validation)."""
        if not gst_number:
            return False
        qs = Supplier.objects.filter(gst_number=gst_number.strip().upper())
        if exclude_id:
            qs = qs.exclude(id=exclude_id)
        return qs.exists()

    @staticmethod
    def mobile_exists(mobile: str, exclude_id=None) -> bool:
        """Check if mobile number already exists."""
        qs = Supplier.objects.filter(mobile=mobile.strip())
        if exclude_id:
            qs = qs.exclude(id=exclude_id)
        return qs.exists()

    @staticmethod
    def has_purchase_history(supplier_id: str) -> bool:
        """Check if supplier has any purchase history."""
        from apps.purchase.models import Purchase
        return Purchase.objects.filter(supplier_id=supplier_id).exists()
