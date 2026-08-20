"""
Seed test data for MSMS development.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from decimal import Decimal
from datetime import date, timedelta

from apps.medicine.models import Medicine
from apps.supplier.models import Supplier
from apps.purchase.services.purchase_service import PurchaseService
from apps.billing.services.billing_service import BillingSessionService
from apps.billing.selectors.billing_selector import BillingSessionSelector
from apps.sales.services.sales_service import SalesService


class Command(BaseCommand):
    help = 'Seed test data for development'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding test data...')
        admin = User.objects.get(username='admin')

        with transaction.atomic():
            suppliers = self._create_suppliers(admin)
            medicines = self._create_medicines(admin)
            self._create_purchases(admin, suppliers, medicines)
            self._create_sales(admin, medicines)

        self.stdout.write(self.style.SUCCESS('✅ Test data seeded successfully!'))

    def _create_suppliers(self, admin):
        data = [
            {'name': 'MedLife Distributors', 'contact_person': 'Rajesh Kumar', 'mobile': '9876543210', 'email': 'rajesh@medlife.com', 'city': 'Mumbai', 'state': 'Maharashtra', 'address': 'Shop 12, Medical Complex, Mumbai', 'gst_number': '27AABCM1234A1Z5'},
            {'name': 'PharmaCo Pvt Ltd',     'contact_person': 'Sneha Joshi',  'mobile': '8765432109', 'email': 'sneha@pharmaco.in',  'city': 'Pune',   'state': 'Maharashtra', 'address': 'Plot 45, Pharma Zone, Pune',    'gst_number': '27AABCP5678B2Z6'},
            {'name': 'GenMed Supplies',       'contact_person': 'Ajay Sharma',  'mobile': '7654321098', 'email': 'ajay@genmed.co',     'city': 'Delhi',  'state': 'Delhi',        'address': 'Block C, Medicine Market, Delhi', 'gst_number': '07AABCG9012C3Z7'},
            {'name': 'Cipla Wholesale',       'contact_person': 'Neha Patil',   'mobile': '6543210987', 'email': 'neha@cipla.com',     'city': 'Mumbai', 'state': 'Maharashtra', 'address': 'Cipla House, Andheri, Mumbai',  'gst_number': '27AABCC3456D4Z8'},
            {'name': 'Sun Pharma Depot',      'contact_person': 'Vikram Singh', 'mobile': '9988776655', 'email': 'vikram@sunpharma.in','city': 'Vadodara','state': 'Gujarat',     'address': 'Sun House, Vadodara',           'gst_number': '24AABCS7890E5Z9'},
        ]
        suppliers = []
        for s in data:
            obj, created = Supplier.objects.get_or_create(mobile=s['mobile'], defaults={**s, 'created_by': admin})
            suppliers.append(obj)
            if created:
                self.stdout.write(f'  Supplier: {obj.name}')
        return suppliers

    def _create_medicines(self, admin):
        from apps.medicine.models import Medicine
        data = [
            {'name': 'Paracetamol 500mg',    'generic_name': 'Paracetamol',      'manufacturer': 'Cipla',       'barcode': 'BAR001', 'strength': '500mg',  'category': 'Analgesic',        'hsn_code': '30049099', 'gst_percentage': Decimal('12.00')},
            {'name': 'Amoxicillin 250mg',     'generic_name': 'Amoxicillin',      'manufacturer': 'Sun Pharma',  'barcode': 'BAR002', 'strength': '250mg',  'category': 'Antibiotic',       'hsn_code': '30041000', 'gst_percentage': Decimal('12.00')},
            {'name': 'Metformin 500mg',       'generic_name': 'Metformin',        'manufacturer': 'Dr. Reddys',  'barcode': 'BAR003', 'strength': '500mg',  'category': 'Antidiabetic',     'hsn_code': '30049099', 'gst_percentage': Decimal('12.00')},
            {'name': 'Atorvastatin 10mg',     'generic_name': 'Atorvastatin',     'manufacturer': 'Torrent',     'barcode': 'BAR004', 'strength': '10mg',   'category': 'Statin',           'hsn_code': '30049099', 'gst_percentage': Decimal('12.00')},
            {'name': 'Omeprazole 20mg',       'generic_name': 'Omeprazole',       'manufacturer': 'Zydus',       'barcode': 'BAR005', 'strength': '20mg',   'category': 'Antacid',          'hsn_code': '30049099', 'gst_percentage': Decimal('12.00')},
            {'name': 'Cetirizine 10mg',       'generic_name': 'Cetirizine',       'manufacturer': 'Cipla',       'barcode': 'BAR006', 'strength': '10mg',   'category': 'Antihistamine',    'hsn_code': '30049099', 'gst_percentage': Decimal('12.00')},
            {'name': 'Azithromycin 500mg',    'generic_name': 'Azithromycin',     'manufacturer': 'Lupin',       'barcode': 'BAR007', 'strength': '500mg',  'category': 'Antibiotic',       'hsn_code': '30041000', 'gst_percentage': Decimal('12.00')},
            {'name': 'Aspirin 75mg',          'generic_name': 'Aspirin',          'manufacturer': 'Bayer',       'barcode': 'BAR008', 'strength': '75mg',   'category': 'Antiplatelet',     'hsn_code': '30049099', 'gst_percentage': Decimal('12.00')},
            {'name': 'Pantoprazole 40mg',     'generic_name': 'Pantoprazole',     'manufacturer': 'Abbott',      'barcode': 'BAR009', 'strength': '40mg',   'category': 'Antacid',          'hsn_code': '30049099', 'gst_percentage': Decimal('12.00')},
            {'name': 'Amlodipine 5mg',        'generic_name': 'Amlodipine',       'manufacturer': 'Cipla',       'barcode': 'BAR010', 'strength': '5mg',    'category': 'Antihypertensive', 'hsn_code': '30049099', 'gst_percentage': Decimal('12.00')},
            {'name': 'Dolo 650mg',            'generic_name': 'Paracetamol',      'manufacturer': 'Micro Labs',  'barcode': 'BAR011', 'strength': '650mg',  'category': 'Analgesic',        'hsn_code': '30049099', 'gst_percentage': Decimal('12.00')},
            {'name': 'Vitamin D3 60000IU',    'generic_name': 'Cholecalciferol',  'manufacturer': 'Sun Pharma',  'barcode': 'BAR012', 'strength': '60000IU','category': 'Vitamin',          'hsn_code': '30049099', 'gst_percentage': Decimal('12.00')},
            {'name': 'Montair LC',            'generic_name': 'Montelukast',      'manufacturer': 'Cipla',       'barcode': 'BAR013', 'strength': '10mg',   'category': 'Antiasthmatic',    'hsn_code': '30049099', 'gst_percentage': Decimal('12.00')},
            {'name': 'Calpol 250mg Syrup',    'generic_name': 'Paracetamol',      'manufacturer': 'GSK',         'barcode': 'BAR014', 'strength': '250mg',  'category': 'Analgesic',        'hsn_code': '30049099', 'gst_percentage': Decimal('12.00')},
            {'name': 'ORS Sachet',            'generic_name': 'Oral Rehydration', 'manufacturer': 'Electral',    'barcode': 'BAR015', 'strength': '21.8g',  'category': 'Electrolyte',      'hsn_code': '30049099', 'gst_percentage': Decimal('5.00')},
        ]
        medicines = []
        for m in data:
            obj, created = Medicine.objects.get_or_create(barcode=m['barcode'], defaults={**m, 'created_by': admin})
            medicines.append(obj)
            if created:
                self.stdout.write(f'  Medicine: {obj.name}')
        return medicines

    def _create_purchases(self, admin, suppliers, medicines):
        mrp_map = {
            'BAR001': Decimal('28'), 'BAR002': Decimal('85'),  'BAR003': Decimal('42'),
            'BAR004': Decimal('120'),'BAR005': Decimal('65'),  'BAR006': Decimal('18'),
            'BAR007': Decimal('150'),'BAR008': Decimal('22'),  'BAR009': Decimal('95'),
            'BAR010': Decimal('55'), 'BAR011': Decimal('32'),  'BAR012': Decimal('180'),
            'BAR013': Decimal('135'),'BAR014': Decimal('48'),  'BAR015': Decimal('12'),
        }
        purchase_groups = [
            {'supplier': suppliers[0], 'inv': 'INV-SUP-1001', 'days_ago': 20, 'items': [(medicines[0], 200, 18), (medicines[1], 50, 55), (medicines[2], 80, 28)]},
            {'supplier': suppliers[1], 'inv': 'INV-SUP-1002', 'days_ago': 15, 'items': [(medicines[3], 60, 75), (medicines[4], 100, 40), (medicines[5], 150, 10)]},
            {'supplier': suppliers[2], 'inv': 'INV-SUP-1003', 'days_ago': 10, 'items': [(medicines[6], 40, 95), (medicines[7], 120, 14), (medicines[8], 80, 60)]},
            {'supplier': suppliers[3], 'inv': 'INV-SUP-1004', 'days_ago': 7,  'items': [(medicines[9], 90, 35), (medicines[10], 200, 20), (medicines[11], 30, 110)]},
            {'supplier': suppliers[4], 'inv': 'INV-SUP-1005', 'days_ago': 3,  'items': [(medicines[12], 50, 85), (medicines[13], 70, 30), (medicines[14], 300, 7)]},
        ]
        for i, pg in enumerate(purchase_groups):
            inv_date = date.today() - timedelta(days=pg['days_ago'])
            purchase_data = {
                'supplier_id': str(pg['supplier'].id),
                'invoice_number': pg['inv'],
                'invoice_date': inv_date,
                'items': [
                    {
                        'medicine_id': str(med.id),
                        'quantity': qty,
                        'purchase_price': Decimal(str(price)),
                        'batch_number': f'BATCH-2024-{i+1:02d}-{med.barcode}',
                        'expiry_date': date.today() + timedelta(days=365 + i * 60),
                        'mrp': mrp_map.get(med.barcode, Decimal('50')),
                        'gst_percentage': med.gst_percentage,
                        'discount_percentage': Decimal('0'),
                    }
                    for med, qty, price in pg['items']
                ]
            }
            try:
                purchase = PurchaseService.create_purchase(data=purchase_data, created_by=admin)
                PurchaseService.finalize_purchase(purchase=purchase, finalized_by=admin)
                self.stdout.write(f'  Purchase {pg["inv"]} finalized')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  Purchase {pg["inv"]} skipped: {e}'))

    def _create_sales(self, admin, medicines):
        sale_scenarios = [
            {'items': [(medicines[0], 2), (medicines[4], 1)],                     'payment': 'cash'},
            {'items': [(medicines[1], 1), (medicines[6], 1)],                     'payment': 'upi'},
            {'items': [(medicines[2], 3), (medicines[9], 1)],                     'payment': 'card'},
            {'items': [(medicines[5], 2), (medicines[10], 1), (medicines[14], 5)],'payment': 'cash'},
            {'items': [(medicines[3], 1), (medicines[8], 2)],                     'payment': 'upi'},
            {'items': [(medicines[11], 1), (medicines[12], 1)],                   'payment': 'cash'},
            {'items': [(medicines[0], 4), (medicines[4], 2), (medicines[7], 1)],  'payment': 'card'},
            {'items': [(medicines[13], 2), (medicines[5], 1)],                    'payment': 'upi'},
            {'items': [(medicines[1], 2), (medicines[0], 3)],                     'payment': 'cash'},
            {'items': [(medicines[6], 1), (medicines[8], 1), (medicines[9], 2)],  'payment': 'card'},
        ]
        for i, scenario in enumerate(sale_scenarios):
            try:
                session = BillingSessionService.create_session(created_by=admin)
                for med, qty in scenario['items']:
                    BillingSessionService.add_item(
                        session=session,
                        medicine_id=str(med.id),
                        quantity=qty,
                        discount_percentage=0,
                    )
                session = BillingSessionSelector.get_by_id(str(session.id))
                sale = SalesService.checkout(
                    session=session,
                    payment_mode=scenario['payment'],
                    remarks='Test sale',
                    created_by=admin,
                )
                self.stdout.write(f'  Sale: {sale.invoice_number}')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  Sale {i+1} skipped: {e}'))
