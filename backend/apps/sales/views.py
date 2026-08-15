"""
Sales Views — thin views only.
"""

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

from common.responses.responses import success_response, error_response
from common.pagination.pagination import StandardPagination

from .serializers import CheckoutSerializer, SaleListSerializer, SaleDetailSerializer
from .services.sales_service import SalesService
from .selectors.sale_selector import SaleSelector
from .filters import SaleFilter

from apps.billing.selectors.billing_selector import BillingSessionSelector

logger = logging.getLogger('apps.sales')


class CheckoutView(APIView):
    """
    POST /api/v1/sales/checkout/
    Convert an active billing session into a completed sale.
    This is the most critical endpoint — runs inside a full transaction.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=CheckoutSerializer,
        responses={
            200: SaleDetailSerializer,
            400: OpenApiResponse(description='Validation error'),
            404: OpenApiResponse(description='Session not found'),
            422: OpenApiResponse(description='Insufficient stock / inactive medicine'),
        },
        summary='Checkout',
        description=(
            'Converts billing session to sale. '
            'Validates stock, reduces inventory (FEFO), generates invoice number. '
            'Entire operation is atomic — any failure causes full rollback.'
        ),
        tags=['Sales'],
    )
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message='Validation failed.',
                errors=serializer.errors,
                status_code=400,
            )

        session_id = str(serializer.validated_data['session_id'])
        session = BillingSessionSelector.get_by_id(session_id)

        if not session:
            return error_response(message='Billing session not found.', status_code=404)

        try:
            sale = SalesService.checkout(
                session=session,
                payment_mode=serializer.validated_data['payment_mode'],
                remarks=serializer.validated_data.get('remarks', ''),
                created_by=request.user,
            )
            return success_response(
                data=SaleDetailSerializer(sale).data,
                message=f'Sale completed. Invoice: {sale.invoice_number}',
            )
        except ValueError as exc:
            return error_response(message=str(exc), status_code=422)


class SaleListView(APIView):
    """
    GET /api/v1/sales/
    List all sales — paginated, filterable by date, status, payment mode.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='List Sales',
        parameters=[
            OpenApiParameter('status', str, description='completed, cancelled'),
            OpenApiParameter('payment_mode', str, description='cash, upi, card, bank_transfer'),
            OpenApiParameter('date_from', str, description='YYYY-MM-DD'),
            OpenApiParameter('date_to', str, description='YYYY-MM-DD'),
            OpenApiParameter('search', str, description='Search by invoice number'),
        ],
        tags=['Sales'],
    )
    def get(self, request):
        queryset = SaleSelector.get_all()

        filterset = SaleFilter(request.GET, queryset=queryset)
        queryset = filterset.qs

        search = request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(invoice_number__icontains=search)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = SaleListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class SaleDetailView(APIView):
    """
    GET /api/v1/sales/{id}/
    Full sale detail with all items.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Get Sale',
        responses={200: SaleDetailSerializer, 404: OpenApiResponse(description='Not found')},
        tags=['Sales'],
    )
    def get(self, request, pk):
        sale = SaleSelector.get_by_id(pk)
        if not sale:
            return error_response(message='Sale not found.', status_code=404)

        return success_response(
            data=SaleDetailSerializer(sale).data,
            message='Sale fetched successfully.',
        )


class SaleByInvoiceView(APIView):
    """
    GET /api/v1/sales/invoice/{invoice_number}/
    Lookup sale by invoice number — used for reprinting.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Get Sale by Invoice Number',
        responses={200: SaleDetailSerializer, 404: OpenApiResponse(description='Not found')},
        tags=['Sales'],
    )
    def get(self, request, invoice_number):
        sale = SaleSelector.get_by_invoice_number(invoice_number)
        if not sale:
            return error_response(
                message=f"No sale found for invoice '{invoice_number}'.",
                status_code=404,
            )
        return success_response(
            data=SaleDetailSerializer(sale).data,
            message='Sale fetched successfully.',
        )


class SaleCancelView(APIView):
    """
    POST /api/v1/sales/{id}/cancel/
    Cancel a completed sale. Does not reverse inventory in POC.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Cancel Sale',
        responses={
            200: SaleDetailSerializer,
            422: OpenApiResponse(description='Already cancelled'),
        },
        tags=['Sales'],
    )
    def post(self, request, pk):
        sale = SaleSelector.get_by_id(pk)
        if not sale:
            return error_response(message='Sale not found.', status_code=404)

        try:
            cancelled = SalesService.cancel_sale(sale=sale, cancelled_by=request.user)
            return success_response(
                data=SaleDetailSerializer(cancelled).data,
                message='Sale cancelled.',
            )
        except ValueError as exc:
            return error_response(message=str(exc), status_code=422)
