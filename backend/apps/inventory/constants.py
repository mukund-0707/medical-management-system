"""
Constants for Inventory module.
"""


class BatchStatus:
    AVAILABLE = 'available'
    EXPIRED = 'expired'
    DAMAGED = 'damaged'
    EXHAUSTED = 'exhausted'    # quantity = 0

    CHOICES = [
        (AVAILABLE, 'Available'),
        (EXPIRED, 'Expired'),
        (DAMAGED, 'Damaged'),
        (EXHAUSTED, 'Exhausted'),
    ]


class LedgerMovementType:
    PURCHASE = 'purchase'
    SALE = 'sale'
    ADJUSTMENT = 'adjustment'
    DAMAGE = 'damage'
    EXPIRY = 'expiry'
    PURCHASE_RETURN = 'purchase_return'
    CUSTOMER_RETURN = 'customer_return'

    CHOICES = [
        (PURCHASE, 'Purchase'),
        (SALE, 'Sale'),
        (ADJUSTMENT, 'Adjustment'),
        (DAMAGE, 'Damage'),
        (EXPIRY, 'Expiry'),
        (PURCHASE_RETURN, 'Purchase Return'),
        (CUSTOMER_RETURN, 'Customer Return'),
    ]


class AdjustmentReason:
    WRONG_ENTRY = 'wrong_entry'
    DAMAGE = 'damage'
    PHYSICAL_COUNT = 'physical_count'
    SUPPLIER_CORRECTION = 'supplier_correction'
    EXPIRED = 'expired'
    OTHER = 'other'

    CHOICES = [
        (WRONG_ENTRY, 'Wrong Entry'),
        (DAMAGE, 'Damage'),
        (PHYSICAL_COUNT, 'Physical Count Difference'),
        (SUPPLIER_CORRECTION, 'Supplier Correction'),
        (EXPIRED, 'Expired Medicine'),
        (OTHER, 'Other'),
    ]


# Medicines with quantity <= this are considered "low stock"
LOW_STOCK_THRESHOLD = 10
