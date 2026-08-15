"""
Billing Session Service.
Manages temporary cart operations before checkout.

Rules:
- Session never touches inventory.
- Stock is validated on add AND again on checkout.
- Checkout delegates to SalesService.
- All totals calculated in backend — never trust frontend.
"""

import logging
from decimal import Decimal
from django.db import transaction

from apps.medicine.models import Medicine
from apps.medicine.constants import MedicineStatus
from apps.inventory.selectors.inventory_selector import InventorySelector

from ..models import BillingSession, BillingSessionItem
from ..constants import SessionStatus

logger = logging.getLogger('apps.billing')


class BillingSessionService:

    # ─────────────────────────────────────────────
    # Create Session
    # ─────────────────────────────────────────────

    @staticmethod
    @transaction.atomic
    def create_session(created_by) -> BillingSession:
        """Create a new empty billing session."""
        session = BillingSession.objects.create(
            status=SessionStatus.ACTIVE,
            created_by=created_by,
        )
        logger.info(f"Billing session created: id={session.id} | by={created_by}")
        return session

    # ─────────────────────────────────────────────
    # Add Item
    # ─────────────────────────────────────────────

    @staticmethod
    @transaction.atomic
    def add_item(session: BillingSession, medicine_id: str,
                 quantity: int, discount_percentage: Decimal = Decimal('0')) -> BillingSessionItem:
        """
        Add a medicine to the session.
        If medicine already exists → increase quantity.

        Rules:
        - Session must be ACTIVE.
        - Medicine must be ACTIVE.
        - Stock must be available.

        Raises:
            ValueError: on any rule violation.
        """
        if not session.is_active:
            raise ValueError('Session is not active.')

        try:
            medicine = Medicine.objects.get(id=medicine_id)
        except Medicine.DoesNotExist:
            raise ValueError('Medicine not found.')

        if medicine.status != MedicineStatus.ACTIVE:
            raise ValueError(f"Medicine '{medicine.name}' is inactive and cannot be billed.")

        # Check stock
        available = InventorySelector.get_total_available_quantity(str(medicine.id))

        # Check if medicine already in cart
        existing_item = session.items.filter(medicine=medicine).first()
        already_in_cart = existing_item.quantity if existing_item else 0
        total_requested = already_in_cart + quantity

        if available < total_requested:
            raise ValueError(
                f"Insufficient stock for '{medicine.name}'. "
                f"Available: {available}, Requested: {total_requested}."
            )

        # Get MRP from available batch (FEFO first batch)
        batches = InventorySelector.get_available_batches(str(medicine.id))
        unit_price = batches.first().mrp if batches.exists() else Decimal('0')
        gst_pct = batches.first().gst_percentage if batches.exists() else Decimal('0')

        if existing_item:
            # Update existing item quantity
            existing_item.quantity = total_requested
            existing_item.discount_percentage = discount_percentage
            existing_item.line_total = BillingSessionService._calc_line_total(
                unit_price, total_requested, discount_percentage, gst_pct
            )
            existing_item.save()
            item = existing_item
            logger.info(f"Cart item updated: medicine='{medicine.name}' | qty={total_requested}")
        else:
            # New item
            line_total = BillingSessionService._calc_line_total(
                unit_price, quantity, discount_percentage, gst_pct
            )
            item = BillingSessionItem.objects.create(
                session=session,
                medicine=medicine,
                quantity=quantity,
                unit_price=unit_price,
                discount_percentage=discount_percentage,
                gst_percentage=gst_pct,
                line_total=line_total,
            )
            logger.info(f"Cart item added: medicine='{medicine.name}' | qty={quantity}")

        BillingSessionService._recalculate_totals(session)
        return item

    # ─────────────────────────────────────────────
    # Update Item
    # ─────────────────────────────────────────────

    @staticmethod
    @transaction.atomic
    def update_item(session: BillingSession, item: BillingSessionItem,
                    quantity: int, discount_percentage: Decimal = None) -> BillingSessionItem:
        """
        Update quantity (and optional discount) of an existing cart item.

        Raises:
            ValueError: if stock insufficient or session inactive.
        """
        if not session.is_active:
            raise ValueError('Session is not active.')

        available = InventorySelector.get_total_available_quantity(
            str(item.medicine_id)
        )
        if available < quantity:
            raise ValueError(
                f"Insufficient stock for '{item.medicine.name}'. "
                f"Available: {available}, Requested: {quantity}."
            )

        item.quantity = quantity
        if discount_percentage is not None:
            item.discount_percentage = discount_percentage

        item.line_total = BillingSessionService._calc_line_total(
            item.unit_price, item.quantity,
            item.discount_percentage, item.gst_percentage
        )
        item.save()

        BillingSessionService._recalculate_totals(session)
        logger.info(f"Cart item updated: id={item.id} | qty={quantity}")
        return item

    # ─────────────────────────────────────────────
    # Remove Item
    # ─────────────────────────────────────────────

    @staticmethod
    @transaction.atomic
    def remove_item(session: BillingSession, item: BillingSessionItem) -> None:
        """Remove a medicine from the cart. No inventory change."""
        if not session.is_active:
            raise ValueError('Session is not active.')

        medicine_name = item.medicine.name
        item.delete()
        BillingSessionService._recalculate_totals(session)
        logger.info(f"Cart item removed: medicine='{medicine_name}' | session={session.id}")

    # ─────────────────────────────────────────────
    # Cancel Session
    # ─────────────────────────────────────────────

    @staticmethod
    @transaction.atomic
    def cancel_session(session: BillingSession) -> BillingSession:
        """Cancel the session. No inventory impact."""
        if not session.is_active:
            raise ValueError('Session is not active.')

        session.status = SessionStatus.CANCELLED
        session.save(update_fields=['status', 'updated_at'])
        logger.info(f"Billing session cancelled: id={session.id}")
        return session

    # ─────────────────────────────────────────────
    # Validate before checkout
    # ─────────────────────────────────────────────

    @staticmethod
    def validate_for_checkout(session: BillingSession) -> None:
        """
        Full re-validation before checkout.
        Called by SalesService — double-checks everything.

        Raises:
            ValueError: if any validation fails.
        """
        if not session.is_active:
            raise ValueError('Session is not active.')

        items = list(session.items.select_related('medicine').all())

        if not items:
            raise ValueError('Cannot checkout an empty cart.')

        for item in items:
            # Re-check medicine is still active
            if item.medicine.status != MedicineStatus.ACTIVE:
                raise ValueError(
                    f"Medicine '{item.medicine.name}' is no longer active."
                )

            # Re-check stock (another counter may have sold same medicine)
            available = InventorySelector.get_total_available_quantity(
                str(item.medicine_id)
            )
            if available < item.quantity:
                raise ValueError(
                    f"Insufficient stock for '{item.medicine.name}'. "
                    f"Available: {available}, In cart: {item.quantity}. "
                    f"Please update the quantity."
                )

    # ─────────────────────────────────────────────
    # Internal helpers
    # ─────────────────────────────────────────────

    @staticmethod
    def _calc_line_total(unit_price: Decimal, quantity: int,
                         discount_pct: Decimal, gst_pct: Decimal) -> Decimal:
        """Calculate line total: (price * qty) - discount + gst."""
        base = unit_price * quantity
        discount = base * (discount_pct / Decimal('100'))
        after_discount = base - discount
        gst = after_discount * (gst_pct / Decimal('100'))
        return (after_discount + gst).quantize(Decimal('0.01'))

    @staticmethod
    def _recalculate_totals(session: BillingSession) -> None:
        """Recalculate and save session totals after any item change."""
        # Always fetch fresh items from DB — never use cached session.items
        items = list(BillingSessionItem.objects.filter(session_id=session.id))

        subtotal = Decimal('0')
        discount_amount = Decimal('0')
        gst_amount = Decimal('0')

        for item in items:
            base = item.unit_price * item.quantity
            discount = base * (item.discount_percentage / Decimal('100'))
            after_discount = base - discount
            gst = after_discount * (item.gst_percentage / Decimal('100'))

            subtotal += base
            discount_amount += discount
            gst_amount += gst

        grand_total = subtotal - discount_amount + gst_amount

        session.subtotal = subtotal.quantize(Decimal('0.01'))
        session.discount_amount = discount_amount.quantize(Decimal('0.01'))
        session.gst_amount = gst_amount.quantize(Decimal('0.01'))
        session.grand_total = grand_total.quantize(Decimal('0.01'))
        session.save(update_fields=[
            'subtotal', 'discount_amount', 'gst_amount', 'grand_total', 'updated_at'
        ])
