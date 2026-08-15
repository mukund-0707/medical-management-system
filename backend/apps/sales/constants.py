"""
Constants for Sales module.
"""


class SaleStatus:
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    CHOICES = [
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]


class PaymentMode:
    CASH = 'cash'
    UPI = 'upi'
    CARD = 'card'
    BANK_TRANSFER = 'bank_transfer'

    CHOICES = [
        (CASH, 'Cash'),
        (UPI, 'UPI'),
        (CARD, 'Card'),
        (BANK_TRANSFER, 'Bank Transfer'),
    ]
