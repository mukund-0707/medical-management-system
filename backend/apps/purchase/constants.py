"""
Constants for Purchase module.
"""


class PurchaseStatus:
    DRAFT = 'draft'
    FINALIZED = 'finalized'
    CANCELLED = 'cancelled'

    CHOICES = [
        (DRAFT, 'Draft'),
        (FINALIZED, 'Finalized'),
        (CANCELLED, 'Cancelled'),
    ]
