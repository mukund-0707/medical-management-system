"""
Serializers for Authentication module.
Responsible only for input/output validation.
No business logic here.
"""

from django.contrib.auth.models import User
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """Validates login request — username + password."""
    username = serializers.CharField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
    )
    password = serializers.CharField(
        required=True,
        allow_blank=False,
        write_only=True,
    )


class TokenRefreshInputSerializer(serializers.Serializer):
    """Validates token refresh request."""
    refresh = serializers.CharField(
        required=True,
        allow_blank=False,
    )


class UserSerializer(serializers.ModelSerializer):
    """Read-only serializer for current user info (/me endpoint)."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
        read_only_fields = fields
