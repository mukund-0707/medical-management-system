"""
Billing Session Models.

BillingSession     : Temporary cart — created when billing starts.
BillingSessionItem : Each medicine line in the cart.

Sessions do NOT affect inventory.
Only checkout triggers the Sales module which updates inventory.
"""

import uuid
from django.db import models
from apps.medicine.models import Medicine
from .constants import SessionStatus


class BillingSession(models.Model):
    """
    Temporary billing cart.
    Lives until checkout, cancel, or expiry.
    Never permanently stored after completion.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    status = models.CharField(
        max_length=20,
        choices=SessionStatus.CHOICES,
        default=SessionStatus.ACTIVE,
        db_index=True,
    )

    # ── Totals (recalculated on every item change) ────────────
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # ── Audit ─────────────────────────────────────────────────
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='billing_sessions',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'billing_session'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_by', 'status']),
        ]

    def __str__(self):
        return f"Session {self.id} | {self.status} | Total: {self.grand_total}"

    @property
    def is_active(self):
        return self.status == SessionStatus.ACTIVE

    @property
    def item_count(self):
        return self.items.count()


class BillingSessionItem(models.Model):
    """
    One medicine line inside a billing session.
    Quantity validated against real-time inventory on add and checkout.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    session = models.ForeignKey(
        BillingSession,
        on_delete=models.CASCADE,
        related_name='items',
        db_index=True,
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT,
        related_name='billing_items',
        db_index=True,
    )

    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # MRP at time of add
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'billing_session_item'
        ordering = ['created_at']
        # Same medicine cannot appear twice in same session
        unique_together = [('session', 'medicine')]

    def __str__(self):
        return f"{self.medicine.name} x{self.quantity} = {self.line_total}"
