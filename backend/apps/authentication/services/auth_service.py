"""
Authentication Service.
All business logic for login, logout, token refresh.
Views call this service — never implement logic in views.
"""

import logging

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

logger = logging.getLogger('apps.authentication')


class AuthService:
    """
    Handles all authentication business operations.
    - login
    - logout (token blacklist)
    - token refresh
    """

    @staticmethod
    def login(username: str, password: str) -> dict:
        """
        Authenticate user and return JWT tokens.

        Returns:
            dict with access + refresh tokens and user info.

        Raises:
            ValueError: if credentials are invalid or user is inactive.
        """
        user = authenticate(username=username, password=password)

        if user is None:
            logger.warning(f"Failed login attempt for username='{username}'")
            raise ValueError('Invalid username or password.')

        if not user.is_active:
            logger.warning(f"Login attempt by inactive user='{username}'")
            raise ValueError('Your account is inactive. Please contact administrator.')

        refresh = RefreshToken.for_user(user)

        logger.info(f"User '{username}' logged in successfully.")

        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
            },
        }

    @staticmethod
    def logout(refresh_token: str) -> None:
        """
        Blacklist the refresh token to invalidate the session.

        Raises:
            ValueError: if the token is invalid or already blacklisted.
        """
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info("Refresh token blacklisted successfully.")
        except (TokenError, InvalidToken) as exc:
            logger.warning(f"Logout failed — invalid token: {exc}")
            raise ValueError('Invalid or expired refresh token.')

    @staticmethod
    def refresh_token(refresh_token_str: str) -> dict:
        """
        Generate a new access token from a valid refresh token.
        SimpleJWT handles ROTATE_REFRESH_TOKENS automatically via its own view,
        but here we do a clean manual refresh for our custom response format.

        Returns:
            dict with new access + new refresh tokens.

        Raises:
            ValueError: if the refresh token is invalid or expired.
        """
        try:
            old_token = RefreshToken(refresh_token_str)

            # Get user from token claim
            user_id = old_token['user_id']
            user = User.objects.get(id=user_id)

            # Blacklist old token
            old_token.blacklist()

            # Issue a fresh token pair
            new_refresh = RefreshToken.for_user(user)

            logger.info(f"Token refreshed for user_id='{user_id}'.")

            return {
                'access': str(new_refresh.access_token),
                'refresh': str(new_refresh),
            }

        except User.DoesNotExist:
            logger.warning("Token refresh failed — user not found.")
            raise ValueError('Invalid token: user does not exist.')
        except (TokenError, InvalidToken) as exc:
            logger.warning(f"Token refresh failed: {exc}")
            raise ValueError('Invalid or expired refresh token.')
