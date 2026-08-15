"""
Medicine Service.
All business logic for Medicine module lives here.
Views call this service — never put logic in views.
"""

import logging
from django.db import transaction

from ..models import Medicine
from ..constants import MedicineStatus
from ..selectors.medicine_selector import MedicineSelector

logger = logging.getLogger('apps.medicine')


class MedicineService:

    @staticmethod
    @transaction.atomic
    def create_medicine(data: dict, created_by) -> Medicine:
        """
        Create a new medicine.

        Rules:
        - Barcode must be unique.
        - Adding medicine does NOT create inventory (stock stays 0).

        Raises:
            ValueError: if barcode already exists.
        """
        barcode = data.get('barcode', '').strip()

        if MedicineSelector.barcode_exists(barcode):
            logger.warning(f"Duplicate barcode attempt: '{barcode}'")
            raise ValueError(f"Barcode '{barcode}' already exists.")

        medicine = Medicine(
            name=data['name'].strip(),
            barcode=barcode,
            generic_name=data.get('generic_name', '').strip(),
            manufacturer=data['manufacturer'].strip(),
            strength=data['strength'].strip(),
            dosage_form=data.get('dosage_form', 'tablet'),
            category=data.get('category', '').strip(),
            description=data.get('description', '').strip(),
            storage_instruction=data.get('storage_instruction', '').strip(),
            hsn_code=data.get('hsn_code', '').strip(),
            gst_percentage=data.get('gst_percentage', 0),
            status=MedicineStatus.ACTIVE,
            created_by=created_by,
        )
        medicine.save()

        logger.info(f"Medicine created: '{medicine.name}' | barcode='{barcode}' | by={created_by}")
        return medicine

    @staticmethod
    @transaction.atomic
    def update_medicine(medicine: Medicine, data: dict, updated_by) -> Medicine:
        """
        Update medicine details.

        Rules:
        - Identity fields (name, barcode, strength, manufacturer) are
          locked once transaction history exists.
        - Status can always be changed.

        Raises:
            ValueError: if trying to change locked identity fields.
        """
        has_history = MedicineSelector.has_transaction_history(str(medicine.id))

        identity_fields = ['name', 'barcode', 'strength', 'manufacturer']

        if has_history:
            for field in identity_fields:
                if field in data:
                    current_val = getattr(medicine, field)
                    new_val = str(data[field]).strip()
                    if current_val != new_val:
                        raise ValueError(
                            f"Cannot change '{field}' — medicine has transaction history."
                        )

        # Check barcode uniqueness if barcode is being changed
        new_barcode = data.get('barcode', '').strip()
        if new_barcode and new_barcode != medicine.barcode:
            if MedicineSelector.barcode_exists(new_barcode, exclude_id=medicine.id):
                raise ValueError(f"Barcode '{new_barcode}' already exists.")

        # Apply updates
        allowed_fields = [
            'name', 'barcode', 'generic_name', 'manufacturer', 'strength',
            'dosage_form', 'category', 'description', 'storage_instruction',
            'hsn_code', 'gst_percentage', 'status',
        ]
        for field in allowed_fields:
            if field in data:
                value = data[field]
                if isinstance(value, str):
                    value = value.strip()
                setattr(medicine, field, value)

        medicine.save()

        logger.info(f"Medicine updated: '{medicine.name}' | id={medicine.id} | by={updated_by}")
        return medicine

    @staticmethod
    @transaction.atomic
    def deactivate_medicine(medicine: Medicine, deactivated_by) -> Medicine:
        """
        Soft delete — sets status to INACTIVE.
        Medicine is never permanently deleted.
        """
        medicine.status = MedicineStatus.INACTIVE
        medicine.save(update_fields=['status', 'updated_at'])

        logger.info(
            f"Medicine deactivated: '{medicine.name}' | id={medicine.id} | by={deactivated_by}"
        )
        return medicine
