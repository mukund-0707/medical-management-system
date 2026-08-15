"""
Purchase Views — thin views only.
"""

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

from common.responses.responses import success_response, created_response, error_response
from common.pagination.pagination import StandardPagination

from .serializers import (
    PurchaseCreateSerializer,
    PurchaseUpdateSerializer,
    PurchaseListSerializer,
    PurchaseDetailSerializer,
)
from .services.purchase_service import PurchaseService
from .selectors.purchase_selector import PurchaseSelector
from .filters import PurchaseFilter

logger = logging.getLogger('apps.purchase')


class PurchaseListCreateView(APIView):
    """
    GET  /api/v1/purchases/  — List purchases
    POST /api/v1/purchases/  — Create draft purchase with items
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='List Purchases',
        parameters=[
            OpenApiParameter('status', str, description='Filter: draft, finalized, cancelled'),
            OpenApiParameter('supplier', str, description='Filter by supplier UUID'),
            OpenApiParameter('search', str, description='Search by invoice number'),
        ],
        tags=['Purchase'],
    )
    def get(self, request):
        queryset = PurchaseSelector.get_all()

        filterset = PurchaseFilter(request.GET, queryset=queryset)
        queryset = filterset.qs

        search = request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(invoice_number__icontains=search)

        ordering = request.GET.get('ordering', '-created_at')
        allowed = ['-created_at', 'created_at', '-invoice_date', 'invoice_date']
        if ordering in allowed:
            queryset = queryset.order_by(ordering)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = PurchaseListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        request=PurchaseCreateSerializer,
        responses={
            201: PurchaseDetailSerializer,
            400: OpenApiResponse(description='Validation error'),
            422: OpenApiResponse(description='Business rule violation'),
        },
        summary='Create Purchase (Draft)',
        description='Creates a purchase in DRAFT status. Inventory is NOT updated yet.',
        tags=['Purchase'],
    )
    def post(self, request):
        serializer = PurchaseCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message='Validation failed.',
                errors=serializer.errors,
                status_code=400,
            )

        try:
            purchase = PurchaseService.create_purchase(
                data=serializer.validated_data,
                created_by=request.user,
            )
            return created_response(
                data=PurchaseDetailSerializer(purchase).data,
                message='Purchase created as draft.',
            )
        except ValueError as exc:
            return error_response(message=str(exc), status_code=422)


class PurchaseDetailView(APIView):
    """
    GET   /api/v1/purchases/{id}/
    PATCH /api/v1/purchases/{id}/  — Update draft only
    """
    permission_classes = [IsAuthenticated]

    def _get_purchase(self, pk):
        return PurchaseSelector.get_by_id(pk)

    @extend_schema(
        summary='Get Purchase',
        responses={200: PurchaseDetailSerializer, 404: OpenApiResponse(description='Not found')},
        tags=['Purchase'],
    )
    def get(self, request, pk):
        purchase = self._get_purchase(pk)
        if not purchase:
            return error_response(message='Purchase not found.', status_code=404)

        return success_response(
            data=PurchaseDetailSerializer(purchase).data,
            message='Purchase fetched successfully.',
        )

    @extend_schema(
        request=PurchaseUpdateSerializer,
        summary='Update Purchase (Draft only)',
        responses={200: PurchaseDetailSerializer},
        tags=['Purchase'],
    )
    def patch(self, request, pk):
        purchase = self._get_purchase(pk)
        if not purchase:
            return error_response(message='Purchase not found.', status_code=404)

        serializer = PurchaseUpdateSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(
                message='Validation failed.',
                errors=serializer.errors,
                status_code=400,
            )

        try:
            updated = PurchaseService.update_purchase(
                purchase=purchase,
                data=serializer.validated_data,
                updated_by=request.user,
            )
            return success_response(
                data=PurchaseDetailSerializer(updated).data,
                message='Purchase updated successfully.',
            )
        except ValueError as exc:
            return error_response(message=str(exc), status_code=422)


class PurchaseFinalizeView(APIView):
    """
    POST /api/v1/purchases/{id}/finalize/
    Finalize a draft purchase → creates inventory batches + ledger entries.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Finalize Purchase',
        description='Converts DRAFT to FINALIZED. Creates inventory batches and stock ledger entries.',
        responses={
            200: PurchaseDetailSerializer,
            422: OpenApiResponse(description='Cannot finalize'),
        },
        tags=['Purchase'],
    )
    def post(self, request, pk):
        purchase = PurchaseSelector.get_by_id(pk)
        if not purchase:
            return error_response(message='Purchase not found.', status_code=404)

        try:
            finalized = PurchaseService.finalize_purchase(
                purchase=purchase,
                finalized_by=request.user,
            )
            return success_response(
                data=PurchaseDetailSerializer(finalized).data,
                message='Purchase finalized. Inventory updated.',
            )
        except ValueError as exc:
            return error_response(message=str(exc), status_code=422)


class PurchaseCancelView(APIView):
    """
    POST /api/v1/purchases/{id}/cancel/
    Cancel a purchase. Reverses inventory if finalized (and no sales consumed it).
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Cancel Purchase',
        description='Cancel a purchase. Finalized purchases can only be cancelled if no stock has been sold.',
        responses={
            200: PurchaseDetailSerializer,
            422: OpenApiResponse(description='Cannot cancel'),
        },
        tags=['Purchase'],
    )
    def post(self, request, pk):
        purchase = PurchaseSelector.get_by_id(pk)
        if not purchase:
            return error_response(message='Purchase not found.', status_code=404)

        try:
            cancelled = PurchaseService.cancel_purchase(
                purchase=purchase,
                cancelled_by=request.user,
            )
            return success_response(
                data=PurchaseDetailSerializer(cancelled).data,
                message='Purchase cancelled successfully.',
            )
        except ValueError as exc:
            return error_response(message=str(exc), status_code=422)
