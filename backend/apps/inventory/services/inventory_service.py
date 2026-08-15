"""
Inventory Service — the heart of the system.

ONLY this service may modify stock.
No other module touches inventory directly.

Responsibilities:
- create_from_purchase()  : Purchase finalization → create batch + ledger
- reduce_for_sale()       : Sale checkout → FEFO deduction + ledger
- reverse_purchase()      : Purchase cancellation → reverse batch + ledger
- adjust_stock()          : Manual adjustment + ledger
- mark_expired()          : Move expired stock
"""

import logging
from django.db import transaction

from ..models import InventoryBatch, InventoryLedger
from ..constants import BatchStatus, LedgerMovementType, AdjustmentReason

logger = logging.getLogger('apps.inventory')


class InventoryService:

    # ─────────────────────────────────────────────
    # Called by Purchase.finalize()
    # ─────────────────────────────────────────────

    @staticmethod
    @transaction.atomic
    def create_from_purchase(purchase_item, created_by) -> InventoryBatch:
        """
        Create an InventoryBatch from a finalized PurchaseItem.
        Creates corresponding ledger entry.

        Called by PurchaseService.finalize_purchase() for each item.
        """
        batch = InventoryBatch.objects.create(
            medicine=purchase_item.medicine,
            batch_number=purchase_item.batch_number,
            expiry_date=purchase_item.expiry_date,
            purchase_price=purchase_item.purchase_price,
            mrp=purchase_item.mrp,
            gst_percentage=purchase_item.gst_percentage,
            quantity=purchase_item.quantity,
            status=BatchStatus.AVAILABLE,
            purchase_item=purchase_item,
        )

        # Ledger entry
        InventoryLedger.objects.create(
            inventory_batch=batch,
            medicine=purchase_item.medicine,
            movement_type=LedgerMovementType.PURCHASE,
            quantity=purchase_item.quantity,
            quantity_before=0,
            quantity_after=purchase_item.quantity,
            reference_id=str(purchase_item.purchase.id),
            reference_type='purchase',
            reason=f"Purchase invoice: {purchase_item.purchase.invoice_number}",
            created_by=created_by,
        )

        logger.info(
            f"Inventory created: medicine='{purchase_item.medicine.name}' "
            f"| batch='{batch.batch_number}' | qty={batch.quantity}"
        )
        return batch

    # ─────────────────────────────────────────────
    # Called by Sales.checkout() — FEFO
    # ─────────────────────────────────────────────

    @staticmethod
    @transaction.atomic
    def reduce_for_sale(medicine_id: str, quantity: int, sale_id: str, created_by) -> list:
        """
        Reduce inventory for a sale using FEFO (First Expiry First Out).
        May consume multiple batches if one batch doesn't have enough.

        Returns:
            list of dicts: [{batch, quantity_deducted}, ...]

        Raises:
            ValueError: if total available < requested quantity.
        """
        from ..selectors.inventory_selector import InventorySelector

        available_batches = list(
            InventorySelector.get_available_batches(medicine_id)
        )

        total_available = sum(b.quantity for b in available_batches)

        if total_available < quantity:
            raise ValueError(
                f"Insufficient stock. Available: {total_available}, Requested: {quantity}."
            )

        remaining = quantity
        deductions = []

        for batch in available_batches:
            if remaining <= 0:
                break

            # Skip expired batches
            if batch.is_expired:
                continue

            deduct = min(batch.quantity, remaining)
            qty_before = batch.quantity

            batch.quantity -= deduct
            if batch.quantity == 0:
                batch.status = BatchStatus.EXHAUSTED
            batch.save(update_fields=['quantity', 'status', 'updated_at'])

            InventoryLedger.objects.create(
                inventory_batch=batch,
                medicine_id=medicine_id,
                movement_type=LedgerMovementType.SALE,
                quantity=-deduct,
                quantity_before=qty_before,
                quantity_after=batch.quantity,
                reference_id=sale_id,
                reference_type='sale',
                reason=f"Sale ID: {sale_id}",
                created_by=created_by,
            )

            deductions.append({'batch': batch, 'quantity_deducted': deduct})
            remaining -= deduct

            logger.info(
                f"Stock reduced: medicine_id={medicine_id} | "
                f"batch='{batch.batch_number}' | deducted={deduct} | remaining_qty={batch.quantity}"
            )

        return deductions

    # ─────────────────────────────────────────────
    # Called by Purchase.cancel() for finalized purchases
    # ─────────────────────────────────────────────

    @staticmethod
    @transaction.atomic
    def reverse_purchase(purchase_item, cancelled_by) -> None:
        """
        Reverse inventory for a cancelled finalized purchase.
        Sets batch quantity to 0 and status to EXHAUSTED.
        Creates a ledger entry for the reversal.
        """
        try:
            batch = purchase_item.inventory_batch
        except InventoryBatch.DoesNotExist:
            logger.warning(
                f"No inventory batch found for purchase_item={purchase_item.id} — skipping."
            )
            return

        qty_before = batch.quantity

        InventoryLedger.objects.create(
            inventory_batch=batch,
            medicine=purchase_item.medicine,
            movement_type=LedgerMovementType.PURCHASE_RETURN,
            quantity=-qty_before,
            quantity_before=qty_before,
            quantity_after=0,
            reference_id=str(purchase_item.purchase.id),
            reference_type='purchase_cancellation',
            reason=f"Purchase cancelled: {purchase_item.purchase.invoice_number}",
            created_by=cancelled_by,
        )

        batch.quantity = 0
        batch.status = BatchStatus.EXHAUSTED
        batch.save(update_fields=['quantity', 'status', 'updated_at'])

        logger.info(
            f"Inventory reversed: batch='{batch.batch_number}' "
            f"| medicine='{purchase_item.medicine.name}' | qty reversed={qty_before}"
        )

    # ─────────────────────────────────────────────
    # Manual Adjustment
    # ─────────────────────────────────────────────

    @staticmethod
    @transaction.atomic
    def adjust_stock(batch: InventoryBatch, new_quantity: int, reason: str,
                     adjustment_reason_code: str, adjusted_by) -> InventoryBatch:
        """
        Manual inventory adjustment.
        Always creates a ledger entry — never silent.

        Args:
            batch            : The InventoryBatch to adjust.
            new_quantity     : The correct quantity (what it should be).
            reason           : Free-text explanation.
            adjustment_reason_code : One of AdjustmentReason constants.
            adjusted_by      : User performing adjustment.

        Raises:
            ValueError: if new_quantity < 0 or reason is empty.
        """
        if new_quantity < 0:
            raise ValueError('New quantity cannot be negative.')

        if not reason or not reason.strip():
            raise ValueError('Adjustment reason is required.')

        qty_before = batch.quantity
        difference = new_quantity - qty_before

        batch.quantity = new_quantity

        # Update status based on new quantity
        if new_quantity == 0:
            batch.status = BatchStatus.EXHAUSTED
        elif batch.status == BatchStatus.EXHAUSTED and new_quantity > 0:
            batch.status = BatchStatus.AVAILABLE

        batch.save(update_fields=['quantity', 'status', 'updated_at'])

        InventoryLedger.objects.create(
            inventory_batch=batch,
            medicine=batch.medicine,
            movement_type=LedgerMovementType.ADJUSTMENT,
            quantity=difference,
            quantity_before=qty_before,
            quantity_after=new_quantity,
            reference_id=str(batch.id),
            reference_type='adjustment',
            reason=f"[{adjustment_reason_code}] {reason.strip()}",
            created_by=adjusted_by,
        )

        logger.info(
            f"Inventory adjusted: medicine='{batch.medicine.name}' "
            f"| batch='{batch.batch_number}' | {qty_before} → {new_quantity} "
            f"| reason='{adjustment_reason_code}' | by={adjusted_by}"
        )

        return batch

    # ─────────────────────────────────────────────
    # Mark expired batches
    # ─────────────────────────────────────────────

    @staticmethod
    @transaction.atomic
    def mark_expired(batch: InventoryBatch, marked_by) -> InventoryBatch:
        """
        Move available quantity to expired_quantity.
        Expired medicines cannot be sold.
        """
        if batch.quantity <= 0:
            raise ValueError('Batch has no available quantity to mark as expired.')

        qty_before = batch.quantity

        batch.expired_quantity += batch.quantity
        batch.quantity = 0
        batch.status = BatchStatus.EXPIRED
        batch.save(update_fields=['quantity', 'expired_quantity', 'status', 'updated_at'])

        InventoryLedger.objects.create(
            inventory_batch=batch,
            medicine=batch.medicine,
            movement_type=LedgerMovementType.EXPIRY,
            quantity=-qty_before,
            quantity_before=qty_before,
            quantity_after=0,
            reference_id=str(batch.id),
            reference_type='expiry',
            reason=f"Batch expired: {batch.expiry_date}",
            created_by=marked_by,
        )

        logger.info(
            f"Batch marked expired: '{batch.batch_number}' "
            f"| medicine='{batch.medicine.name}' | qty moved={qty_before}"
        )

        return batch
