"""
Supplier Views.
Thin views — validate input, call service, return response.
No business logic here.
"""

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

from common.responses.responses import (
    success_response, created_response, error_response, no_content_response
)
from common.pagination.pagination import StandardPagination

from .serializers import (
    SupplierCreateSerializer,
    SupplierUpdateSerializer,
    SupplierListSerializer,
    SupplierDetailSerializer,
)
from .services.supplier_service import SupplierService
from .selectors.supplier_selector import SupplierSelector
from .filters import SupplierFilter

logger = logging.getLogger('apps.supplier')


class SupplierListCreateView(APIView):
    """
    GET  /api/v1/suppliers/  — List all suppliers (paginated, filterable)
    POST /api/v1/suppliers/  — Create new supplier
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='List Suppliers',
        description='Returns paginated list of suppliers. Supports search and filtering.',
        parameters=[
            OpenApiParameter('search', str, description='Search by name, mobile, GST, contact person'),
            OpenApiParameter('status', str, description='Filter by status: active, inactive'),
            OpenApiParameter('city', str, description='Filter by city'),
            OpenApiParameter('page', int, description='Page number'),
            OpenApiParameter('page_size', int, description='Items per page (max 100)'),
        ],
        tags=['Supplier'],
    )
    def get(self, request):
        queryset = SupplierSelector.get_all()

        # Apply filters
        filterset = SupplierFilter(request.GET, queryset=queryset)
        queryset = filterset.qs

        # Apply search
        search = request.GET.get('search', '').strip()
        if search:
            queryset = SupplierSelector.search(search)

        # Apply ordering
        ordering = request.GET.get('ordering', 'name')
        allowed_orderings = ['name', '-name', 'created_at', '-created_at', 'city', 'status']
        if ordering in allowed_orderings:
            queryset = queryset.order_by(ordering)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = SupplierListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        request=SupplierCreateSerializer,
        responses={
            201: SupplierDetailSerializer,
            400: OpenApiResponse(description='Validation error'),
            409: OpenApiResponse(description='GST number already exists'),
        },
        summary='Create Supplier',
        description='Register a new supplier. GST number must be unique if provided.',
        tags=['Supplier'],
    )
    def post(self, request):
        serializer = SupplierCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message='Validation failed.',
                errors=serializer.errors,
                status_code=400,
            )

        try:
            supplier = SupplierService.create_supplier(
                data=serializer.validated_data,
                created_by=request.user,
            )
            return created_response(
                data=SupplierDetailSerializer(supplier).data,
                message='Supplier created successfully.',
            )
        except ValueError as exc:
            return error_response(message=str(exc), status_code=409)


class SupplierDetailView(APIView):
    """
    GET    /api/v1/suppliers/{id}/  — Retrieve supplier
    PUT    /api/v1/suppliers/{id}/  — Full update
    PATCH  /api/v1/suppliers/{id}/  — Partial update
    DELETE /api/v1/suppliers/{id}/  — Soft delete (deactivate)
    """
    permission_classes = [IsAuthenticated]

    def _get_supplier(self, supplier_id):
        return SupplierSelector.get_by_id(supplier_id)

    @extend_schema(
        summary='Get Supplier',
        responses={200: SupplierDetailSerializer, 404: OpenApiResponse(description='Not found')},
        tags=['Supplier'],
    )
    def get(self, request, pk):
        supplier = self._get_supplier(pk)
        if not supplier:
            return error_response(message='Supplier not found.', status_code=404)

        return success_response(
            data=SupplierDetailSerializer(supplier).data,
            message='Supplier fetched successfully.',
        )

    @extend_schema(
        request=SupplierUpdateSerializer,
        summary='Update Supplier (Full)',
        responses={200: SupplierDetailSerializer},
        tags=['Supplier'],
    )
    def put(self, request, pk):
        return self._update(request, pk, partial=False)

    @extend_schema(
        request=SupplierUpdateSerializer,
        summary='Update Supplier (Partial)',
        responses={200: SupplierDetailSerializer},
        tags=['Supplier'],
    )
    def patch(self, request, pk):
        return self._update(request, pk, partial=True)

    def _update(self, request, pk, partial):
        supplier = self._get_supplier(pk)
        if not supplier:
            return error_response(message='Supplier not found.', status_code=404)

        serializer = SupplierUpdateSerializer(
            supplier, data=request.data, partial=partial
        )
        if not serializer.is_valid():
            return error_response(
                message='Validation failed.',
                errors=serializer.errors,
                status_code=400,
            )

        try:
            updated = SupplierService.update_supplier(
                supplier=supplier,
                data=serializer.validated_data,
                updated_by=request.user,
            )
            return success_response(
                data=SupplierDetailSerializer(updated).data,
                message='Supplier updated successfully.',
            )
        except ValueError as exc:
            return error_response(message=str(exc), status_code=422)

    @extend_schema(
        summary='Deactivate Supplier (Soft Delete)',
        responses={
            204: OpenApiResponse(description='Supplier deactivated'),
            404: OpenApiResponse(description='Not found'),
        },
        tags=['Supplier'],
    )
    def delete(self, request, pk):
        supplier = self._get_supplier(pk)
        if not supplier:
            return error_response(message='Supplier not found.', status_code=404)

        SupplierService.deactivate_supplier(supplier, deactivated_by=request.user)
        return no_content_response()
