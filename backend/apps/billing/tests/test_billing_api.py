"""
Tests for Billing Session API.
Run: pytest apps/billing/tests/test_billing_api.py -v
"""

import pytest
from datetime import date, timedelta
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from apps.medicine.models import Medicine
from apps.medicine.constants import MedicineStatus
from apps.inventory.models import InventoryBatch
from apps.inventory.constants import BatchStatus
from apps.billing.models import BillingSession, BillingSessionItem
from apps.billing.constants import SessionStatus


# ─────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username='cashier', password='testpass123')


@pytest.fixture
def auth_client(api_client, user):
    response = api_client.post('/api/v1/auth/login/', {
        'username': 'cashier', 'password': 'testpass123',
    }, format='json')
    token = response.data['data']['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.fixture
def medicine(db, user):
    return Medicine.objects.create(
        name='Dolo 650', barcode='BILL-001',
        manufacturer='Micro Labs', strength='650mg',
        dosage_form='tablet', created_by=user,
    )


@pytest.fixture
def medicine2(db, user):
    return Medicine.objects.create(
        name='Crocin 500', barcode='BILL-002',
        manufacturer='GSK', strength='500mg',
        dosage_form='tablet', created_by=user,
    )


@pytest.fixture
def batch(db, medicine):
    """Inventory batch with 50 units available."""
    return InventoryBatch.objects.create(
        medicine=medicine,
        batch_number='BILL-BATCH-001',
        expiry_date=date.today() + timedelta(days=365),
        purchase_price=10.00,
        mrp=15.00,
        gst_percentage=12.00,
        quantity=50,
        status=BatchStatus.AVAILABLE,
    )


@pytest.fixture
def batch2(db, medicine2):
    return InventoryBatch.objects.create(
        medicine=medicine2,
        batch_number='BILL-BATCH-002',
        expiry_date=date.today() + timedelta(days=365),
        purchase_price=8.00,
        mrp=12.00,
        gst_percentage=12.00,
        quantity=30,
        status=BatchStatus.AVAILABLE,
    )


@pytest.fixture
def active_session(db, user):
    return BillingSession.objects.create(
        status=SessionStatus.ACTIVE,
        created_by=user,
    )


# ─────────────────────────────────────────────
# Create Session Tests
# ─────────────────────────────────────────────

class TestCreateSession:

    def test_create_success(self, auth_client, db):
        response = auth_client.post('/api/v1/billing/sessions/')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['data']['status'] == 'active'
        assert response.data['data']['grand_total'] == '0.00'

    def test_create_unauthenticated(self, api_client):
        response = api_client.post('/api/v1/billing/sessions/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ─────────────────────────────────────────────
# Get Session Tests
# ─────────────────────────────────────────────

class TestGetSession:

    def test_get_success(self, auth_client, active_session):
        response = auth_client.get(f'/api/v1/billing/sessions/{active_session.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['id'] == str(active_session.id)

    def test_get_not_found(self, auth_client, db):
        response = auth_client.get('/api/v1/billing/sessions/00000000-0000-0000-0000-000000000000/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ─────────────────────────────────────────────
# Add Item Tests
# ─────────────────────────────────────────────

class TestAddItem:

    def test_add_item_success(self, auth_client, active_session, medicine, batch):
        response = auth_client.post(
            f'/api/v1/billing/sessions/{active_session.id}/items/',
            {'medicine_id': str(medicine.id), 'quantity': 5},
            format='json',
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['data']['items']) == 1
        assert response.data['data']['items'][0]['quantity'] == 5

    def test_add_same_medicine_increases_quantity(self, auth_client, active_session, medicine, batch):
        # Add once
        auth_client.post(
            f'/api/v1/billing/sessions/{active_session.id}/items/',
            {'medicine_id': str(medicine.id), 'quantity': 5},
            format='json',
        )
        # Add again
        response = auth_client.post(
            f'/api/v1/billing/sessions/{active_session.id}/items/',
            {'medicine_id': str(medicine.id), 'quantity': 3},
            format='json',
        )

        assert response.status_code == status.HTTP_200_OK
        # Should be 8, not two separate rows
        assert response.data['data']['items'][0]['quantity'] == 8
        assert len(response.data['data']['items']) == 1

    def test_add_exceeds_stock(self, auth_client, active_session, medicine, batch):
        response = auth_client.post(
            f'/api/v1/billing/sessions/{active_session.id}/items/',
            {'medicine_id': str(medicine.id), 'quantity': 999},
            format='json',
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_add_inactive_medicine(self, auth_client, active_session, medicine, batch):
        medicine.status = MedicineStatus.INACTIVE
        medicine.save()

        response = auth_client.post(
            f'/api/v1/billing/sessions/{active_session.id}/items/',
            {'medicine_id': str(medicine.id), 'quantity': 2},
            format='json',
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_add_to_cancelled_session(self, auth_client, medicine, batch, db, user):
        cancelled = BillingSession.objects.create(
            status=SessionStatus.CANCELLED, created_by=user
        )
        response = auth_client.post(
            f'/api/v1/billing/sessions/{cancelled.id}/items/',
            {'medicine_id': str(medicine.id), 'quantity': 2},
            format='json',
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_totals_calculated_correctly(self, auth_client, active_session, medicine, batch):
        response = auth_client.post(
            f'/api/v1/billing/sessions/{active_session.id}/items/',
            {'medicine_id': str(medicine.id), 'quantity': 2},
            format='json',
        )
        # MRP=15, qty=2, GST=12%
        # base = 30, gst = 3.60, total = 33.60
        data = response.data['data']
        assert float(data['subtotal']) == 30.0
        assert float(data['grand_total']) == 33.60


# ─────────────────────────────────────────────
# Update Item Tests
# ─────────────────────────────────────────────

class TestUpdateItem:

    def test_update_quantity(self, auth_client, active_session, medicine, batch):
        # Add item first
        auth_client.post(
            f'/api/v1/billing/sessions/{active_session.id}/items/',
            {'medicine_id': str(medicine.id), 'quantity': 5},
            format='json',
        )
        item = BillingSessionItem.objects.get(session=active_session)

        response = auth_client.patch(
            f'/api/v1/billing/sessions/{active_session.id}/items/{item.id}/',
            {'quantity': 10},
            format='json',
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['items'][0]['quantity'] == 10

    def test_update_exceeds_stock(self, auth_client, active_session, medicine, batch):
        auth_client.post(
            f'/api/v1/billing/sessions/{active_session.id}/items/',
            {'medicine_id': str(medicine.id), 'quantity': 5},
            format='json',
        )
        item = BillingSessionItem.objects.get(session=active_session)

        response = auth_client.patch(
            f'/api/v1/billing/sessions/{active_session.id}/items/{item.id}/',
            {'quantity': 9999},
            format='json',
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# ─────────────────────────────────────────────
# Remove Item Tests
# ─────────────────────────────────────────────

class TestRemoveItem:

    def test_remove_item_success(self, auth_client, active_session, medicine, batch):
        auth_client.post(
            f'/api/v1/billing/sessions/{active_session.id}/items/',
            {'medicine_id': str(medicine.id), 'quantity': 3},
            format='json',
        )
        item = BillingSessionItem.objects.get(session=active_session)

        response = auth_client.delete(
            f'/api/v1/billing/sessions/{active_session.id}/items/{item.id}/'
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not BillingSessionItem.objects.filter(id=item.id).exists()


# ─────────────────────────────────────────────
# Cancel Session Tests
# ─────────────────────────────────────────────

class TestCancelSession:

    def test_cancel_success(self, auth_client, active_session):
        response = auth_client.delete(f'/api/v1/billing/sessions/{active_session.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        active_session.refresh_from_db()
        assert active_session.status == SessionStatus.CANCELLED

    def test_cancel_already_cancelled(self, auth_client, db, user):
        session = BillingSession.objects.create(
            status=SessionStatus.CANCELLED, created_by=user
        )
        response = auth_client.delete(f'/api/v1/billing/sessions/{session.id}/')
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
