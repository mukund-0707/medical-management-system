"""
Billing Session Selectors — read-only queries.
"""

from ..models import BillingSession, BillingSessionItem
from ..constants import SessionStatus


class BillingSessionSelector:

    @staticmethod
    def get_by_id(session_id: str) -> BillingSession | None:
        try:
            return BillingSession.objects.prefetch_related(
                'items__medicine'
            ).get(id=session_id)
        except BillingSession.DoesNotExist:
            return None

    @staticmethod
    def get_item_by_id(item_id: str) -> BillingSessionItem | None:
        try:
            return BillingSessionItem.objects.select_related(
                'medicine', 'session'
            ).get(id=item_id)
        except BillingSessionItem.DoesNotExist:
            return None

    @staticmethod
    def get_active_sessions_for_user(user_id):
        return BillingSession.objects.filter(
            created_by_id=user_id,
            status=SessionStatus.ACTIVE,
        ).prefetch_related('items__medicine')
