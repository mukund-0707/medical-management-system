"""
Supplier Service.
All business logic for Supplier module.
Views call this — never put logic in views.
"""

import logging
from django.db import transaction

from ..models import Supplier
from ..constants import SupplierStatus
from ..selectors.supplier_selector import SupplierSelector

logger = logging.getLogger('apps.supplier')


class SupplierService:

    @staticmethod
    @transaction.atomic
    def create_supplier(data: dict, created_by) -> Supplier:
        """
        Create a new supplier.

        Rules:
        - GST number must be unique (if provided).
        - Duplicate mobile triggers a warning (allowed but logged).

        Raises:
            ValueError: if GST number already exists.
        """
        gst_number = data.get('gst_number', '').strip().upper()
        mobile = data.get('mobile', '').strip()

        # GST uniqueness — hard reject
        if gst_number and SupplierSelector.gst_exists(gst_number):
            logger.warning(f"Duplicate GST number attempt: '{gst_number}'")
            raise ValueError(f"GST number '{gst_number}' already exists.")

        # Duplicate mobile — log warning, allow creation
        if SupplierSelector.mobile_exists(mobile):
            logger.warning(f"Duplicate mobile number detected: '{mobile}' — allowed.")

        supplier = Supplier(
            name=data['name'].strip(),
            mobile=mobile,
            email=data.get('email', '').strip().lower(),
            contact_person=data.get('contact_person', '').strip(),
            gst_number=gst_number,
            drug_license_number=data.get('drug_license_number', '').strip(),
            address=data['address'].strip(),
            city=data.get('city', '').strip(),
            state=data.get('state', '').strip(),
            pincode=data.get('pincode', '').strip(),
            remarks=data.get('remarks', '').strip(),
            status=SupplierStatus.ACTIVE,
            created_by=created_by,
        )
        supplier.save()

        logger.info(f"Supplier created: '{supplier.name}' | id={supplier.id} | by={created_by}")
        return supplier

    @staticmethod
    @transaction.atomic
    def update_supplier(supplier: Supplier, data: dict, updated_by) -> Supplier:
        """
        Update supplier details.

        Rules:
        - GST number must remain unique if changed.
        - Name and GST are locked after purchase history exists.

        Raises:
            ValueError: if business rules are violated.
        """
        has_history = SupplierSelector.has_purchase_history(str(supplier.id))

        # Lock identity fields after purchase history
        if has_history:
            locked_fields = ['name', 'gst_number']
            for field in locked_fields:
                if field in data:
                    current_val = str(getattr(supplier, field, '') or '')
                    new_val = str(data[field]).strip()
                    if current_val != new_val:
                        raise ValueError(
                            f"Cannot change '{field}' — supplier has purchase history."
                        )

        # GST uniqueness check if changing GST
        new_gst = data.get('gst_number', '').strip().upper()
        if new_gst and new_gst != supplier.gst_number:
            if SupplierSelector.gst_exists(new_gst, exclude_id=supplier.id):
                raise ValueError(f"GST number '{new_gst}' already exists.")

        # Apply updates
        allowed_fields = [
            'name', 'mobile', 'email', 'contact_person', 'gst_number',
            'drug_license_number', 'address', 'city', 'state',
            'pincode', 'remarks', 'status',
        ]
        for field in allowed_fields:
            if field in data:
                value = data[field]
                if isinstance(value, str):
                    value = value.strip()
                setattr(supplier, field, value)

        supplier.save()

        logger.info(f"Supplier updated: '{supplier.name}' | id={supplier.id} | by={updated_by}")
        return supplier

    @staticmethod
    @transaction.atomic
    def deactivate_supplier(supplier: Supplier, deactivated_by) -> Supplier:
        """
        Soft delete — sets status to INACTIVE.
        Supplier is never permanently deleted.
        Purchase history remains intact.
        """
        supplier.status = SupplierStatus.INACTIVE
        supplier.save(update_fields=['status', 'updated_at'])

        logger.info(
            f"Supplier deactivated: '{supplier.name}' | id={supplier.id} | by={deactivated_by}"
        )
        return supplier
