"""
Inventory Models — InventoryBatch + InventoryLedger.

InventoryBatch  : Current stock snapshot per batch.
InventoryLedger : Permanent, immutable history of every stock movement.

Two tables exist by design:
- Batch  → fast reads (dashboard, billing)
- Ledger → full audit trail (reports, history)
"""

import uuid
from django.db import models
from apps.medicine.models import Medicine
from .constants import BatchStatus, LedgerMovementType


class InventoryBatch(models.Model):
    """
    Represents one batch of a medicine in stock.
    Created when a Purchase is finalized.
    Quantity decreases with every sale.
    Never deleted — status changes to EXHAUSTED/EXPIRED/DAMAGED.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ── Medicine & Batch ──────────────────────────────────────
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT,
        related_name='inventory_batches',
        db_index=True,
    )
    batch_number = models.CharField(max_length=100, db_index=True)
    expiry_date = models.DateField(db_index=True)

    # ── Pricing (snapshot from purchase) ─────────────────────
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # ── Quantities ────────────────────────────────────────────
    quantity = models.PositiveIntegerField(default=0)        # current available
    damaged_quantity = models.PositiveIntegerField(default=0)
    expired_quantity = models.PositiveIntegerField(default=0)

    # ── Status ────────────────────────────────────────────────
    status = models.CharField(
        max_length=20,
        choices=BatchStatus.CHOICES,
        default=BatchStatus.AVAILABLE,
        db_index=True,
    )

    # ── Source Purchase ───────────────────────────────────────
    purchase_item = models.OneToOneField(
        'purchase.PurchaseItem',
        on_delete=models.PROTECT,
        related_name='inventory_batch',
        null=True,
        blank=True,
    )

    # ── Timestamps ────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventory_batch'
        ordering = ['expiry_date', 'created_at']   # FEFO default ordering
        indexes = [
            models.Index(fields=['medicine', 'status']),
            models.Index(fields=['batch_number']),
            models.Index(fields=['expiry_date']),
            models.Index(fields=['medicine', 'expiry_date']),
        ]

    def __str__(self):
        return f"{self.medicine.name} | Batch: {self.batch_number} | Qty: {self.quantity}"

    @property
    def is_available(self):
        return self.status == BatchStatus.AVAILABLE and self.quantity > 0

    @property
    def is_expired(self):
        from datetime import date
        return self.expiry_date <= date.today()


class InventoryLedger(models.Model):
    """
    Immutable stock movement history.
    One row = one stock event.
    Rows are NEVER updated or deleted.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ── Batch reference ───────────────────────────────────────
    inventory_batch = models.ForeignKey(
        InventoryBatch,
        on_delete=models.PROTECT,
        related_name='ledger_entries',
        db_index=True,
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT,
        related_name='ledger_entries',
        db_index=True,
    )

    # ── Movement ──────────────────────────────────────────────
    movement_type = models.CharField(
        max_length=30,
        choices=LedgerMovementType.CHOICES,
        db_index=True,
    )
    quantity = models.IntegerField()          # positive = stock in, negative = stock out
    quantity_before = models.PositiveIntegerField()
    quantity_after = models.PositiveIntegerField()

    # ── Reference ─────────────────────────────────────────────
    reference_id = models.CharField(max_length=100, blank=True, default='', db_index=True)
    reference_type = models.CharField(max_length=50, blank=True, default='')
    reason = models.TextField(blank=True, default='')

    # ── Audit ─────────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ledger_entries',
    )

    class Meta:
        db_table = 'inventory_ledger'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['medicine', 'created_at']),
            models.Index(fields=['movement_type']),
            models.Index(fields=['reference_id']),
        ]

    def __str__(self):
        sign = '+' if self.quantity > 0 else ''
        return (
            f"{self.medicine.name} | {self.movement_type} | "
            f"{sign}{self.quantity} | {self.created_at.date()}"
        )
