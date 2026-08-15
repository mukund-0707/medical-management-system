"""
Constants for Supplier module.
"""


class SupplierStatus:
    ACTIVE = 'active'
    INACTIVE = 'inactive'

    CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]
