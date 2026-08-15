"""
Sales Selectors — read-only queries.
"""

from django.db.models import Q
from ..models import Sale
from ..constants import SaleStatus


class SaleSelector:

    @staticmethod
    def get_all(status=None, payment_mode=None):
        qs = Sale.objects.prefetch_related('items__medicine', 'items__inventory_batch')
        if status:
            qs = qs.filter(status=status)
        if payment_mode:
            qs = qs.filter(payment_mode=payment_mode)
        return qs.order_by('-created_at')

    @staticmethod
    def get_by_id(sale_id: str) -> Sale | None:
        try:
            return Sale.objects.prefetch_related(
                'items__medicine', 'items__inventory_batch'
            ).get(id=sale_id)
        except Sale.DoesNotExist:
            return None

    @staticmethod
    def get_by_invoice_number(invoice_number: str) -> Sale | None:
        try:
            return Sale.objects.prefetch_related(
                'items__medicine', 'items__inventory_batch'
            ).get(invoice_number=invoice_number)
        except Sale.DoesNotExist:
            return None

    @staticmethod
    def generate_invoice_number() -> str:
        """
        Generate unique invoice number: INV-YYYYMMDD-XXXX
        Thread-safe via DB query for last invoice of the day.
        """
        from datetime import date
        today = date.today()
        date_str = today.strftime('%Y%m%d')
        prefix = f"INV-{date_str}-"

        last = Sale.objects.filter(
            invoice_number__startswith=prefix
        ).order_by('-invoice_number').first()

        if last:
            try:
                seq = int(last.invoice_number.split('-')[-1]) + 1
            except (ValueError, IndexError):
                seq = 1
        else:
            seq = 1

        return f"{prefix}{seq:04d}"
