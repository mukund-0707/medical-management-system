"""
Tests for Inventory Module.
Covers: batch creation via purchase, FEFO deduction, adjustment, mark expired.
Run: pytest apps/inventory/tests/test_inventory_api.py -v
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
from apps.inventory.models import InventoryBatch, InventoryLedger
from apps.inventory.constants import BatchStatus, LedgerMovementType
from apps.inventory.services.inventory_service import InventoryService


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
        name='Dolo 650', barcode='TEST-001',
        manufacturer='Micro Labs', strength='650mg',
        dosage_form='tablet', created_by=user,
    )


@pytest.fixture
def purchase_with_item(db, user, supplier, medicine):
    purchase = Purchase.objects.create(
        supplier=supplier,
        invoice_number='INV-001',
        invoice_date=date.today(),
        status=PurchaseStatus.DRAFT,
        created_by=user,
    )
    item = PurchaseItem.objects.create(
        purchase=purchase,
        medicine=medicine,
        batch_number='BATCH-001',
        expiry_date=date.today() + timedelta(days=365),
        purchase_price=10.00,
        mrp=15.00,
        quantity=100,
    )
    return purchase, item


@pytest.fixture
def inventory_batch(db, user, medicine):
    """Direct batch — not via purchase."""
    return InventoryBatch.objects.create(
        medicine=medicine,
        batch_number='DIRECT-BATCH',
        expiry_date=date.today() + timedelta(days=365),
        purchase_price=10.00,
        mrp=15.00,
        quantity=50,
        status=BatchStatus.AVAILABLE,
    )


# ─────────────────────────────────────────────
# create_from_purchase Tests
# ─────────────────────────────────────────────

class TestCreateFromPurchase:

    def test_creates_batch_and_ledger(self, db, user, purchase_with_item):
        purchase, item = purchase_with_item

        batch = InventoryService.create_from_purchase(item, created_by=user)

        assert batch.quantity == 100
        assert batch.status == BatchStatus.AVAILABLE
        assert batch.batch_number == 'BATCH-001'

        ledger = InventoryLedger.objects.get(inventory_batch=batch)
        assert ledger.movement_type == LedgerMovementType.PURCHASE
        assert ledger.quantity == 100
        assert ledger.quantity_before == 0
        assert ledger.quantity_after == 100

    def test_full_purchase_finalize_via_api(self, auth_client, user, supplier, medicine):
        """Full flow via API — create purchase, finalize, check inventory."""
        future = (date.today() + timedelta(days=365)).isoformat()

        # Create purchase
        response = auth_client.post('/api/v1/purchases/', {
            'supplier_id': str(supplier.id),
            'invoice_number': 'INV-FULL',
            'invoice_date': date.today().isoformat(),
            'items': [{
                'medicine_id': str(medicine.id),
                'batch_number': 'BATCH-FULL',
                'expiry_date': future,
                'purchase_price': '10.00',
                'mrp': '15.00',
                'quantity': 50,
            }],
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        purchase_id = response.data['data']['id']

        # Finalize
        response = auth_client.post(f'/api/v1/purchases/{purchase_id}/finalize/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['status'] == 'finalized'

        # Check inventory created
        assert InventoryBatch.objects.filter(batch_number='BATCH-FULL').exists()
        batch = InventoryBatch.objects.get(batch_number='BATCH-FULL')
        assert batch.quantity == 50
        assert InventoryLedger.objects.filter(inventory_batch=batch).exists()


# ─────────────────────────────────────────────
# FEFO reduce_for_sale Tests
# ─────────────────────────────────────────────

class TestReduceForSale:

    def test_reduce_single_batch(self, db, user, medicine, inventory_batch):
        deductions = InventoryService.reduce_for_sale(
            medicine_id=str(medicine.id),
            quantity=10,
            sale_id='SALE-001',
            created_by=user,
        )

        assert len(deductions) == 1
        assert deductions[0]['quantity_deducted'] == 10

        inventory_batch.refresh_from_db()
        assert inventory_batch.quantity == 40

        ledger = InventoryLedger.objects.filter(
            inventory_batch=inventory_batch,
            movement_type=LedgerMovementType.SALE,
        ).first()
        assert ledger is not None
        assert ledger.quantity == -10

    def test_reduce_multi_batch_fefo(self, db, user, medicine):
        """FEFO — nearest expiry batch consumed first."""
        batch_near = InventoryBatch.objects.create(
            medicine=medicine, batch_number='NEAR',
            expiry_date=date.today() + timedelta(days=30),
            purchase_price=10, mrp=15, quantity=5,
            status=BatchStatus.AVAILABLE,
        )
        batch_far = InventoryBatch.objects.create(
            medicine=medicine, batch_number='FAR',
            expiry_date=date.today() + timedelta(days=365),
            purchase_price=10, mrp=15, quantity=20,
            status=BatchStatus.AVAILABLE,
        )

        deductions = InventoryService.reduce_for_sale(
            medicine_id=str(medicine.id),
            quantity=10,
            sale_id='SALE-FEFO',
            created_by=user,
        )

        assert len(deductions) == 2

        batch_near.refresh_from_db()
        batch_far.refresh_from_db()
        assert batch_near.quantity == 0
        assert batch_near.status == BatchStatus.EXHAUSTED
        assert batch_far.quantity == 15

    def test_reduce_insufficient_stock(self, db, user, medicine, inventory_batch):
        with pytest.raises(ValueError, match='Insufficient stock'):
            InventoryService.reduce_for_sale(
                medicine_id=str(medicine.id),
                quantity=1000,
                sale_id='SALE-FAIL',
                created_by=user,
            )

    def test_exhausted_batch_status(self, db, user, medicine, inventory_batch):
        InventoryService.reduce_for_sale(
            medicine_id=str(medicine.id),
            quantity=50,   # exact quantity
            sale_id='SALE-EXHAUST',
            created_by=user,
        )
        inventory_batch.refresh_from_db()
        assert inventory_batch.quantity == 0
        assert inventory_batch.status == BatchStatus.EXHAUSTED


# ─────────────────────────────────────────────
# Manual Adjustment Tests
# ─────────────────────────────────────────────

class TestAdjustStock:

    def test_adjust_up(self, db, user, inventory_batch):
        updated = InventoryService.adjust_stock(
            batch=inventory_batch,
            new_quantity=80,
            reason='Physical count showed more',
            adjustment_reason_code='physical_count',
            adjusted_by=user,
        )
        assert updated.quantity == 80

        ledger = InventoryLedger.objects.filter(
            inventory_batch=inventory_batch,
            movement_type=LedgerMovementType.ADJUSTMENT,
        ).first()
        assert ledger.quantity == 30   # 80 - 50
        assert ledger.quantity_before == 50
        assert ledger.quantity_after == 80

    def test_adjust_down(self, db, user, inventory_batch):
        updated = InventoryService.adjust_stock(
            batch=inventory_batch,
            new_quantity=20,
            reason='Damaged items found',
            adjustment_reason_code='damage',
            adjusted_by=user,
        )
        assert updated.quantity == 20

    def test_adjust_to_zero_marks_exhausted(self, db, user, inventory_batch):
        updated = InventoryService.adjust_stock(
            batch=inventory_batch,
            new_quantity=0,
            reason='All damaged',
            adjustment_reason_code='damage',
            adjusted_by=user,
        )
        assert updated.status == BatchStatus.EXHAUSTED

    def test_adjust_requires_reason(self, db, user, inventory_batch):
        with pytest.raises(ValueError, match='reason'):
            InventoryService.adjust_stock(
                batch=inventory_batch,
                new_quantity=40,
                reason='',
                adjustment_reason_code='damage',
                adjusted_by=user,
            )

    def test_adjust_negative_rejected(self, db, user, inventory_batch):
        with pytest.raises(ValueError):
            InventoryService.adjust_stock(
                batch=inventory_batch,
                new_quantity=-5,
                reason='Test',
                adjustment_reason_code='damage',
                adjusted_by=user,
            )


# ─────────────────────────────────────────────
# Adjustment API Tests
# ─────────────────────────────────────────────

class TestAdjustmentAPI:

    def test_adjust_via_api(self, auth_client, inventory_batch):
        response = auth_client.post('/api/v1/inventory/adjust/', {
            'batch_id': str(inventory_batch.id),
            'new_quantity': 30,
            'reason': 'Physical count',
            'adjustment_reason_code': 'physical_count',
        }, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['quantity'] == 30

    def test_adjust_missing_reason(self, auth_client, inventory_batch):
        response = auth_client.post('/api/v1/inventory/adjust/', {
            'batch_id': str(inventory_batch.id),
            'new_quantity': 30,
            'reason': '',
            'adjustment_reason_code': 'damage',
        }, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ─────────────────────────────────────────────
# Mark Expired Tests
# ─────────────────────────────────────────────

class TestMarkExpired:

    def test_mark_expired_success(self, db, user, inventory_batch):
        updated = InventoryService.mark_expired(batch=inventory_batch, marked_by=user)

        assert updated.quantity == 0
        assert updated.expired_quantity == 50
        assert updated.status == BatchStatus.EXPIRED

        ledger = InventoryLedger.objects.filter(
            inventory_batch=inventory_batch,
            movement_type=LedgerMovementType.EXPIRY,
        ).first()
        assert ledger is not None
        assert ledger.quantity == -50

    def test_mark_expired_via_api(self, auth_client, inventory_batch):
        response = auth_client.post(
            f'/api/v1/inventory/batches/{inventory_batch.id}/mark-expired/'
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['status'] == 'expired'

    def test_mark_expired_empty_batch(self, db, user, medicine):
        empty_batch = InventoryBatch.objects.create(
            medicine=medicine, batch_number='EMPTY',
            expiry_date=date.today() + timedelta(days=10),
            purchase_price=10, mrp=15, quantity=0,
            status=BatchStatus.EXHAUSTED,
        )
        with pytest.raises(ValueError, match='no available quantity'):
            InventoryService.mark_expired(batch=empty_batch, marked_by=user)


# ─────────────────────────────────────────────
# Stock Summary API Tests
# ─────────────────────────────────────────────

class TestMedicineStockAPI:

    def test_stock_summary(self, auth_client, medicine, inventory_batch):
        response = auth_client.get(f'/api/v1/inventory/stock/{medicine.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['total_available'] == 50
        assert len(response.data['data']['batches']) == 1

    def test_ledger_list(self, auth_client, db, user, medicine, inventory_batch):
        # Create a ledger entry
        InventoryService.adjust_stock(
            batch=inventory_batch, new_quantity=40,
            reason='Test', adjustment_reason_code='physical_count',
            adjusted_by=user,
        )

        response = auth_client.get('/api/v1/inventory/ledger/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1
