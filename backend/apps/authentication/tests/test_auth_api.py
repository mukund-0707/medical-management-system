"""
Tests for Authentication API.
Tests every endpoint — success, failure, edge cases.
Run: pytest apps/authentication/tests/test_auth_api.py -v
"""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def active_user(db):
    """Create a normal active user."""
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com',
        first_name='Test',
        last_name='User',
    )


@pytest.fixture
def inactive_user(db):
    """Create an inactive user."""
    return User.objects.create_user(
        username='inactiveuser',
        password='testpass123',
        is_active=False,
    )


@pytest.fixture
def auth_tokens(api_client, active_user):
    """Login and return tokens."""
    response = api_client.post('/api/v1/auth/login/', {
        'username': 'testuser',
        'password': 'testpass123',
    }, format='json')
    return response.data['data']


# ─────────────────────────────────────────────
# Login Tests
# ─────────────────────────────────────────────

class TestLoginView:

    def test_login_success(self, api_client, active_user):
        """Valid credentials should return tokens."""
        response = api_client.post('/api/v1/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123',
        }, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert 'access' in response.data['data']
        assert 'refresh' in response.data['data']
        assert response.data['data']['user']['username'] == 'testuser'

    def test_login_wrong_password(self, api_client, active_user):
        """Wrong password should return 401."""
        response = api_client.post('/api/v1/auth/login/', {
            'username': 'testuser',
            'password': 'wrongpassword',
        }, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['success'] is False

    def test_login_wrong_username(self, api_client, db):
        """Non-existent username should return 401."""
        response = api_client.post('/api/v1/auth/login/', {
            'username': 'doesnotexist',
            'password': 'somepassword',
        }, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['success'] is False

    def test_login_inactive_user(self, api_client, inactive_user):
        """Inactive user should be rejected."""
        response = api_client.post('/api/v1/auth/login/', {
            'username': 'inactiveuser',
            'password': 'testpass123',
        }, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['success'] is False

    def test_login_missing_username(self, api_client, db):
        """Missing username should return 400."""
        response = api_client.post('/api/v1/auth/login/', {
            'password': 'testpass123',
        }, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['success'] is False

    def test_login_missing_password(self, api_client, db):
        """Missing password should return 400."""
        response = api_client.post('/api/v1/auth/login/', {
            'username': 'testuser',
        }, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['success'] is False

    def test_login_empty_username(self, api_client, db):
        """Empty username should return 400."""
        response = api_client.post('/api/v1/auth/login/', {
            'username': '',
            'password': 'testpass123',
        }, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ─────────────────────────────────────────────
# Logout Tests
# ─────────────────────────────────────────────

class TestLogoutView:

    def test_logout_success(self, api_client, active_user, auth_tokens):
        """Valid refresh token should be blacklisted."""
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_tokens['access']}")
        response = api_client.post('/api/v1/auth/logout/', {
            'refresh': auth_tokens['refresh'],
        }, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True

    def test_logout_without_token(self, api_client):
        """Unauthenticated request should return 401."""
        response = api_client.post('/api/v1/auth/logout/', {
            'refresh': 'sometoken',
        }, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_missing_refresh(self, api_client, active_user, auth_tokens):
        """Missing refresh token body should return 400."""
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_tokens['access']}")
        response = api_client.post('/api/v1/auth/logout/', {}, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ─────────────────────────────────────────────
# Token Refresh Tests
# ─────────────────────────────────────────────

class TestTokenRefreshView:

    def test_refresh_success(self, api_client, active_user, auth_tokens):
        """Valid refresh token should return new access token."""
        response = api_client.post('/api/v1/auth/refresh/', {
            'refresh': auth_tokens['refresh'],
        }, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert 'access' in response.data['data']

    def test_refresh_invalid_token(self, api_client, db):
        """Invalid refresh token should return 401."""
        response = api_client.post('/api/v1/auth/refresh/', {
            'refresh': 'this-is-not-a-valid-token',
        }, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['success'] is False

    def test_refresh_missing_token(self, api_client, db):
        """Missing refresh field should return 400."""
        response = api_client.post('/api/v1/auth/refresh/', {}, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ─────────────────────────────────────────────
# /me Endpoint Tests
# ─────────────────────────────────────────────

class TestMeView:

    def test_me_authenticated(self, api_client, active_user, auth_tokens):
        """Authenticated user should get their details."""
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_tokens['access']}")
        response = api_client.get('/api/v1/auth/me/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert response.data['data']['username'] == 'testuser'
        assert response.data['data']['email'] == 'test@example.com'

    def test_me_unauthenticated(self, api_client):
        """Unauthenticated request should return 401."""
        response = api_client.get('/api/v1/auth/me/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
