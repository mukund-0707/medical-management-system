"""
Reports Views — thin views, all read-only.
Each report is paginated and filterable.
"""

import logging
from datetime import date
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter

from common.responses.responses import success_response
from common.pagination.pagination import StandardPagination

from .services.reports_service import ReportsService

# Reuse serializers from existing modules
from apps.sales.serializers import SaleListSerializer, SaleDetailSerializer
from apps.purchase.serializers import PurchaseListSerializer, PurchaseDetailSerializer
from apps.inventory.serializers import InventoryBatchSerializer, InventoryLedgerSerializer
from apps.medicine.serializers import MedicineListSerializer
from apps.supplier.serializers import SupplierListSerializer

logger = logging.getLogger('apps.reports')


def _parse_date(val: str) -> date | None:
    if not val:
        return None
    try:
        return date.fromisoformat(val)
    except ValueError:
        return None


def _parse_int(val: str, default: int) -> int:
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


class SalesReportView(APIView):
    """GET /api/v1/reports/sales/"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Sales Report',
        parameters=[
            OpenApiParameter('date_from', str, description='YYYY-MM-DD'),
            OpenApiParameter('date_to', str, description='YYYY-MM-DD'),
            OpenApiParameter('payment_mode', str, description='cash, upi, card, bank_transfer'),
            OpenApiParameter('status', str, description='completed, cancelled'),
            OpenApiParameter('search', str, description='Invoice number search'),
        ],
        tags=['Reports'],
    )
    def get(self, request):
        qs = ReportsService.get_sales_report(
            date_from=_parse_date(request.GET.get('date_from')),
            date_to=_parse_date(request.GET.get('date_to')),
            payment_mode=request.GET.get('payment_mode'),
            status=request.GET.get('status'),
            search=request.GET.get('search'),
        )
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(SaleListSerializer(page, many=True).data)


class PurchaseReportView(APIView):
    """GET /api/v1/reports/purchases/"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Purchase Report',
        parameters=[
            OpenApiParameter('date_from', str, description='YYYY-MM-DD'),
            OpenApiParameter('date_to', str, description='YYYY-MM-DD'),
            OpenApiParameter('supplier', str, description='Supplier UUID'),
            OpenApiParameter('status', str, description='draft, finalized, cancelled'),
            OpenApiParameter('search', str, description='Invoice number search'),
        ],
        tags=['Reports'],
    )
    def get(self, request):
        qs = ReportsService.get_purchase_report(
            date_from=_parse_date(request.GET.get('date_from')),
            date_to=_parse_date(request.GET.get('date_to')),
            supplier_id=request.GET.get('supplier'),
            status=request.GET.get('status'),
            search=request.GET.get('search'),
        )
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(PurchaseListSerializer(page, many=True).data)


class InventoryReportView(APIView):
    """GET /api/v1/reports/inventory/"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Inventory Report',
        parameters=[
            OpenApiParameter('medicine', str, description='Medicine UUID'),
            OpenApiParameter('status', str, description='available, expired, damaged, exhausted'),
            OpenApiParameter('batch_number', str, description='Batch number search'),
        ],
        tags=['Reports'],
    )
    def get(self, request):
        qs = ReportsService.get_inventory_report(
            medicine_id=request.GET.get('medicine'),
            status=request.GET.get('status'),
            batch_number=request.GET.get('batch_number'),
        )
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(InventoryBatchSerializer(page, many=True).data)


class LedgerReportView(APIView):
    """GET /api/v1/reports/ledger/"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Stock Ledger Report',
        description='Complete stock movement history. Immutable audit trail.',
        parameters=[
            OpenApiParameter('medicine', str, description='Medicine UUID'),
            OpenApiParameter('movement_type', str, description='purchase, sale, adjustment...'),
            OpenApiParameter('date_from', str, description='YYYY-MM-DD'),
            OpenApiParameter('date_to', str, description='YYYY-MM-DD'),
            OpenApiParameter('batch_number', str, description='Batch number search'),
        ],
        tags=['Reports'],
    )
    def get(self, request):
        qs = ReportsService.get_ledger_report(
            medicine_id=request.GET.get('medicine'),
            movement_type=request.GET.get('movement_type'),
            date_from=_parse_date(request.GET.get('date_from')),
            date_to=_parse_date(request.GET.get('date_to')),
            batch_number=request.GET.get('batch_number'),
        )
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(InventoryLedgerSerializer(page, many=True).data)


class ExpiryReportView(APIView):
    """GET /api/v1/reports/expiry/"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Expiry Report',
        description='Batches expired or expiring soon.',
        parameters=[
            OpenApiParameter('days', int, description='Expiring within N days (default: 90)'),
        ],
        tags=['Reports'],
    )
    def get(self, request):
        days = _parse_int(request.GET.get('days'), default=90)
        qs = ReportsService.get_expiry_report(days=days)
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(InventoryBatchSerializer(page, many=True).data)


class LowStockReportView(APIView):
    """GET /api/v1/reports/low-stock/"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Low Stock Report',
        description='Medicines with quantity at or below threshold.',
        parameters=[
            OpenApiParameter('threshold', int, description='Quantity threshold (default: 10)'),
        ],
        tags=['Reports'],
    )
    def get(self, request):
        threshold = _parse_int(request.GET.get('threshold'), default=None)
        qs = ReportsService.get_low_stock_report(threshold=threshold)
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(InventoryBatchSerializer(page, many=True).data)


class AdjustmentReportView(APIView):
    """GET /api/v1/reports/adjustments/"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Adjustment Report',
        description='All manual stock adjustment history.',
        parameters=[
            OpenApiParameter('medicine', str, description='Medicine UUID'),
            OpenApiParameter('date_from', str, description='YYYY-MM-DD'),
            OpenApiParameter('date_to', str, description='YYYY-MM-DD'),
        ],
        tags=['Reports'],
    )
    def get(self, request):
        qs = ReportsService.get_adjustment_report(
            medicine_id=request.GET.get('medicine'),
            date_from=_parse_date(request.GET.get('date_from')),
            date_to=_parse_date(request.GET.get('date_to')),
        )
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(InventoryLedgerSerializer(page, many=True).data)


class MedicineReportView(APIView):
    """GET /api/v1/reports/medicines/"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Medicine Report',
        parameters=[
            OpenApiParameter('status', str, description='active, inactive, discontinued'),
            OpenApiParameter('search', str, description='Name, barcode, manufacturer search'),
        ],
        tags=['Reports'],
    )
    def get(self, request):
        qs = ReportsService.get_medicine_report(
            status=request.GET.get('status'),
            search=request.GET.get('search'),
        )
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(MedicineListSerializer(page, many=True).data)


class SupplierReportView(APIView):
    """GET /api/v1/reports/suppliers/"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Supplier Report',
        parameters=[
            OpenApiParameter('status', str, description='active, inactive'),
            OpenApiParameter('search', str, description='Name, mobile, GST search'),
        ],
        tags=['Reports'],
    )
    def get(self, request):
        qs = ReportsService.get_supplier_report(
            status=request.GET.get('status'),
            search=request.GET.get('search'),
        )
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(SupplierListSerializer(page, many=True).data)
