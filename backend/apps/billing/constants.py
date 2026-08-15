"""
Constants for Billing Session module.
"""


class SessionStatus:
    ACTIVE = 'active'
    CHECKED_OUT = 'checked_out'
    CANCELLED = 'cancelled'
    EXPIRED = 'expired'

    CHOICES = [
        (ACTIVE, 'Active'),
        (CHECKED_OUT, 'Checked Out'),
        (CANCELLED, 'Cancelled'),
        (EXPIRED, 'Expired'),
    ]


# Session expires after this many minutes of inactivity
SESSION_EXPIRY_MINUTES = 30
