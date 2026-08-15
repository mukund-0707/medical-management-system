"""
Purchase Models — Purchase header + PurchaseItem.

Purchase is the ONLY way to introduce new stock into the system.
Draft purchases do NOT affect inventory.
Only FINALIZED purchases trigger inventory creation.
"""

import uuid
from django.db import models
from apps.supplier.models import Supplier
from apps.medicine.models import Medicine
from .constants import PurchaseStatus


class Purchase(models.Model):
    """
    Purchase invoice header.
    Contains supplier + invoice info.
    Medicine details are in PurchaseItem.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ── Supplier ──────────────────────────────────────────────
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='purchases',
        db_index=True,
    )

    # ── Invoice Info ──────────────────────────────────────────
    invoice_number = models.CharField(max_length=100, db_index=True)
    invoice_date = models.DateField()
    remarks = models.TextField(blank=True, default='')

    # ── Status ────────────────────────────────────────────────
    status = models.CharField(
        max_length=20,
        choices=PurchaseStatus.CHOICES,
        default=PurchaseStatus.DRAFT,
        db_index=True,
    )

    # ── Timestamps & Audit ────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='purchases_created',
    )
    finalized_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'purchase'
        ordering = ['-created_at']
        # Invoice number unique per supplier
        unique_together = [('supplier', 'invoice_number')]
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['status']),
            models.Index(fields=['invoice_date']),
        ]

    def __str__(self):
        return f"Purchase #{self.invoice_number} — {self.supplier.name}"

    @property
    def is_draft(self):
        return self.status == PurchaseStatus.DRAFT

    @property
    def is_finalized(self):
        return self.status == PurchaseStatus.FINALIZED

    @property
    def is_cancelled(self):
        return self.status == PurchaseStatus.CANCELLED


class PurchaseItem(models.Model):
    """
    Individual medicine line in a purchase invoice.
    Each PurchaseItem creates exactly one InventoryBatch on finalization.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ── Relations ─────────────────────────────────────────────
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name='items',
        db_index=True,
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT,
        related_name='purchase_items',
        db_index=True,
    )

    # ── Batch Info ────────────────────────────────────────────
    batch_number = models.CharField(max_length=100, db_index=True)
    expiry_date = models.DateField()

    # ── Pricing ───────────────────────────────────────────────
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)  # per unit
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # ── Quantity ──────────────────────────────────────────────
    quantity = models.PositiveIntegerField()

    # ── Timestamps ────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'purchase_item'
        ordering = ['created_at']
        # Same batch number cannot appear twice in same purchase
        unique_together = [('purchase', 'batch_number')]
        indexes = [
            models.Index(fields=['batch_number']),
            models.Index(fields=['expiry_date']),
        ]

    def __str__(self):
        return f"{self.medicine.name} | Batch: {self.batch_number} | Qty: {self.quantity}"

    @property
    def total_amount(self):
        """Line total after discount, before GST."""
        base = self.purchase_price * self.quantity
        discount = base * (self.discount_percentage / 100)
        return base - discount
