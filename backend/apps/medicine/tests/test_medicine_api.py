"""
Tests for Medicine API.
Run: pytest apps/medicine/tests/test_medicine_api.py -v
"""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from apps.medicine.models import Medicine
from apps.medicine.constants import MedicineStatus


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
    """Authenticated API client."""
    response = api_client.post('/api/v1/auth/login/', {
        'username': 'testuser',
        'password': 'testpass123',
    }, format='json')
    token = response.data['data']['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.fixture
def medicine(db, user):
    return Medicine.objects.create(
        name='Dolo 650',
        barcode='8901234567890',
        manufacturer='Micro Labs',
        strength='650mg',
        dosage_form='tablet',
        status=MedicineStatus.ACTIVE,
        created_by=user,
    )


# ─────────────────────────────────────────────
# Create Medicine Tests
# ─────────────────────────────────────────────

class TestMedicineCreate:

    def test_create_success(self, auth_client, db):
        response = auth_client.post('/api/v1/medicines/', {
            'name': 'Paracetamol',
            'barcode': '1234567890123',
            'manufacturer': 'Sun Pharma',
            'strength': '500mg',
            'dosage_form': 'tablet',
        }, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['success'] is True
        assert response.data['data']['barcode'] == '1234567890123'

    def test_create_duplicate_barcode(self, auth_client, medicine):
        response = auth_client.post('/api/v1/medicines/', {
            'name': 'Another Medicine',
            'barcode': '8901234567890',  # same barcode as fixture
            'manufacturer': 'Some Company',
            'strength': '500mg',
            'dosage_form': 'tablet',
        }, format='json')

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.data['success'] is False

    def test_create_missing_required_fields(self, auth_client, db):
        response = auth_client.post('/api/v1/medicines/', {
            'name': 'Incomplete Medicine',
        }, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['success'] is False

    def test_create_unauthenticated(self, api_client, db):
        response = api_client.post('/api/v1/medicines/', {
            'name': 'Test',
            'barcode': '111',
            'manufacturer': 'X',
            'strength': '10mg',
        }, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ─────────────────────────────────────────────
# List Medicine Tests
# ─────────────────────────────────────────────

class TestMedicineList:

    def test_list_success(self, auth_client, medicine):
        response = auth_client.get('/api/v1/medicines/')

        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data

    def test_list_unauthenticated(self, api_client):
        response = api_client.get('/api/v1/medicines/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_search_by_name(self, auth_client, medicine):
        response = auth_client.get('/api/v1/medicines/?search=Dolo')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1

    def test_filter_by_status(self, auth_client, medicine):
        response = auth_client.get('/api/v1/medicines/?status=active')

        assert response.status_code == status.HTTP_200_OK


# ─────────────────────────────────────────────
# Retrieve Medicine Tests
# ─────────────────────────────────────────────

class TestMedicineDetail:

    def test_retrieve_success(self, auth_client, medicine):
        response = auth_client.get(f'/api/v1/medicines/{medicine.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['id'] == str(medicine.id)

    def test_retrieve_not_found(self, auth_client, db):
        response = auth_client.get('/api/v1/medicines/00000000-0000-0000-0000-000000000000/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


# ─────────────────────────────────────────────
# Update Medicine Tests
# ─────────────────────────────────────────────

class TestMedicineUpdate:

    def test_patch_success(self, auth_client, medicine):
        response = auth_client.patch(f'/api/v1/medicines/{medicine.id}/', {
            'category': 'Analgesic',
        }, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['category'] == 'Analgesic'

    def test_patch_not_found(self, auth_client, db):
        response = auth_client.patch(
            '/api/v1/medicines/00000000-0000-0000-0000-000000000000/',
            {'category': 'X'},
            format='json',
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ─────────────────────────────────────────────
# Soft Delete Tests
# ─────────────────────────────────────────────

class TestMedicineDelete:

    def test_delete_success(self, auth_client, medicine):
        response = auth_client.delete(f'/api/v1/medicines/{medicine.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify medicine is inactive, not deleted
        medicine.refresh_from_db()
        assert medicine.status == MedicineStatus.INACTIVE

    def test_delete_not_found(self, auth_client, db):
        response = auth_client.delete('/api/v1/medicines/00000000-0000-0000-0000-000000000000/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


# ─────────────────────────────────────────────
# Barcode Lookup Tests
# ─────────────────────────────────────────────

class TestBarcodeLookup:

    def test_barcode_found(self, auth_client, medicine):
        response = auth_client.get(f'/api/v1/medicines/barcode/{medicine.barcode}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['barcode'] == medicine.barcode

    def test_barcode_not_found(self, auth_client, db):
        response = auth_client.get('/api/v1/medicines/barcode/0000000000000/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_barcode_inactive_medicine(self, auth_client, medicine):
        medicine.status = MedicineStatus.INACTIVE
        medicine.save()

        response = auth_client.get(f'/api/v1/medicines/barcode/{medicine.barcode}/')

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
