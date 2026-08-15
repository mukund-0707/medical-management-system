"""
Basic role-based permissions for POC.
Admin: Full access. Cashier: Billing & Sales only.
"""

from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Allow access only to admin users."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsCashier(BasePermission):
    """Allow access only to cashier users."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'cashier'
        )


class IsAdminOrCashier(BasePermission):
    """Allow access to both admin and cashier users."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('admin', 'cashier')
        )
