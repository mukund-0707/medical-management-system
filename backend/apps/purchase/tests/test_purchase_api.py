"""
Tests for Purchase API.
Run: pytest apps/purchase/tests/test_purchase_api.py -v
"""

import pytest
from datetime import date, timedelta
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from apps.supplier.models import Supplier
from apps.medicine.models import Medicine
from apps.purchase.models import Purchase, PurchaseItem
from apps.purchase.constants import PurchaseStatus


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
        'username': 'testuser', 'password': 'testpass123',
    }, format='json')
    token = response.data['data']['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.fixture
def supplier(db, user):
    return Supplier.objects.create(
        name='Test Pharma', mobile='9876543210',
        address='Test Address', created_by=user,
    )


@pytest.fixture
def medicine(db, user):
    return Medicine.objects.create(
        name='Dolo 650', barcode='1234567890',
        manufacturer='Micro Labs', strength='650mg',
        dosage_form='tablet', created_by=user,
    )


@pytest.fixture
def future_date():
    return (date.today() + timedelta(days=365)).isoformat()


@pytest.fixture
def draft_purchase(db, user, supplier, medicine, future_date):
    purchase = Purchase.objects.create(
        supplier=supplier,
        invoice_number='INV-001',
        invoice_date=date.today(),
        status=PurchaseStatus.DRAFT,
        created_by=user,
    )
    PurchaseItem.objects.create(
        purchase=purchase,
        medicine=medicine,
        batch_number='BATCH-001',
        expiry_date=date.today() + timedelta(days=365),
        purchase_price=10.00,
        mrp=15.00,
        quantity=100,
    )
    return purchase


def valid_payload(supplier_id, medicine_id, future_date):
    return {
        'supplier_id': str(supplier_id),
        'invoice_number': 'INV-TEST-001',
        'invoice_date': date.today().isoformat(),
        'items': [{
            'medicine_id': str(medicine_id),
            'batch_number': 'BATCH-A',
            'expiry_date': future_date,
            'purchase_price': '10.00',
            'mrp': '15.00',
            'quantity': 50,
        }],
    }


# ─────────────────────────────────────────────
# Create Purchase Tests
# ─────────────────────────────────────────────

class TestPurchaseCreate:

    def test_create_draft_success(self, auth_client, supplier, medicine, future_date):
        response = auth_client.post(
            '/api/v1/purchases/',
            valid_payload(supplier.id, medicine.id, future_date),
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['data']['status'] == 'draft'
        assert len(response.data['data']['items']) == 1

    def test_create_inactive_supplier(self, auth_client, supplier, medicine, future_date):
        supplier.status = 'inactive'
        supplier.save()

        response = auth_client.post(
            '/api/v1/purchases/',
            valid_payload(supplier.id, medicine.id, future_date),
            format='json',
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_duplicate_invoice(self, auth_client, supplier, medicine, future_date, draft_purchase):
        payload = valid_payload(supplier.id, medicine.id, future_date)
        payload['invoice_number'] = 'INV-001'  # same as draft_purchase

        response = auth_client.post('/api/v1/purchases/', payload, format='json')
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_missing_items(self, auth_client, supplier, future_date):
        response = auth_client.post('/api/v1/purchases/', {
            'supplier_id': str(supplier.id),
            'invoice_number': 'INV-X',
            'invoice_date': date.today().isoformat(),
            'items': [],
        }, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_past_expiry(self, auth_client, supplier, medicine):
        response = auth_client.post('/api/v1/purchases/', {
            'supplier_id': str(supplier.id),
            'invoice_number': 'INV-EXP',
            'invoice_date': date.today().isoformat(),
            'items': [{
                'medicine_id': str(medicine.id),
                'batch_number': 'BATCH-EXP',
                'expiry_date': '2020-01-01',  # past date
                'purchase_price': '10.00',
                'mrp': '15.00',
                'quantity': 10,
            }],
        }, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_duplicate_batch_in_same_purchase(self, auth_client, supplier, medicine, future_date):
        payload = {
            'supplier_id': str(supplier.id),
            'invoice_number': 'INV-DUP',
            'invoice_date': date.today().isoformat(),
            'items': [
                {
                    'medicine_id': str(medicine.id),
                    'batch_number': 'SAME-BATCH',
                    'expiry_date': future_date,
                    'purchase_price': '10.00', 'mrp': '15.00', 'quantity': 10,
                },
                {
                    'medicine_id': str(medicine.id),
                    'batch_number': 'SAME-BATCH',  # duplicate
                    'expiry_date': future_date,
                    'purchase_price': '10.00', 'mrp': '15.00', 'quantity': 5,
                },
            ],
        }
        response = auth_client.post('/api/v1/purchases/', payload, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_unauthenticated(self, api_client, supplier, medicine, future_date):
        response = api_client.post(
            '/api/v1/purchases/',
            valid_payload(supplier.id, medicine.id, future_date),
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ─────────────────────────────────────────────
# List & Retrieve Tests
# ─────────────────────────────────────────────

class TestPurchaseList:

    def test_list_success(self, auth_client, draft_purchase):
        response = auth_client.get('/api/v1/purchases/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1

    def test_filter_by_status(self, auth_client, draft_purchase):
        response = auth_client.get('/api/v1/purchases/?status=draft')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_success(self, auth_client, draft_purchase):
        response = auth_client.get(f'/api/v1/purchases/{draft_purchase.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['invoice_number'] == 'INV-001'

    def test_retrieve_not_found(self, auth_client, db):
        response = auth_client.get('/api/v1/purchases/00000000-0000-0000-0000-000000000000/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ─────────────────────────────────────────────
# Update Tests
# ─────────────────────────────────────────────

class TestPurchaseUpdate:

    def test_patch_draft_success(self, auth_client, draft_purchase):
        response = auth_client.patch(
            f'/api/v1/purchases/{draft_purchase.id}/',
            {'remarks': 'Updated remarks'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

    def test_patch_finalized_rejected(self, auth_client, draft_purchase):
        draft_purchase.status = PurchaseStatus.FINALIZED
        draft_purchase.save()

        response = auth_client.patch(
            f'/api/v1/purchases/{draft_purchase.id}/',
            {'remarks': 'Try to update'},
            format='json',
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# ─────────────────────────────────────────────
# Finalize & Cancel Tests
# (Full inventory tests are in inventory tests)
# ─────────────────────────────────────────────

class TestPurchaseCancel:

    def test_cancel_draft_success(self, auth_client, draft_purchase):
        response = auth_client.post(f'/api/v1/purchases/{draft_purchase.id}/cancel/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['status'] == 'cancelled'

    def test_cancel_already_cancelled(self, auth_client, draft_purchase):
        draft_purchase.status = PurchaseStatus.CANCELLED
        draft_purchase.save()

        response = auth_client.post(f'/api/v1/purchases/{draft_purchase.id}/cancel/')
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
