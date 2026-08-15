"""
Reports Service — read-only historical reports.
No data is ever modified here.

Available reports:
- Sales Report
- Purchase Report
- Inventory Report
- Stock Ledger Report
- Low Stock Report
- Expiry Report
- Adjustment Report
- Medicine Report
- Supplier Report
"""

import logging
from datetime import date, timedelta

from django.db.models import Q, Sum, Count

logger = logging.getLogger('apps.reports')


class ReportsService:

    # ─────────────────────────────────────────────
    # Sales Report
    # ─────────────────────────────────────────────

    @staticmethod
    def get_sales_report(
        date_from: date = None,
        date_to: date = None,
        payment_mode: str = None,
        status: str = None,
        search: str = None,
    ):
        """
        Sales report — all completed/cancelled sales in a date range.
        Returns queryset for pagination in view.
        """
        from apps.sales.models import Sale

        qs = Sale.objects.prefetch_related(
            'items__medicine'
        ).select_related('created_by')

        if date_from:
            qs = qs.filter(sale_date__gte=date_from)
        if date_to:
            qs = qs.filter(sale_date__lte=date_to)
        if payment_mode:
            qs = qs.filter(payment_mode=payment_mode)
        if status:
            qs = qs.filter(status=status)
        if search:
            qs = qs.filter(invoice_number__icontains=search)

        return qs.order_by('-sale_date', '-created_at')

    # ─────────────────────────────────────────────
    # Purchase Report
    # ─────────────────────────────────────────────

    @staticmethod
    def get_purchase_report(
        date_from: date = None,
        date_to: date = None,
        supplier_id: str = None,
        status: str = None,
        search: str = None,
    ):
        """Purchase report — all purchases in a date range."""
        from apps.purchase.models import Purchase

        qs = Purchase.objects.select_related(
            'supplier', 'created_by'
        ).prefetch_related('items__medicine')

        if date_from:
            qs = qs.filter(invoice_date__gte=date_from)
        if date_to:
            qs = qs.filter(invoice_date__lte=date_to)
        if supplier_id:
            qs = qs.filter(supplier_id=supplier_id)
        if status:
            qs = qs.filter(status=status)
        if search:
            qs = qs.filter(invoice_number__icontains=search)

        return qs.order_by('-invoice_date', '-created_at')

    # ─────────────────────────────────────────────
    # Inventory Report
    # ─────────────────────────────────────────────

    @staticmethod
    def get_inventory_report(
        medicine_id: str = None,
        status: str = None,
        batch_number: str = None,
    ):
        """Current inventory snapshot — all batches."""
        from apps.inventory.models import InventoryBatch

        qs = InventoryBatch.objects.select_related('medicine')

        if medicine_id:
            qs = qs.filter(medicine_id=medicine_id)
        if status:
            qs = qs.filter(status=status)
        if batch_number:
            qs = qs.filter(batch_number__icontains=batch_number)

        return qs.order_by('medicine__name', 'expiry_date')

    # ─────────────────────────────────────────────
    # Ledger (Stock Movement) Report
    # ─────────────────────────────────────────────

    @staticmethod
    def get_ledger_report(
        medicine_id: str = None,
        movement_type: str = None,
        date_from: date = None,
        date_to: date = None,
        batch_number: str = None,
    ):
        """Full stock movement history from InventoryLedger."""
        from apps.inventory.models import InventoryLedger

        qs = InventoryLedger.objects.select_related(
            'medicine', 'inventory_batch', 'created_by'
        )

        if medicine_id:
            qs = qs.filter(medicine_id=medicine_id)
        if movement_type:
            qs = qs.filter(movement_type=movement_type)
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)
        if batch_number:
            qs = qs.filter(inventory_batch__batch_number__icontains=batch_number)

        return qs.order_by('-created_at')

    # ─────────────────────────────────────────────
    # Expiry Report
    # ─────────────────────────────────────────────

    @staticmethod
    def get_expiry_report(days: int = 90):
        """
        Batches expiring within given days + already expired with stock.
        days=0 means only already expired.
        """
        from apps.inventory.models import InventoryBatch
        from apps.inventory.constants import BatchStatus

        today = date.today()
        threshold = today + timedelta(days=days)

        qs = InventoryBatch.objects.filter(
            quantity__gt=0,
        ).filter(
            Q(expiry_date__lt=today, status=BatchStatus.AVAILABLE) |  # expired
            Q(expiry_date__gte=today, expiry_date__lte=threshold, status=BatchStatus.AVAILABLE)  # expiring
        ).select_related('medicine').order_by('expiry_date')

        return qs

    # ─────────────────────────────────────────────
    # Low Stock Report
    # ─────────────────────────────────────────────

    @staticmethod
    def get_low_stock_report(threshold: int = None):
        """All available batches where quantity <= threshold."""
        from apps.inventory.models import InventoryBatch
        from apps.inventory.constants import BatchStatus, LOW_STOCK_THRESHOLD

        limit = threshold if threshold is not None else LOW_STOCK_THRESHOLD

        return InventoryBatch.objects.filter(
            status=BatchStatus.AVAILABLE,
            quantity__lte=limit,
            quantity__gt=0,
        ).select_related('medicine').order_by('quantity', 'expiry_date')

    # ─────────────────────────────────────────────
    # Adjustment Report
    # ─────────────────────────────────────────────

    @staticmethod
    def get_adjustment_report(
        medicine_id: str = None,
        date_from: date = None,
        date_to: date = None,
    ):
        """All manual adjustment ledger entries."""
        from apps.inventory.models import InventoryLedger
        from apps.inventory.constants import LedgerMovementType

        qs = InventoryLedger.objects.filter(
            movement_type=LedgerMovementType.ADJUSTMENT
        ).select_related('medicine', 'inventory_batch', 'created_by')

        if medicine_id:
            qs = qs.filter(medicine_id=medicine_id)
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)

        return qs.order_by('-created_at')

    # ─────────────────────────────────────────────
    # Medicine Report
    # ─────────────────────────────────────────────

    @staticmethod
    def get_medicine_report(status: str = None, search: str = None):
        """Medicine master list with current stock summary."""
        from apps.medicine.models import Medicine

        qs = Medicine.objects.all()

        if status:
            qs = qs.filter(status=status)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(generic_name__icontains=search) |
                Q(barcode__icontains=search) |
                Q(manufacturer__icontains=search)
            )

        return qs.order_by('name')

    # ─────────────────────────────────────────────
    # Supplier Report
    # ─────────────────────────────────────────────

    @staticmethod
    def get_supplier_report(status: str = None, search: str = None):
        """Supplier list with purchase counts."""
        from apps.supplier.models import Supplier

        qs = Supplier.objects.annotate(
            purchase_count=Count('purchases'),
        )

        if status:
            qs = qs.filter(status=status)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(mobile__icontains=search) |
                Q(gst_number__icontains=search)
            )

        return qs.order_by('name')
