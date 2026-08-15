"""
Dashboard Service — read-only aggregated queries.
No data modification here — ever.

Provides:
- KPI cards (today's sales, purchases, inventory value, etc.)
- Alerts (low stock, expiring, expired)
- Sales summary
- Purchase summary
- Inventory summary
- Recent activity
"""

import logging
from datetime import date, timedelta
from decimal import Decimal

from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone

logger = logging.getLogger('apps.dashboard')


class DashboardService:

    # ─────────────────────────────────────────────
    # Main KPI Summary
    # ─────────────────────────────────────────────

    @staticmethod
    def get_kpi_summary(filter_date: date = None) -> dict:
        """
        Top KPI cards for dashboard.
        filter_date defaults to today.
        """
        from apps.sales.models import Sale
        from apps.purchase.models import Purchase
        from apps.inventory.models import InventoryBatch
        from apps.medicine.models import Medicine
        from apps.inventory.constants import BatchStatus, LOW_STOCK_THRESHOLD
        from apps.sales.constants import SaleStatus
        from apps.purchase.constants import PurchaseStatus

        target_date = filter_date or date.today()

        # Today's sales
        todays_sales = Sale.objects.filter(
            sale_date=target_date,
            status=SaleStatus.COMPLETED,
        ).aggregate(
            total_amount=Sum('grand_total'),
            invoice_count=Count('id'),
        )

        # Today's purchases
        todays_purchases = Purchase.objects.filter(
            invoice_date=target_date,
            status=PurchaseStatus.FINALIZED,
        ).aggregate(
            count=Count('id'),
        )

        # Inventory stats
        available_batches = InventoryBatch.objects.filter(
            status=BatchStatus.AVAILABLE,
            quantity__gt=0,
        )
        inventory_value = available_batches.aggregate(
            total=Sum('mrp' * 1)  # fallback
        )

        # Calculate inventory value properly
        inv_value = Decimal('0')
        for batch in available_batches.values('mrp', 'quantity'):
            inv_value += Decimal(str(batch['mrp'])) * batch['quantity']

        # Counts
        total_medicines = Medicine.objects.filter(status='active').count()
        low_stock_count = InventoryBatch.objects.filter(
            status=BatchStatus.AVAILABLE,
            quantity__lte=LOW_STOCK_THRESHOLD,
            quantity__gt=0,
        ).count()

        expired_count = InventoryBatch.objects.filter(
            expiry_date__lt=target_date,
            status=BatchStatus.AVAILABLE,
            quantity__gt=0,
        ).count()

        out_of_stock_count = InventoryBatch.objects.filter(
            status=BatchStatus.EXHAUSTED,
        ).values('medicine').distinct().count()

        return {
            'date': target_date.isoformat(),
            'sales': {
                'today_total': todays_sales['total_amount'] or Decimal('0'),
                'today_invoice_count': todays_sales['invoice_count'] or 0,
            },
            'purchases': {
                'today_count': todays_purchases['count'] or 0,
            },
            'inventory': {
                'total_active_medicines': total_medicines,
                'inventory_value': inv_value,
                'low_stock_count': low_stock_count,
                'expired_batch_count': expired_count,
                'out_of_stock_count': out_of_stock_count,
            },
        }

    # ─────────────────────────────────────────────
    # Sales Summary
    # ─────────────────────────────────────────────

    @staticmethod
    def get_sales_summary(date_from: date = None, date_to: date = None) -> dict:
        """Sales summary for a date range. Defaults to today."""
        from apps.sales.models import Sale, SaleItem
        from apps.sales.constants import SaleStatus

        today = date.today()
        date_from = date_from or today
        date_to = date_to or today

        sales = Sale.objects.filter(
            sale_date__gte=date_from,
            sale_date__lte=date_to,
            status=SaleStatus.COMPLETED,
        )

        aggregates = sales.aggregate(
            total_amount=Sum('grand_total'),
            total_discount=Sum('discount_amount'),
            total_gst=Sum('gst_amount'),
            invoice_count=Count('id'),
        )

        # Top selling medicines in range
        top_medicines = SaleItem.objects.filter(
            sale__sale_date__gte=date_from,
            sale__sale_date__lte=date_to,
            sale__status=SaleStatus.COMPLETED,
        ).values(
            'medicine__id', 'medicine__name'
        ).annotate(
            total_qty=Sum('quantity'),
            total_amount=Sum('line_total'),
        ).order_by('-total_qty')[:5]

        # Recent sales (last 10)
        recent = sales.order_by('-created_at')[:10].values(
            'id', 'invoice_number', 'sale_date',
            'grand_total', 'payment_mode', 'created_at',
        )

        return {
            'date_from': date_from.isoformat(),
            'date_to': date_to.isoformat(),
            'total_amount': aggregates['total_amount'] or Decimal('0'),
            'total_discount': aggregates['total_discount'] or Decimal('0'),
            'total_gst': aggregates['total_gst'] or Decimal('0'),
            'invoice_count': aggregates['invoice_count'] or 0,
            'top_medicines': list(top_medicines),
            'recent_sales': list(recent),
        }

    # ─────────────────────────────────────────────
    # Purchase Summary
    # ─────────────────────────────────────────────

    @staticmethod
    def get_purchase_summary(date_from: date = None, date_to: date = None) -> dict:
        """Purchase summary for a date range."""
        from apps.purchase.models import Purchase
        from apps.purchase.constants import PurchaseStatus

        today = date.today()
        date_from = date_from or today
        date_to = date_to or today

        purchases = Purchase.objects.filter(
            invoice_date__gte=date_from,
            invoice_date__lte=date_to,
            status=PurchaseStatus.FINALIZED,
        ).select_related('supplier')

        count = purchases.count()

        recent = purchases.order_by('-created_at')[:10].values(
            'id', 'invoice_number', 'invoice_date',
            'supplier__name', 'status', 'created_at',
        )

        return {
            'date_from': date_from.isoformat(),
            'date_to': date_to.isoformat(),
            'finalized_count': count,
            'recent_purchases': list(recent),
        }

    # ─────────────────────────────────────────────
    # Inventory Summary
    # ─────────────────────────────────────────────

    @staticmethod
    def get_inventory_summary() -> dict:
        """Current inventory state summary."""
        from apps.inventory.models import InventoryBatch
        from apps.inventory.constants import BatchStatus, LOW_STOCK_THRESHOLD

        today = date.today()
        expiry_30 = today + timedelta(days=30)
        expiry_60 = today + timedelta(days=60)

        totals = InventoryBatch.objects.aggregate(
            available_batches=Count('id', filter=Q(status=BatchStatus.AVAILABLE, quantity__gt=0)),
            expired_batches=Count('id', filter=Q(status=BatchStatus.EXPIRED)),
            damaged_batches=Count('id', filter=Q(status=BatchStatus.DAMAGED)),
            exhausted_batches=Count('id', filter=Q(status=BatchStatus.EXHAUSTED)),
        )

        low_stock = InventoryBatch.objects.filter(
            status=BatchStatus.AVAILABLE,
            quantity__lte=LOW_STOCK_THRESHOLD,
            quantity__gt=0,
        ).select_related('medicine').values(
            'medicine__id', 'medicine__name', 'batch_number', 'quantity', 'expiry_date'
        ).order_by('quantity')[:20]

        expiring_soon = InventoryBatch.objects.filter(
            status=BatchStatus.AVAILABLE,
            quantity__gt=0,
            expiry_date__lte=expiry_30,
            expiry_date__gte=today,
        ).select_related('medicine').values(
            'medicine__id', 'medicine__name', 'batch_number', 'quantity', 'expiry_date'
        ).order_by('expiry_date')[:20]

        expired = InventoryBatch.objects.filter(
            expiry_date__lt=today,
            status=BatchStatus.AVAILABLE,
            quantity__gt=0,
        ).select_related('medicine').values(
            'medicine__id', 'medicine__name', 'batch_number', 'quantity', 'expiry_date'
        ).order_by('expiry_date')[:20]

        return {
            'batch_counts': totals,
            'low_stock_medicines': list(low_stock),
            'expiring_in_30_days': list(expiring_soon),
            'expired_with_stock': list(expired),
        }

    # ─────────────────────────────────────────────
    # Alerts
    # ─────────────────────────────────────────────

    @staticmethod
    def get_alerts() -> dict:
        """Priority-sorted alerts for dashboard banner."""
        from apps.inventory.models import InventoryBatch
        from apps.inventory.constants import BatchStatus, LOW_STOCK_THRESHOLD

        today = date.today()
        expiry_threshold = today + timedelta(days=30)

        expired_count = InventoryBatch.objects.filter(
            expiry_date__lt=today,
            status=BatchStatus.AVAILABLE,
            quantity__gt=0,
        ).count()

        expiring_count = InventoryBatch.objects.filter(
            status=BatchStatus.AVAILABLE,
            quantity__gt=0,
            expiry_date__lte=expiry_threshold,
            expiry_date__gte=today,
        ).count()

        low_stock_count = InventoryBatch.objects.filter(
            status=BatchStatus.AVAILABLE,
            quantity__lte=LOW_STOCK_THRESHOLD,
            quantity__gt=0,
        ).count()

        alerts = []

        if expired_count:
            alerts.append({
                'type': 'error',
                'priority': 1,
                'title': 'Expired Medicines',
                'message': f'{expired_count} batch(es) have expired and still have stock.',
                'count': expired_count,
            })

        if expiring_count:
            alerts.append({
                'type': 'warning',
                'priority': 2,
                'title': 'Expiring Soon',
                'message': f'{expiring_count} batch(es) expiring within 30 days.',
                'count': expiring_count,
            })

        if low_stock_count:
            alerts.append({
                'type': 'warning',
                'priority': 3,
                'title': 'Low Stock',
                'message': f'{low_stock_count} medicine(s) are running low on stock.',
                'count': low_stock_count,
            })

        # Sort by priority
        alerts.sort(key=lambda x: x['priority'])

        return {
            'total_alerts': len(alerts),
            'alerts': alerts,
        }
