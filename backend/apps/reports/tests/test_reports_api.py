"""
Tests for Reports Module.
Run: pytest apps/reports/tests/ -v
"""

import pytest
from datetime import date, timedelta
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from apps.medicine.models import Medicine
from apps.supplier.models import Supplier
from apps.purchase.models import Purchase, PurchaseItem
from apps.purchase.constants import PurchaseStatus
from apps.inventory.models import InventoryBatch, InventoryLedger
from apps.inventory.constants import BatchStatus, LedgerMovementType
from apps.sales.models import Sale, SaleItem
from apps.sales.constants import SaleStatus, PaymentMode


# ─────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username='admin', password='testpass123')


@pytest.fixture
def auth_client(api_client, user):
    response = api_client.post('/api/v1/auth/login/', {
        'username': 'admin', 'password': 'testpass123',
    }, format='json')
    token = response.data['data']['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.fixture
def medicine(db, user):
    return Medicine.objects.create(
        name='Dolo 650', barcode='REP-001',
        manufacturer='Micro Labs', strength='650mg',
        dosage_form='tablet', created_by=user,
    )


@pytest.fixture
def supplier(db, user):
    return Supplier.objects.create(
        name='Test Pharma', mobile='9876543210',
        address='Test Address', created_by=user,
    )


@pytest.fixture
def batch(db, medicine):
    return InventoryBatch.objects.create(
        medicine=medicine,
        batch_number='REP-BATCH',
        expiry_date=date.today() + timedelta(days=365),
        purchase_price=10.00, mrp=15.00,
        quantity=100, status=BatchStatus.AVAILABLE,
    )


@pytest.fixture
def expiring_batch(db, medicine):
    return InventoryBatch.objects.create(
        medicine=medicine,
        batch_number='EXP-BATCH',
        expiry_date=date.today() + timedelta(days=15),
        purchase_price=10.00, mrp=15.00,
        quantity=20, status=BatchStatus.AVAILABLE,
    )


@pytest.fixture
def low_batch(db, medicine):
    return InventoryBatch.objects.create(
        medicine=medicine,
        batch_number='LOW-BATCH',
        expiry_date=date.today() + timedelta(days=365),
        purchase_price=10.00, mrp=15.00,
        quantity=3, status=BatchStatus.AVAILABLE,
    )


@pytest.fixture
def completed_sale(db, user, medicine, batch):
    sale = Sale.objects.create(
        invoice_number='REP-INV-001',
        sale_date=date.today(),
        payment_mode=PaymentMode.CASH,
        subtotal=30.00, discount_amount=0,
        gst_amount=3.60, grand_total=33.60,
        status=SaleStatus.COMPLETED, created_by=user,
    )
    SaleItem.objects.create(
        sale=sale, medicine=medicine, inventory_batch=batch,
        quantity=2, unit_price=15.00,
        gst_percentage=12.00, line_total=33.60,
    )
    return sale


@pytest.fixture
def finalized_purchase(db, user, supplier, medicine):
    purchase = Purchase.objects.create(
        supplier=supplier,
        invoice_number='REP-PO-001',
        invoice_date=date.today(),
        status=PurchaseStatus.FINALIZED,
        created_by=user,
    )
    PurchaseItem.objects.create(
        purchase=purchase, medicine=medicine,
        batch_number='REP-PO-BATCH',
        expiry_date=date.today() + timedelta(days=365),
        purchase_price=10.00, mrp=15.00, quantity=50,
    )
    return purchase


@pytest.fixture
def adjustment_ledger(db, user, medicine, batch):
    return InventoryLedger.objects.create(
        inventory_batch=batch,
        medicine=medicine,
        movement_type=LedgerMovementType.ADJUSTMENT,
        quantity=-5,
        quantity_before=100,
        quantity_after=95,
        reason='[damage] Physical damage found',
        created_by=user,
    )


# ─────────────────────────────────────────────
# Sales Report Tests
# ─────────────────────────────────────────────

class TestSalesReport:

    def test_sales_report_empty(self, auth_client, db):
        response = auth_client.get('/api/v1/reports/sales/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0

    def test_sales_report_with_data(self, auth_client, completed_sale):
        response = auth_client.get('/api/v1/reports/sales/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_sales_report_date_filter(self, auth_client, completed_sale):
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        response = auth_client.get(
            f'/api/v1/reports/sales/?date_from={yesterday}&date_to={yesterday}'
        )
        assert response.data['count'] == 0

    def test_sales_report_payment_filter(self, auth_client, completed_sale):
        response = auth_client.get('/api/v1/reports/sales/?payment_mode=cash')
        assert response.data['count'] == 1

        response = auth_client.get('/api/v1/reports/sales/?payment_mode=upi')
        assert response.data['count'] == 0

    def test_sales_report_search(self, auth_client, completed_sale):
        response = auth_client.get('/api/v1/reports/sales/?search=REP-INV')
        assert response.data['count'] == 1

    def test_sales_report_unauthenticated(self, api_client):
        response = api_client.get('/api/v1/reports/sales/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ─────────────────────────────────────────────
# Purchase Report Tests
# ─────────────────────────────────────────────

class TestPurchaseReport:

    def test_purchase_report_empty(self, auth_client, db):
        response = auth_client.get('/api/v1/reports/purchases/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0

    def test_purchase_report_with_data(self, auth_client, finalized_purchase):
        response = auth_client.get('/api/v1/reports/purchases/')
        assert response.data['count'] == 1

    def test_purchase_report_supplier_filter(self, auth_client, finalized_purchase):
        response = auth_client.get(
            f'/api/v1/reports/purchases/?supplier={finalized_purchase.supplier.id}'
        )
        assert response.data['count'] == 1

    def test_purchase_report_status_filter(self, auth_client, finalized_purchase):
        response = auth_client.get('/api/v1/reports/purchases/?status=finalized')
        assert response.data['count'] == 1

        response = auth_client.get('/api/v1/reports/purchases/?status=draft')
        assert response.data['count'] == 0


# ─────────────────────────────────────────────
# Inventory Report Tests
# ─────────────────────────────────────────────

class TestInventoryReport:

    def test_inventory_report(self, auth_client, batch):
        response = auth_client.get('/api/v1/reports/inventory/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1

    def test_inventory_filter_by_medicine(self, auth_client, batch, medicine):
        response = auth_client.get(f'/api/v1/reports/inventory/?medicine={medicine.id}')
        assert response.data['count'] == 1

    def test_inventory_filter_by_status(self, auth_client, batch):
        response = auth_client.get('/api/v1/reports/inventory/?status=available')
        assert response.data['count'] >= 1


# ─────────────────────────────────────────────
# Ledger Report Tests
# ─────────────────────────────────────────────

class TestLedgerReport:

    def test_ledger_empty(self, auth_client, db):
        response = auth_client.get('/api/v1/reports/ledger/')
        assert response.status_code == status.HTTP_200_OK

    def test_ledger_with_entries(self, auth_client, adjustment_ledger):
        response = auth_client.get('/api/v1/reports/ledger/')
        assert response.data['count'] >= 1

    def test_ledger_movement_type_filter(self, auth_client, adjustment_ledger):
        response = auth_client.get('/api/v1/reports/ledger/?movement_type=adjustment')
        assert response.data['count'] >= 1


# ─────────────────────────────────────────────
# Expiry Report Tests
# ─────────────────────────────────────────────

class TestExpiryReport:

    def test_expiry_report_no_expiry(self, auth_client, batch):
        # batch expires in 365 days, default 90 days threshold
        response = auth_client.get('/api/v1/reports/expiry/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0

    def test_expiry_report_catches_expiring(self, auth_client, expiring_batch):
        response = auth_client.get('/api/v1/reports/expiry/?days=30')
        assert response.data['count'] >= 1

    def test_expiry_report_custom_days(self, auth_client, expiring_batch):
        response = auth_client.get('/api/v1/reports/expiry/?days=365')
        assert response.data['count'] >= 1


# ─────────────────────────────────────────────
# Low Stock Report Tests
# ─────────────────────────────────────────────

class TestLowStockReport:

    def test_low_stock_empty(self, auth_client, batch):
        # batch has 100 qty, threshold=10 → no low stock
        response = auth_client.get('/api/v1/reports/low-stock/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0

    def test_low_stock_detected(self, auth_client, low_batch):
        response = auth_client.get('/api/v1/reports/low-stock/')
        assert response.data['count'] >= 1

    def test_low_stock_custom_threshold(self, auth_client, batch):
        # batch has 100 qty, threshold=200 → caught
        response = auth_client.get('/api/v1/reports/low-stock/?threshold=200')
        assert response.data['count'] >= 1


# ─────────────────────────────────────────────
# Adjustment Report Tests
# ─────────────────────────────────────────────

class TestAdjustmentReport:

    def test_adjustment_report_empty(self, auth_client, db):
        response = auth_client.get('/api/v1/reports/adjustments/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0

    def test_adjustment_report_with_data(self, auth_client, adjustment_ledger):
        response = auth_client.get('/api/v1/reports/adjustments/')
        assert response.data['count'] == 1

    def test_adjustment_filter_medicine(self, auth_client, adjustment_ledger, medicine):
        response = auth_client.get(
            f'/api/v1/reports/adjustments/?medicine={medicine.id}'
        )
        assert response.data['count'] == 1


# ─────────────────────────────────────────────
# Medicine & Supplier Report Tests
# ─────────────────────────────────────────────

class TestMedicineReport:

    def test_medicine_report(self, auth_client, medicine):
        response = auth_client.get('/api/v1/reports/medicines/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1

    def test_medicine_search(self, auth_client, medicine):
        response = auth_client.get('/api/v1/reports/medicines/?search=Dolo')
        assert response.data['count'] >= 1


class TestSupplierReport:

    def test_supplier_report(self, auth_client, supplier):
        response = auth_client.get('/api/v1/reports/suppliers/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1

    def test_supplier_search(self, auth_client, supplier):
        response = auth_client.get('/api/v1/reports/suppliers/?search=Test Pharma')
        assert response.data['count'] >= 1
