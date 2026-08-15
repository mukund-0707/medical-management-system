"""
Tests for Sales Module.
Covers full checkout flow end-to-end.
Run: pytest apps/sales/tests/test_sales_api.py -v
"""

import pytest
from datetime import date, timedelta
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from apps.medicine.models import Medicine
from apps.inventory.models import InventoryBatch, InventoryLedger
from apps.inventory.constants import BatchStatus, LedgerMovementType
from apps.billing.models import BillingSession, BillingSessionItem
from apps.billing.constants import SessionStatus
from apps.sales.models import Sale, SaleItem
from apps.sales.constants import SaleStatus


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
        name='Dolo 650', barcode='SALE-001',
        manufacturer='Micro Labs', strength='650mg',
        dosage_form='tablet', created_by=user,
    )


@pytest.fixture
def medicine2(db, user):
    return Medicine.objects.create(
        name='Crocin 500', barcode='SALE-002',
        manufacturer='GSK', strength='500mg',
        dosage_form='tablet', created_by=user,
    )


@pytest.fixture
def batch(db, medicine):
    return InventoryBatch.objects.create(
        medicine=medicine,
        batch_number='SALE-BATCH-001',
        expiry_date=date.today() + timedelta(days=365),
        purchase_price=10.00,
        mrp=15.00,
        gst_percentage=12.00,
        quantity=100,
        status=BatchStatus.AVAILABLE,
    )


@pytest.fixture
def batch2(db, medicine2):
    return InventoryBatch.objects.create(
        medicine=medicine2,
        batch_number='SALE-BATCH-002',
        expiry_date=date.today() + timedelta(days=365),
        purchase_price=8.00,
        mrp=12.00,
        gst_percentage=12.00,
        quantity=50,
        status=BatchStatus.AVAILABLE,
    )


@pytest.fixture
def session_with_items(db, user, medicine, medicine2, batch, batch2):
    """Active billing session with 2 items."""
    session = BillingSession.objects.create(
        status=SessionStatus.ACTIVE,
        subtotal=39.00,
        discount_amount=0,
        gst_amount=4.68,
        grand_total=43.68,
        created_by=user,
    )
    BillingSessionItem.objects.create(
        session=session,
        medicine=medicine,
        quantity=2,
        unit_price=15.00,
        gst_percentage=12.00,
        line_total=33.60,
    )
    BillingSessionItem.objects.create(
        session=session,
        medicine=medicine2,
        quantity=1,
        unit_price=12.00,
        gst_percentage=12.00,
        line_total=13.44,
    )
    return session


# ─────────────────────────────────────────────
# Full Checkout Flow Tests
# ─────────────────────────────────────────────

class TestCheckout:

    def test_checkout_success(self, auth_client, session_with_items, batch, batch2):
        """Full end-to-end checkout test."""
        response = auth_client.post('/api/v1/sales/checkout/', {
            'session_id': str(session_with_items.id),
            'payment_mode': 'cash',
        }, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True

        data = response.data['data']
        assert data['status'] == 'completed'
        assert data['invoice_number'].startswith('INV-')
        assert len(data['items']) == 2

    def test_checkout_reduces_inventory(self, auth_client, session_with_items, batch, batch2):
        """Verify stock is reduced after checkout."""
        auth_client.post('/api/v1/sales/checkout/', {
            'session_id': str(session_with_items.id),
            'payment_mode': 'upi',
        }, format='json')

        batch.refresh_from_db()
        batch2.refresh_from_db()
        assert batch.quantity == 98   # was 100, sold 2
        assert batch2.quantity == 49  # was 50, sold 1

    def test_checkout_creates_ledger_entries(self, auth_client, session_with_items, batch, batch2):
        """Verify ledger entries created for each item."""
        auth_client.post('/api/v1/sales/checkout/', {
            'session_id': str(session_with_items.id),
            'payment_mode': 'cash',
        }, format='json')

        sale_ledgers = InventoryLedger.objects.filter(
            movement_type=LedgerMovementType.SALE
        )
        assert sale_ledgers.count() == 2

    def test_checkout_marks_session_checked_out(self, auth_client, session_with_items, batch, batch2):
        """Session status becomes checked_out after checkout."""
        auth_client.post('/api/v1/sales/checkout/', {
            'session_id': str(session_with_items.id),
            'payment_mode': 'cash',
        }, format='json')

        session_with_items.refresh_from_db()
        assert session_with_items.status == SessionStatus.CHECKED_OUT

    def test_checkout_generates_unique_invoice_numbers(
        self, auth_client, user, medicine, batch, db
    ):
        """Two checkouts on same day must have different invoice numbers."""
        def make_session_and_checkout():
            s = BillingSession.objects.create(
                status=SessionStatus.ACTIVE,
                subtotal=15, grand_total=16.80,
                gst_amount=1.80, created_by=user,
            )
            BillingSessionItem.objects.create(
                session=s, medicine=medicine,
                quantity=1, unit_price=15.00,
                gst_percentage=12.00, line_total=16.80,
            )
            resp = auth_client.post('/api/v1/sales/checkout/', {
                'session_id': str(s.id), 'payment_mode': 'cash',
            }, format='json')
            return resp.data['data']['invoice_number']

        inv1 = make_session_and_checkout()
        inv2 = make_session_and_checkout()

        assert inv1 != inv2

    def test_checkout_empty_session_rejected(self, auth_client, db, user):
        """Empty cart cannot be checked out."""
        empty_session = BillingSession.objects.create(
            status=SessionStatus.ACTIVE, created_by=user
        )
        response = auth_client.post('/api/v1/sales/checkout/', {
            'session_id': str(empty_session.id),
            'payment_mode': 'cash',
        }, format='json')
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_checkout_cancelled_session_rejected(self, auth_client, db, user):
        """Cancelled session cannot be checked out."""
        cancelled = BillingSession.objects.create(
            status=SessionStatus.CANCELLED, created_by=user
        )
        response = auth_client.post('/api/v1/sales/checkout/', {
            'session_id': str(cancelled.id),
            'payment_mode': 'cash',
        }, format='json')
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_checkout_insufficient_stock_rollback(self, auth_client, user, medicine, db):
        """If stock runs out during checkout, entire transaction rolls back."""
        low_batch = InventoryBatch.objects.create(
            medicine=medicine, batch_number='LOW-BATCH',
            expiry_date=date.today() + timedelta(days=365),
            purchase_price=10, mrp=15, quantity=1,
            status=BatchStatus.AVAILABLE,
        )
        session = BillingSession.objects.create(
            status=SessionStatus.ACTIVE,
            subtotal=30, grand_total=33.60,
            gst_amount=3.60, created_by=user,
        )
        BillingSessionItem.objects.create(
            session=session, medicine=medicine,
            quantity=5,  # more than available (1)
            unit_price=15.00, gst_percentage=12.00, line_total=16.80,
        )

        response = auth_client.post('/api/v1/sales/checkout/', {
            'session_id': str(session.id),
            'payment_mode': 'cash',
        }, format='json')

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Verify no Sale was created (rollback)
        assert not Sale.objects.filter(billing_session_id=session.id).exists()

        # Verify stock was NOT reduced (rollback)
        low_batch.refresh_from_db()
        assert low_batch.quantity == 1

    def test_checkout_unauthenticated(self, api_client, db):
        response = api_client.post('/api/v1/sales/checkout/', {
            'session_id': '00000000-0000-0000-0000-000000000000',
            'payment_mode': 'cash',
        }, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ─────────────────────────────────────────────
# Sale List & Detail Tests
# ─────────────────────────────────────────────

class TestSaleList:

    def test_list_empty(self, auth_client, db):
        response = auth_client.get('/api/v1/sales/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0

    def test_list_after_checkout(self, auth_client, session_with_items, batch, batch2):
        auth_client.post('/api/v1/sales/checkout/', {
            'session_id': str(session_with_items.id),
            'payment_mode': 'cash',
        }, format='json')

        response = auth_client.get('/api/v1/sales/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_filter_by_payment_mode(self, auth_client, session_with_items, batch, batch2):
        auth_client.post('/api/v1/sales/checkout/', {
            'session_id': str(session_with_items.id),
            'payment_mode': 'upi',
        }, format='json')

        response = auth_client.get('/api/v1/sales/?payment_mode=upi')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

        response = auth_client.get('/api/v1/sales/?payment_mode=cash')
        assert response.data['count'] == 0


class TestSaleDetail:

    def test_get_by_id(self, auth_client, session_with_items, batch, batch2):
        resp = auth_client.post('/api/v1/sales/checkout/', {
            'session_id': str(session_with_items.id),
            'payment_mode': 'cash',
        }, format='json')
        sale_id = resp.data['data']['id']

        response = auth_client.get(f'/api/v1/sales/{sale_id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['id'] == sale_id

    def test_get_by_invoice(self, auth_client, session_with_items, batch, batch2):
        resp = auth_client.post('/api/v1/sales/checkout/', {
            'session_id': str(session_with_items.id),
            'payment_mode': 'cash',
        }, format='json')
        invoice = resp.data['data']['invoice_number']

        response = auth_client.get(f'/api/v1/sales/invoice/{invoice}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['invoice_number'] == invoice

    def test_get_not_found(self, auth_client, db):
        response = auth_client.get('/api/v1/sales/00000000-0000-0000-0000-000000000000/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ─────────────────────────────────────────────
# Sale Cancel Tests
# ─────────────────────────────────────────────

class TestSaleCancel:

    def test_cancel_success(self, auth_client, session_with_items, batch, batch2):
        resp = auth_client.post('/api/v1/sales/checkout/', {
            'session_id': str(session_with_items.id),
            'payment_mode': 'cash',
        }, format='json')
        sale_id = resp.data['data']['id']

        response = auth_client.post(f'/api/v1/sales/{sale_id}/cancel/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['status'] == 'cancelled'

    def test_cancel_already_cancelled(self, auth_client, session_with_items, batch, batch2):
        resp = auth_client.post('/api/v1/sales/checkout/', {
            'session_id': str(session_with_items.id),
            'payment_mode': 'cash',
        }, format='json')
        sale_id = resp.data['data']['id']

        auth_client.post(f'/api/v1/sales/{sale_id}/cancel/')
        response = auth_client.post(f'/api/v1/sales/{sale_id}/cancel/')
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
