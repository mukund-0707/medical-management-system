"""
Medicine Views.
Thin views — validate input, call service, return response.
No business logic here.
"""

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

from common.responses.responses import success_response, created_response, error_response, no_content_response
from common.pagination.pagination import StandardPagination

from .models import Medicine
from .serializers import (
    MedicineCreateSerializer,
    MedicineUpdateSerializer,
    MedicineListSerializer,
    MedicineDetailSerializer,
)
from .services.medicine_service import MedicineService
from .selectors.medicine_selector import MedicineSelector
from .filters import MedicineFilter

logger = logging.getLogger('apps.medicine')


class MedicineListCreateView(APIView):
    """
    GET  /api/v1/medicines/  — List all medicines (paginated, filterable)
    POST /api/v1/medicines/  — Create new medicine
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='List Medicines',
        description='Returns paginated list of medicines. Supports search, filter, ordering.',
        parameters=[
            OpenApiParameter('search', str, description='Search by name, generic name, barcode, manufacturer'),
            OpenApiParameter('status', str, description='Filter by status: active, inactive, discontinued'),
            OpenApiParameter('category', str, description='Filter by category'),
            OpenApiParameter('page', int, description='Page number'),
            OpenApiParameter('page_size', int, description='Items per page (max 100)'),
        ],
        tags=['Medicine'],
    )
    def get(self, request):
        queryset = MedicineSelector.get_all()

        # Apply filters
        filterset = MedicineFilter(request.GET, queryset=queryset)
        queryset = filterset.qs

        # Apply search
        search = request.GET.get('search', '').strip()
        if search:
            queryset = MedicineSelector.search(search)

        # Apply ordering
        ordering = request.GET.get('ordering', 'name')
        allowed_orderings = ['name', '-name', 'created_at', '-created_at', 'manufacturer', 'status']
        if ordering in allowed_orderings:
            queryset = queryset.order_by(ordering)

        # Paginate
        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = MedicineListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        request=MedicineCreateSerializer,
        responses={
            201: MedicineDetailSerializer,
            400: OpenApiResponse(description='Validation error'),
            409: OpenApiResponse(description='Barcode already exists'),
        },
        summary='Create Medicine',
        description='Create a new medicine. Barcode must be unique. Does NOT create inventory.',
        tags=['Medicine'],
    )
    def post(self, request):
        serializer = MedicineCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message='Validation failed.',
                errors=serializer.errors,
                status_code=400,
            )

        try:
            medicine = MedicineService.create_medicine(
                data=serializer.validated_data,
                created_by=request.user,
            )
            return created_response(
                data=MedicineDetailSerializer(medicine).data,
                message='Medicine created successfully.',
            )
        except ValueError as exc:
            return error_response(message=str(exc), status_code=409)


class MedicineDetailView(APIView):
    """
    GET    /api/v1/medicines/{id}/  — Retrieve medicine
    PUT    /api/v1/medicines/{id}/  — Full update
    PATCH  /api/v1/medicines/{id}/  — Partial update
    DELETE /api/v1/medicines/{id}/  — Soft delete (deactivate)
    """
    permission_classes = [IsAuthenticated]

    def _get_medicine(self, medicine_id):
        medicine = MedicineSelector.get_by_id(medicine_id)
        if not medicine:
            return None
        return medicine

    @extend_schema(
        summary='Get Medicine',
        responses={200: MedicineDetailSerializer, 404: OpenApiResponse(description='Not found')},
        tags=['Medicine'],
    )
    def get(self, request, pk):
        medicine = self._get_medicine(pk)
        if not medicine:
            return error_response(message='Medicine not found.', status_code=404)

        return success_response(
            data=MedicineDetailSerializer(medicine).data,
            message='Medicine fetched successfully.',
        )

    @extend_schema(
        request=MedicineUpdateSerializer,
        summary='Update Medicine (Full)',
        responses={200: MedicineDetailSerializer, 400: OpenApiResponse(description='Validation error')},
        tags=['Medicine'],
    )
    def put(self, request, pk):
        return self._update(request, pk, partial=False)

    @extend_schema(
        request=MedicineUpdateSerializer,
        summary='Update Medicine (Partial)',
        responses={200: MedicineDetailSerializer, 400: OpenApiResponse(description='Validation error')},
        tags=['Medicine'],
    )
    def patch(self, request, pk):
        return self._update(request, pk, partial=True)

    def _update(self, request, pk, partial):
        medicine = self._get_medicine(pk)
        if not medicine:
            return error_response(message='Medicine not found.', status_code=404)

        serializer = MedicineUpdateSerializer(
            medicine, data=request.data, partial=partial
        )
        if not serializer.is_valid():
            return error_response(
                message='Validation failed.',
                errors=serializer.errors,
                status_code=400,
            )

        try:
            updated = MedicineService.update_medicine(
                medicine=medicine,
                data=serializer.validated_data,
                updated_by=request.user,
            )
            return success_response(
                data=MedicineDetailSerializer(updated).data,
                message='Medicine updated successfully.',
            )
        except ValueError as exc:
            return error_response(message=str(exc), status_code=422)

    @extend_schema(
        summary='Deactivate Medicine (Soft Delete)',
        responses={
            204: OpenApiResponse(description='Medicine deactivated'),
            404: OpenApiResponse(description='Not found'),
        },
        tags=['Medicine'],
    )
    def delete(self, request, pk):
        medicine = self._get_medicine(pk)
        if not medicine:
            return error_response(message='Medicine not found.', status_code=404)

        MedicineService.deactivate_medicine(medicine, deactivated_by=request.user)
        return no_content_response()


class MedicineBarcodeView(APIView):
    """
    GET /api/v1/medicines/barcode/{barcode}/
    Fast barcode lookup — used by billing/cashier.
    Returns medicine info if found and active.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Barcode Lookup',
        description='Look up a medicine by barcode. Returns medicine details if active.',
        responses={
            200: MedicineDetailSerializer,
            404: OpenApiResponse(description='Medicine not found'),
            422: OpenApiResponse(description='Medicine inactive'),
        },
        tags=['Medicine'],
    )
    def get(self, request, barcode):
        medicine = MedicineSelector.get_by_barcode(barcode)

        if not medicine:
            logger.warning(f"Barcode not found: '{barcode}'")
            return error_response(
                message=f"No medicine found for barcode '{barcode}'.",
                status_code=404,
            )

        if not medicine.is_active:
            return error_response(
                message='This medicine is inactive and cannot be billed.',
                status_code=422,
            )

        return success_response(
            data=MedicineDetailSerializer(medicine).data,
            message='Medicine found.',
        )
