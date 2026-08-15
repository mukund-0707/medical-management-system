"""
Sales Models — Sale header + SaleItem.

Sale     : One completed billing transaction.
SaleItem : Each medicine line in the sale.

Sale records are permanent.
Completed sales cannot be edited.
"""

import uuid
from django.db import models
from apps.medicine.models import Medicine
from apps.inventory.models import InventoryBatch
from .constants import SaleStatus, PaymentMode


class Sale(models.Model):
    """
    A completed sale transaction.
    Created only after successful checkout.
    Immutable after creation.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ── Invoice ───────────────────────────────────────────────
    invoice_number = models.CharField(
        max_length=50, unique=True, db_index=True
    )
    sale_date = models.DateField(db_index=True)

    # ── Payment ───────────────────────────────────────────────
    payment_mode = models.CharField(
        max_length=20,
        choices=PaymentMode.CHOICES,
        default=PaymentMode.CASH,
    )

    # ── Totals ────────────────────────────────────────────────
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2)

    # ── Status ────────────────────────────────────────────────
    status = models.CharField(
        max_length=20,
        choices=SaleStatus.CHOICES,
        default=SaleStatus.COMPLETED,
        db_index=True,
    )

    remarks = models.TextField(blank=True, default='')

    # ── Billing Session reference (kept for traceability) ─────
    billing_session_id = models.UUIDField(null=True, blank=True)

    # ── Audit ─────────────────────────────────────────────────
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sales_created',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'sale'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['sale_date']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_mode']),
        ]

    def __str__(self):
        return f"Sale {self.invoice_number} | {self.grand_total} | {self.sale_date}"

    @property
    def is_completed(self):
        return self.status == SaleStatus.COMPLETED

    @property
    def is_cancelled(self):
        return self.status == SaleStatus.CANCELLED


class SaleItem(models.Model):
    """
    One medicine line in a completed sale.
    Always references the InventoryBatch that was consumed.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='items',
        db_index=True,
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT,
        related_name='sale_items',
        db_index=True,
    )
    inventory_batch = models.ForeignKey(
        InventoryBatch,
        on_delete=models.PROTECT,
        related_name='sale_items',
        null=True,
        blank=True,
    )

    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sale_item'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.medicine.name} x{self.quantity} = {self.line_total}"
