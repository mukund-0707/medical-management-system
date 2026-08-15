"""
Inventory Views — thin views only.
"""

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

from common.responses.responses import success_response, error_response
from common.pagination.pagination import StandardPagination

from .models import InventoryBatch
from .serializers import InventoryBatchSerializer, InventoryLedgerSerializer, AdjustmentSerializer
from .services.inventory_service import InventoryService
from .selectors.inventory_selector import InventorySelector
from .filters import InventoryBatchFilter, InventoryLedgerFilter

logger = logging.getLogger('apps.inventory')


class InventoryBatchListView(APIView):
    """
    GET /api/v1/inventory/batches/
    List all inventory batches. Supports filter by status, medicine, expiry, low_stock.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='List Inventory Batches',
        parameters=[
            OpenApiParameter('status', str, description='available, expired, damaged, exhausted'),
            OpenApiParameter('medicine', str, description='Medicine UUID'),
            OpenApiParameter('low_stock', bool, description='True = show only low stock'),
            OpenApiParameter('expiry_before', str, description='YYYY-MM-DD'),
        ],
        tags=['Inventory'],
    )
    def get(self, request):
        queryset = InventorySelector.get_all_batches()

        filterset = InventoryBatchFilter(request.GET, queryset=queryset)
        queryset = filterset.qs

        ordering = request.GET.get('ordering', 'expiry_date')
        allowed = ['expiry_date', '-expiry_date', 'quantity', '-quantity', '-created_at']
        if ordering in allowed:
            queryset = queryset.order_by(ordering)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = InventoryBatchSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class InventoryBatchDetailView(APIView):
    """
    GET /api/v1/inventory/batches/{id}/
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Get Inventory Batch',
        responses={200: InventoryBatchSerializer, 404: OpenApiResponse(description='Not found')},
        tags=['Inventory'],
    )
    def get(self, request, pk):
        batch = InventorySelector.get_batch_by_id(pk)
        if not batch:
            return error_response(message='Inventory batch not found.', status_code=404)

        return success_response(
            data=InventoryBatchSerializer(batch).data,
            message='Batch fetched successfully.',
        )


class InventoryAdjustView(APIView):
    """
    POST /api/v1/inventory/adjust/
    Manual stock adjustment — always creates a ledger entry.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AdjustmentSerializer,
        responses={
            200: InventoryBatchSerializer,
            400: OpenApiResponse(description='Validation error'),
            404: OpenApiResponse(description='Batch not found'),
            422: OpenApiResponse(description='Business rule error'),
        },
        summary='Adjust Stock',
        description='Manually adjust stock for a batch. Reason is mandatory. Always creates ledger entry.',
        tags=['Inventory'],
    )
    def post(self, request):
        serializer = AdjustmentSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message='Validation failed.',
                errors=serializer.errors,
                status_code=400,
            )

        batch = InventorySelector.get_batch_by_id(
            str(serializer.validated_data['batch_id'])
        )
        if not batch:
            return error_response(message='Inventory batch not found.', status_code=404)

        try:
            updated_batch = InventoryService.adjust_stock(
                batch=batch,
                new_quantity=serializer.validated_data['new_quantity'],
                reason=serializer.validated_data['reason'],
                adjustment_reason_code=serializer.validated_data['adjustment_reason_code'],
                adjusted_by=request.user,
            )
            return success_response(
                data=InventoryBatchSerializer(updated_batch).data,
                message='Stock adjusted successfully.',
            )
        except ValueError as exc:
            return error_response(message=str(exc), status_code=422)


class InventoryMarkExpiredView(APIView):
    """
    POST /api/v1/inventory/batches/{id}/mark-expired/
    Mark a batch as expired — moves quantity to expired_quantity.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Mark Batch Expired',
        responses={
            200: InventoryBatchSerializer,
            422: OpenApiResponse(description='No quantity to expire'),
        },
        tags=['Inventory'],
    )
    def post(self, request, pk):
        batch = InventorySelector.get_batch_by_id(pk)
        if not batch:
            return error_response(message='Inventory batch not found.', status_code=404)

        try:
            updated = InventoryService.mark_expired(batch=batch, marked_by=request.user)
            return success_response(
                data=InventoryBatchSerializer(updated).data,
                message='Batch marked as expired.',
            )
        except ValueError as exc:
            return error_response(message=str(exc), status_code=422)


class InventoryLedgerListView(APIView):
    """
    GET /api/v1/inventory/ledger/
    View stock movement history. Filterable by medicine, movement_type, date.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Stock Ledger',
        description='Complete stock movement history. Immutable — read-only.',
        parameters=[
            OpenApiParameter('medicine', str, description='Medicine UUID'),
            OpenApiParameter('movement_type', str, description='purchase, sale, adjustment...'),
            OpenApiParameter('date_from', str, description='YYYY-MM-DD'),
            OpenApiParameter('date_to', str, description='YYYY-MM-DD'),
        ],
        tags=['Inventory'],
    )
    def get(self, request):
        queryset = InventorySelector.get_all_ledger()

        filterset = InventoryLedgerFilter(request.GET, queryset=queryset)
        queryset = filterset.qs

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = InventoryLedgerSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class MedicineStockView(APIView):
    """
    GET /api/v1/inventory/stock/{medicine_id}/
    Current stock summary for a specific medicine.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Medicine Stock Summary',
        description='Returns all batches and total available quantity for a medicine.',
        tags=['Inventory'],
    )
    def get(self, request, medicine_id):
        batches = InventorySelector.get_batches_for_medicine(str(medicine_id))
        total = InventorySelector.get_total_available_quantity(str(medicine_id))

        return success_response(
            data={
                'medicine_id': str(medicine_id),
                'total_available': total,
                'batches': InventoryBatchSerializer(batches, many=True).data,
            },
            message='Stock summary fetched.',
        )
