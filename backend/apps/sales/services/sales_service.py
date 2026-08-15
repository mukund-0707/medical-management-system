"""
Sales Service — converts BillingSession into a completed Sale.

Checkout flow (all inside ONE transaction):
  1. Validate session
  2. Validate stock (double-check)
  3. Generate invoice number
  4. Create Sale header
  5. For each cart item → reduce inventory (FEFO) → create SaleItem
  6. Mark billing session as checked_out
  7. Commit

If ANYTHING fails → full rollback.
"""

import logging
from django.db import transaction
from django.utils import timezone

from apps.billing.models import BillingSession
from apps.billing.constants import SessionStatus
from apps.billing.services.billing_service import BillingSessionService
from apps.inventory.services.inventory_service import InventoryService

from ..models import Sale, SaleItem
from ..constants import SaleStatus
from ..selectors.sale_selector import SaleSelector

logger = logging.getLogger('apps.sales')


class SalesService:

    @staticmethod
    @transaction.atomic
    def checkout(session: BillingSession, payment_mode: str,
                 remarks: str, created_by) -> Sale:
        """
        Convert a BillingSession into a completed Sale.

        Steps:
        1. Validate session + stock (double-check)
        2. Generate invoice number
        3. Create Sale
        4. For each item: reduce inventory (FEFO), create SaleItem
        5. Mark session as checked_out

        Raises:
            ValueError: on any validation or business rule failure.
        """

        # ── Step 1: Validate session and stock ────────────────
        BillingSessionService.validate_for_checkout(session)

        items = list(session.items.select_related('medicine').all())

        # ── Step 2: Generate unique invoice number ────────────
        invoice_number = SaleSelector.generate_invoice_number()

        # ── Step 3: Create Sale header ────────────────────────
        sale = Sale.objects.create(
            invoice_number=invoice_number,
            sale_date=timezone.now().date(),
            payment_mode=payment_mode,
            subtotal=session.subtotal,
            discount_amount=session.discount_amount,
            gst_amount=session.gst_amount,
            grand_total=session.grand_total,
            status=SaleStatus.COMPLETED,
            remarks=remarks.strip(),
            billing_session_id=session.id,
            created_by=created_by,
        )

        # ── Step 4: Reduce inventory + create SaleItems ───────
        for cart_item in items:
            deductions = InventoryService.reduce_for_sale(
                medicine_id=str(cart_item.medicine_id),
                quantity=cart_item.quantity,
                sale_id=str(sale.id),
                created_by=created_by,
            )

            # Create one SaleItem per cart item
            # Use the first batch from FEFO deduction as reference
            primary_batch = deductions[0]['batch'] if deductions else None

            SaleItem.objects.create(
                sale=sale,
                medicine=cart_item.medicine,
                inventory_batch=primary_batch,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                discount_percentage=cart_item.discount_percentage,
                gst_percentage=cart_item.gst_percentage,
                line_total=cart_item.line_total,
            )

        # ── Step 5: Mark session as checked out ───────────────
        session.status = SessionStatus.CHECKED_OUT
        session.save(update_fields=['status', 'updated_at'])

        logger.info(
            f"Sale COMPLETED: invoice='{invoice_number}' "
            f"| total={sale.grand_total} | payment={payment_mode} "
            f"| items={len(items)} | by={created_by}"
        )

        return sale

    @staticmethod
    @transaction.atomic
    def cancel_sale(sale: Sale, cancelled_by) -> Sale:
        """
        Cancel a completed sale.
        NOTE: This does NOT reverse inventory in POC.
        Future version will implement customer return workflow.

        Raises:
            ValueError: if sale is already cancelled.
        """
        if sale.is_cancelled:
            raise ValueError('Sale is already cancelled.')

        sale.status = SaleStatus.CANCELLED
        sale.cancelled_at = timezone.now()
        sale.save(update_fields=['status', 'cancelled_at', 'updated_at'])

        logger.info(
            f"Sale CANCELLED: invoice='{sale.invoice_number}' "
            f"| id={sale.id} | by={cancelled_by}"
        )
        return sale
