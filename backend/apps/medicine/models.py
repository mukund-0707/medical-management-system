"""
Medicine Model.
Stores medicine master/identity information ONLY.
Stock, batch, expiry — all belong to Inventory module.
"""

import uuid
from django.db import models
from .constants import MedicineStatus, DosageForm


class Medicine(models.Model):
    """
    Master catalog of medicines.
    Medicine never stores stock quantity.
    Stock is managed by the Inventory module.
    """

    # ── Identity ──────────────────────────────────────────────
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    barcode = models.CharField(max_length=100, unique=True, db_index=True)
    generic_name = models.CharField(max_length=255, blank=True, default='')
    manufacturer = models.CharField(max_length=255)
    strength = models.CharField(max_length=100)  # e.g. "500mg", "10mg/5ml"
    dosage_form = models.CharField(
        max_length=50,
        choices=DosageForm.CHOICES,
        default=DosageForm.TABLET,
    )

    # ── Optional Info ─────────────────────────────────────────
    category = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    storage_instruction = models.CharField(max_length=255, blank=True, default='')
    hsn_code = models.CharField(max_length=20, blank=True, default='')
    gst_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00
    )

    # ── Status ────────────────────────────────────────────────
    status = models.CharField(
        max_length=20,
        choices=MedicineStatus.CHOICES,
        default=MedicineStatus.ACTIVE,
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
        related_name='medicines_created',
    )

    class Meta:
        db_table = 'medicine'
        ordering = ['name']
        indexes = [
            models.Index(fields=['barcode']),
            models.Index(fields=['name']),
            models.Index(fields=['generic_name']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.name} {self.strength} ({self.manufacturer})"

    @property
    def is_active(self):
        return self.status == MedicineStatus.ACTIVE
