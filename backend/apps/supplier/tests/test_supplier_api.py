"""
Tests for Supplier API.
Run: pytest apps/supplier/tests/test_supplier_api.py -v
"""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from apps.supplier.models import Supplier
from apps.supplier.constants import SupplierStatus


# ─────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass123')


@pytest.fixture
def auth_client(api_client, user):
    response = api_client.post('/api/v1/auth/login/', {
        'username': 'testuser',
        'password': 'testpass123',
    }, format='json')
    token = response.data['data']['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.fixture
def supplier(db, user):
    return Supplier.objects.create(
        name='MediCorp Pharma',
        mobile='9876543210',
        address='123 MG Road, Mumbai',
        gst_number='27AAPFU0939F1ZV',
        status=SupplierStatus.ACTIVE,
        created_by=user,
    )


VALID_PAYLOAD = {
    'name': 'Sun Pharma Distributors',
    'mobile': '9123456780',
    'address': '45 Industrial Area, Pune',
    'city': 'Pune',
    'state': 'Maharashtra',
}


# ─────────────────────────────────────────────
# Create Supplier Tests
# ─────────────────────────────────────────────

class TestSupplierCreate:

    def test_create_success(self, auth_client, db):
        response = auth_client.post('/api/v1/suppliers/', VALID_PAYLOAD, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['success'] is True
        assert response.data['data']['name'] == 'Sun Pharma Distributors'
        assert response.data['data']['status'] == 'active'

    def test_create_duplicate_gst(self, auth_client, supplier):
        response = auth_client.post('/api/v1/suppliers/', {
            **VALID_PAYLOAD,
            'gst_number': '27AAPFU0939F1ZV',  # same as fixture
        }, format='json')

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.data['success'] is False

    def test_create_without_gst(self, auth_client, db):
        """GST is optional — should succeed without it."""
        response = auth_client.post('/api/v1/suppliers/', VALID_PAYLOAD, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_invalid_gst_format(self, auth_client, db):
        response = auth_client.post('/api/v1/suppliers/', {
            **VALID_PAYLOAD,
            'gst_number': 'INVALID_GST',
        }, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_missing_required_fields(self, auth_client, db):
        response = auth_client.post('/api/v1/suppliers/', {
            'name': 'Incomplete Supplier',
        }, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_unauthenticated(self, api_client, db):
        response = api_client.post('/api/v1/suppliers/', VALID_PAYLOAD, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ─────────────────────────────────────────────
# List Supplier Tests
# ─────────────────────────────────────────────

class TestSupplierList:

    def test_list_success(self, auth_client, supplier):
        response = auth_client.get('/api/v1/suppliers/')

        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert response.data['count'] >= 1

    def test_list_unauthenticated(self, api_client):
        response = api_client.get('/api/v1/suppliers/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_search_by_name(self, auth_client, supplier):
        response = auth_client.get('/api/v1/suppliers/?search=MediCorp')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1

    def test_filter_by_status_active(self, auth_client, supplier):
        response = auth_client.get('/api/v1/suppliers/?status=active')

        assert response.status_code == status.HTTP_200_OK

    def test_search_by_mobile(self, auth_client, supplier):
        response = auth_client.get(f'/api/v1/suppliers/?search={supplier.mobile}')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1


# ─────────────────────────────────────────────
# Retrieve Supplier Tests
# ─────────────────────────────────────────────

class TestSupplierDetail:

    def test_retrieve_success(self, auth_client, supplier):
        response = auth_client.get(f'/api/v1/suppliers/{supplier.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['id'] == str(supplier.id)
        assert response.data['data']['name'] == supplier.name

    def test_retrieve_not_found(self, auth_client, db):
        response = auth_client.get('/api/v1/suppliers/00000000-0000-0000-0000-000000000000/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


# ─────────────────────────────────────────────
# Update Supplier Tests
# ─────────────────────────────────────────────

class TestSupplierUpdate:

    def test_patch_success(self, auth_client, supplier):
        response = auth_client.patch(f'/api/v1/suppliers/{supplier.id}/', {
            'city': 'Mumbai',
            'remarks': 'Reliable supplier',
        }, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['city'] == 'Mumbai'

    def test_patch_not_found(self, auth_client, db):
        response = auth_client.patch(
            '/api/v1/suppliers/00000000-0000-0000-0000-000000000000/',
            {'city': 'Delhi'},
            format='json',
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_status_change(self, auth_client, supplier):
        response = auth_client.patch(f'/api/v1/suppliers/{supplier.id}/', {
            'status': 'inactive',
        }, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['status'] == 'inactive'


# ─────────────────────────────────────────────
# Soft Delete Tests
# ─────────────────────────────────────────────

class TestSupplierDelete:

    def test_delete_success(self, auth_client, supplier):
        response = auth_client.delete(f'/api/v1/suppliers/{supplier.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify supplier is inactive, not permanently deleted
        supplier.refresh_from_db()
        assert supplier.status == SupplierStatus.INACTIVE

    def test_delete_not_found(self, auth_client, db):
        response = auth_client.delete('/api/v1/suppliers/00000000-0000-0000-0000-000000000000/')

        assert response.status_code == status.HTTP_404_NOT_FOUND
