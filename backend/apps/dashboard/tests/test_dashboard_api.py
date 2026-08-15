"""
Tests for Dashboard API.
Run: pytest apps/dashboard/tests/ -v
"""

import pytest
from datetime import date, timedelta
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from apps.medicine.models import Medicine
from apps.inventory.models import InventoryBatch
from apps.inventory.constants import BatchStatus
from apps.sales.models import Sale, SaleItem
from apps.sales.constants import SaleStatus, PaymentMode
from apps.purchase.models import Purchase
from apps.purchase.constants import PurchaseStatus
from apps.supplier.models import Supplier


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
        name='Dolo 650', barcode='DASH-001',
        manufacturer='Micro Labs', strength='650mg',
        dosage_form='tablet', created_by=user,
    )


@pytest.fixture
def batch(db, medicine):
    return InventoryBatch.objects.create(
        medicine=medicine,
        batch_number='DASH-BATCH',
        expiry_date=date.today() + timedelta(days=365),
        purchase_price=10.00,
        mrp=15.00,
        quantity=100,
        status=BatchStatus.AVAILABLE,
    )


@pytest.fixture
def low_stock_batch(db, medicine):
    return InventoryBatch.objects.create(
        medicine=medicine,
        batch_number='LOW-BATCH',
        expiry_date=date.today() + timedelta(days=365),
        purchase_price=10.00,
        mrp=15.00,
        quantity=5,  # <= LOW_STOCK_THRESHOLD (10)
        status=BatchStatus.AVAILABLE,
    )


@pytest.fixture
def expiring_batch(db, medicine):
    return InventoryBatch.objects.create(
        medicine=medicine,
        batch_number='EXP-SOON',
        expiry_date=date.today() + timedelta(days=10),  # expiring in 10 days
        purchase_price=10.00,
        mrp=15.00,
        quantity=20,
        status=BatchStatus.AVAILABLE,
    )


@pytest.fixture
def expired_batch(db, medicine):
    return InventoryBatch.objects.create(
        medicine=medicine,
        batch_number='EXPIRED',
        expiry_date=date.today() - timedelta(days=5),  # already expired
        purchase_price=10.00,
        mrp=15.00,
        quantity=10,
        status=BatchStatus.AVAILABLE,
    )


@pytest.fixture
def completed_sale(db, user, medicine, batch):
    sale = Sale.objects.create(
        invoice_number='INV-DASH-001',
        sale_date=date.today(),
        payment_mode=PaymentMode.CASH,
        subtotal=30.00,
        discount_amount=0,
        gst_amount=3.60,
        grand_total=33.60,
        status=SaleStatus.COMPLETED,
        created_by=user,
    )
    SaleItem.objects.create(
        sale=sale,
        medicine=medicine,
        inventory_batch=batch,
        quantity=2,
        unit_price=15.00,
        gst_percentage=12.00,
        line_total=33.60,
    )
    return sale


# ─────────────────────────────────────────────
# KPI Tests
# ─────────────────────────────────────────────

class TestDashboardKPI:

    def test_kpi_success(self, auth_client, db):
        response = auth_client.get('/api/v1/dashboard/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        data = response.data['data']
        assert 'sales' in data
        assert 'purchases' in data
        assert 'inventory' in data

    def test_kpi_with_no_data_returns_zeros(self, auth_client, db):
        response = auth_client.get('/api/v1/dashboard/')
        assert response.status_code == status.HTTP_200_OK
        data = response.data['data']
        assert data['sales']['today_invoice_count'] == 0

    def test_kpi_counts_todays_sale(self, auth_client, completed_sale):
        response = auth_client.get('/api/v1/dashboard/')
        data = response.data['data']
        assert data['sales']['today_invoice_count'] == 1

    def test_kpi_unauthenticated(self, api_client):
        response = api_client.get('/api/v1/dashboard/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ─────────────────────────────────────────────
# Sales Summary Tests
# ─────────────────────────────────────────────

class TestDashboardSales:

    def test_sales_summary_empty(self, auth_client, db):
        response = auth_client.get('/api/v1/dashboard/sales/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['invoice_count'] == 0

    def test_sales_summary_with_sale(self, auth_client, completed_sale):
        response = auth_client.get('/api/v1/dashboard/sales/')
        data = response.data['data']
        assert data['invoice_count'] == 1
        assert float(data['total_amount']) == 33.60

    def test_sales_summary_date_filter(self, auth_client, completed_sale):
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        response = auth_client.get(
            f'/api/v1/dashboard/sales/?date_from={yesterday}&date_to={yesterday}'
        )
        assert response.data['data']['invoice_count'] == 0


# ─────────────────────────────────────────────
# Inventory Summary Tests
# ─────────────────────────────────────────────

class TestDashboardInventory:

    def test_inventory_summary(self, auth_client, batch):
        response = auth_client.get('/api/v1/dashboard/inventory/')
        assert response.status_code == status.HTTP_200_OK
        data = response.data['data']
        assert 'low_stock_medicines' in data
        assert 'expiring_in_30_days' in data
        assert 'expired_with_stock' in data

    def test_low_stock_detected(self, auth_client, low_stock_batch):
        response = auth_client.get('/api/v1/dashboard/inventory/')
        data = response.data['data']
        assert len(data['low_stock_medicines']) >= 1

    def test_expiring_detected(self, auth_client, expiring_batch):
        response = auth_client.get('/api/v1/dashboard/inventory/')
        data = response.data['data']
        assert len(data['expiring_in_30_days']) >= 1

    def test_expired_detected(self, auth_client, expired_batch):
        response = auth_client.get('/api/v1/dashboard/inventory/')
        data = response.data['data']
        assert len(data['expired_with_stock']) >= 1


# ─────────────────────────────────────────────
# Alerts Tests
# ─────────────────────────────────────────────

class TestDashboardAlerts:

    def test_no_alerts_when_clean(self, auth_client, batch):
        response = auth_client.get('/api/v1/dashboard/alerts/')
        assert response.status_code == status.HTTP_200_OK
        # batch is fine — no alerts
        data = response.data['data']
        assert data['total_alerts'] == 0

    def test_expired_alert_triggered(self, auth_client, expired_batch):
        response = auth_client.get('/api/v1/dashboard/alerts/')
        data = response.data['data']
        assert data['total_alerts'] >= 1
        alert_types = [a['title'] for a in data['alerts']]
        assert 'Expired Medicines' in alert_types

    def test_low_stock_alert_triggered(self, auth_client, low_stock_batch):
        response = auth_client.get('/api/v1/dashboard/alerts/')
        data = response.data['data']
        assert data['total_alerts'] >= 1
        alert_types = [a['title'] for a in data['alerts']]
        assert 'Low Stock' in alert_types

    def test_alerts_sorted_by_priority(self, auth_client, expired_batch, low_stock_batch):
        """Expired should appear before low stock (priority 1 vs 3)."""
        response = auth_client.get('/api/v1/dashboard/alerts/')
        alerts = response.data['data']['alerts']
        priorities = [a['priority'] for a in alerts]
        assert priorities == sorted(priorities)
