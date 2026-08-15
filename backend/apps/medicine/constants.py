"""
Constants for Medicine module.
Never hardcode these values elsewhere.
"""


class MedicineStatus:
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DISCONTINUED = 'discontinued'

    CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (DISCONTINUED, 'Discontinued'),
    ]


class DosageForm:
    TABLET = 'tablet'
    CAPSULE = 'capsule'
    SYRUP = 'syrup'
    INJECTION = 'injection'
    DROPS = 'drops'
    CREAM = 'cream'
    OINTMENT = 'ointment'
    GEL = 'gel'
    POWDER = 'powder'
    INHALER = 'inhaler'
    PATCH = 'patch'
    OTHER = 'other'

    CHOICES = [
        (TABLET, 'Tablet'),
        (CAPSULE, 'Capsule'),
        (SYRUP, 'Syrup'),
        (INJECTION, 'Injection'),
        (DROPS, 'Drops'),
        (CREAM, 'Cream'),
        (OINTMENT, 'Ointment'),
        (GEL, 'Gel'),
        (POWDER, 'Powder'),
        (INHALER, 'Inhaler'),
        (PATCH, 'Patch'),
        (OTHER, 'Other'),
    ]
