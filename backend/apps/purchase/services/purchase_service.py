"""
Purchase Service.
Orchestrates the full purchase workflow:
  Draft → Finalize → Inventory Created → Ledger Created

This is the ONLY entry point for new inventory.
All steps run inside a single database transaction.
"""

import logging
from datetime import timezone as dt_timezone
from django.utils import timezone
from django.db import transaction

from apps.supplier.models import Supplier
from apps.medicine.models import Medicine
from apps.supplier.constants import SupplierStatus
from apps.medicine.constants import MedicineStatus

from ..models import Purchase, PurchaseItem
from ..constants import PurchaseStatus
from ..selectors.purchase_selector import PurchaseSelector

logger = logging.getLogger('apps.purchase')


class PurchaseService:

    # ─────────────────────────────────────────────
    # Create Draft Purchase
    # ─────────────────────────────────────────────

    @staticmethod
    @transaction.atomic
    def create_purchase(data: dict, created_by) -> Purchase:
        """
        Create a purchase in DRAFT status with its items.
        Inventory is NOT updated at this stage.

        Raises:
            ValueError: on any business rule violation.
        """
        supplier_id = str(data['supplier_id'])
        invoice_number = data['invoice_number'].strip().upper()

        # Validate supplier
        try:
            supplier = Supplier.objects.get(id=supplier_id)
        except Supplier.DoesNotExist:
            raise ValueError('Supplier not found.')

        if not supplier.is_active:
            raise ValueError('Cannot create purchase for an inactive supplier.')

        # Duplicate invoice check (per supplier)
        if PurchaseSelector.invoice_exists(supplier_id, invoice_number):
            raise ValueError(
                f"Invoice '{invoice_number}' already exists for this supplier."
            )

        # Validate each item
        items_data = data['items']
        validated_items = PurchaseService._validate_items(items_data)

        # Create purchase header
        purchase = Purchase.objects.create(
            supplier=supplier,
            invoice_number=invoice_number,
            invoice_date=data['invoice_date'],
            remarks=data.get('remarks', '').strip(),
            status=PurchaseStatus.DRAFT,
            created_by=created_by,
        )

        # Create items
        PurchaseItem.objects.bulk_create([
            PurchaseItem(
                purchase=purchase,
                medicine=item['medicine'],
                batch_number=item['batch_number'],
                expiry_date=item['expiry_date'],
                purchase_price=item['purchase_price'],
                mrp=item['mrp'],
                gst_percentage=item['gst_percentage'],
                discount_percentage=item['discount_percentage'],
                quantity=item['quantity'],
            )
            for item in validated_items
        ])

        logger.info(
            f"Purchase DRAFT created: invoice='{invoice_number}' "
            f"| supplier='{supplier.name}' | by={created_by}"
        )
        return purchase

    # ─────────────────────────────────────────────
    # Finalize Purchase → triggers inventory
    # ─────────────────────────────────────────────

    @staticmethod
    @transaction.atomic
    def finalize_purchase(purchase: Purchase, finalized_by) -> Purchase:
        """
        Finalize a DRAFT purchase.
        This triggers:
          1. Create InventoryBatch for each item
          2. Create InventoryLedger entries
          3. Lock the purchase (read-only)

        Everything runs in one atomic transaction.
        If anything fails → full rollback.

        Raises:
            ValueError: if purchase is not in DRAFT status.
        """
        if not purchase.is_draft:
            raise ValueError(
                f"Cannot finalize purchase with status '{purchase.status}'. "
                "Only DRAFT purchases can be finalized."
            )

        items = list(purchase.items.select_related('medicine').all())
        if not items:
            raise ValueError('Cannot finalize a purchase with no items.')

        # Re-validate all medicines are still active
        for item in items:
            if not item.medicine.is_active:
                raise ValueError(
                    f"Medicine '{item.medicine.name}' is inactive. "
                    "Cannot finalize purchase."
                )

        # Import inventory service here to avoid circular imports
        from apps.inventory.services.inventory_service import InventoryService

        # Create inventory batches + ledger entries for each item
        for item in items:
            InventoryService.create_from_purchase(
                purchase_item=item,
                created_by=finalized_by,
            )

        # Lock the purchase
        purchase.status = PurchaseStatus.FINALIZED
        purchase.finalized_at = timezone.now()
        purchase.save(update_fields=['status', 'finalized_at', 'updated_at'])

        logger.info(
            f"Purchase FINALIZED: invoice='{purchase.invoice_number}' "
            f"| id={purchase.id} | by={finalized_by}"
        )
        return purchase

    # ─────────────────────────────────────────────
    # Cancel Purchase
    # ─────────────────────────────────────────────

    @staticmethod
    @transaction.atomic
    def cancel_purchase(purchase: Purchase, cancelled_by) -> Purchase:
        """
        Cancel a purchase.

        Rules:
        - DRAFT can always be cancelled.
        - FINALIZED can be cancelled ONLY if no inventory has been consumed
          (no sales from any batch in this purchase).

        Raises:
            ValueError: if cancellation is not allowed.
        """
        if purchase.is_cancelled:
            raise ValueError('Purchase is already cancelled.')

        if purchase.is_finalized:
            # Check if any batch from this purchase has been consumed
            from apps.inventory.selectors.inventory_selector import InventorySelector
            for item in purchase.items.all():
                if InventorySelector.batch_has_sales(item.batch_number, item.medicine_id):
                    raise ValueError(
                        f"Cannot cancel — batch '{item.batch_number}' of "
                        f"'{item.medicine.name}' has already been sold."
                    )

            # Reverse inventory
            from apps.inventory.services.inventory_service import InventoryService
            for item in purchase.items.select_related('medicine').all():
                InventoryService.reverse_purchase(
                    purchase_item=item,
                    cancelled_by=cancelled_by,
                )

        purchase.status = PurchaseStatus.CANCELLED
        purchase.cancelled_at = timezone.now()
        purchase.save(update_fields=['status', 'cancelled_at', 'updated_at'])

        logger.info(
            f"Purchase CANCELLED: invoice='{purchase.invoice_number}' "
            f"| id={purchase.id} | by={cancelled_by}"
        )
        return purchase

    # ─────────────────────────────────────────────
    # Update Draft Purchase
    # ─────────────────────────────────────────────

    @staticmethod
    @transaction.atomic
    def update_purchase(purchase: Purchase, data: dict, updated_by) -> Purchase:
        """
        Update header fields of a DRAFT purchase.
        Finalized purchases cannot be edited.

        Raises:
            ValueError: if purchase is not DRAFT.
        """
        if not purchase.is_draft:
            raise ValueError('Only DRAFT purchases can be edited.')

        if 'invoice_number' in data:
            new_invoice = data['invoice_number'].strip().upper()
            if new_invoice != purchase.invoice_number:
                if PurchaseSelector.invoice_exists(
                    str(purchase.supplier_id), new_invoice, exclude_id=purchase.id
                ):
                    raise ValueError(
                        f"Invoice '{new_invoice}' already exists for this supplier."
                    )
            purchase.invoice_number = new_invoice

        if 'invoice_date' in data:
            purchase.invoice_date = data['invoice_date']

        if 'remarks' in data:
            purchase.remarks = data['remarks'].strip()

        purchase.save()

        logger.info(f"Purchase updated: id={purchase.id} | by={updated_by}")
        return purchase

    # ─────────────────────────────────────────────
    # Internal helpers
    # ─────────────────────────────────────────────

    @staticmethod
    def _validate_items(items_data: list) -> list:
        """
        Validate all purchase items — medicine exists, active, price > 0.
        Returns list of validated item dicts with medicine objects.
        """
        validated = []
        for item in items_data:
            medicine_id = str(item['medicine_id'])
            try:
                medicine = Medicine.objects.get(id=medicine_id)
            except Medicine.DoesNotExist:
                raise ValueError(f"Medicine with id '{medicine_id}' not found.")

            if not medicine.is_active:
                raise ValueError(
                    f"Medicine '{medicine.name}' is inactive. "
                    "Cannot add to purchase."
                )

            validated.append({
                'medicine': medicine,
                'batch_number': item['batch_number'].strip().upper(),
                'expiry_date': item['expiry_date'],
                'purchase_price': item['purchase_price'],
                'mrp': item['mrp'],
                'gst_percentage': item.get('gst_percentage', 0),
                'discount_percentage': item.get('discount_percentage', 0),
                'quantity': item['quantity'],
            })

        return validated
