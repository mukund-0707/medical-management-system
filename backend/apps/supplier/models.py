"""
Supplier Model.
Stores supplier/vendor master information.
Supplier does NOT own inventory or medicines.
Every Purchase must be linked to an active Supplier.
"""

import uuid
from django.db import models
from .constants import SupplierStatus


class Supplier(models.Model):
    """
    Master table for medicine suppliers/vendors.
    Soft delete only — purchase history must remain intact.
    """

    # ── Identity ──────────────────────────────────────────────
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    mobile = models.CharField(max_length=15)

    # ── Optional Info ─────────────────────────────────────────
    email = models.EmailField(blank=True, default='')
    contact_person = models.CharField(max_length=255, blank=True, default='')
    gst_number = models.CharField(max_length=20, blank=True, default='', db_index=True)
    drug_license_number = models.CharField(max_length=50, blank=True, default='')

    # ── Address ───────────────────────────────────────────────
    address = models.TextField()
    city = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True, default='')
    pincode = models.CharField(max_length=10, blank=True, default='')

    # ── Remarks ───────────────────────────────────────────────
    remarks = models.TextField(blank=True, default='')

    # ── Status ────────────────────────────────────────────────
    status = models.CharField(
        max_length=20,
        choices=SupplierStatus.CHOICES,
        default=SupplierStatus.ACTIVE,
        db_index=True,
    )

    # ── Timestamps ────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='suppliers_created',
    )

    class Meta:
        db_table = 'supplier'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['mobile']),
            models.Index(fields=['gst_number']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.name} ({self.mobile})"

    @property
    def is_active(self):
        return self.status == SupplierStatus.ACTIVE
