"""
Billing Session Views — thin views only.
"""

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from common.responses.responses import (
    success_response, created_response, error_response, no_content_response
)
from .models import BillingSession, BillingSessionItem
from .serializers import (
    BillingSessionSerializer, AddItemSerializer, UpdateItemSerializer
)
from .services.billing_service import BillingSessionService
from .selectors.billing_selector import BillingSessionSelector

logger = logging.getLogger('apps.billing')


class BillingSessionCreateView(APIView):
    """
    POST /api/v1/billing/sessions/
    Create a new empty billing session.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Create Billing Session',
        description='Opens a new cart. Returns session ID to use for all subsequent cart operations.',
        responses={201: BillingSessionSerializer},
        tags=['Billing'],
    )
    def post(self, request):
        session = BillingSessionService.create_session(created_by=request.user)
        return created_response(
            data=BillingSessionSerializer(session).data,
            message='Billing session created.',
        )


class BillingSessionDetailView(APIView):
    """
    GET    /api/v1/billing/sessions/{id}/  — Get session with items
    DELETE /api/v1/billing/sessions/{id}/  — Cancel session
    """
    permission_classes = [IsAuthenticated]

    def _get_session(self, session_id):
        return BillingSessionSelector.get_by_id(session_id)

    @extend_schema(
        summary='Get Billing Session',
        responses={200: BillingSessionSerializer, 404: OpenApiResponse(description='Not found')},
        tags=['Billing'],
    )
    def get(self, request, pk):
        session = self._get_session(pk)
        if not session:
            return error_response(message='Session not found.', status_code=404)

        return success_response(
            data=BillingSessionSerializer(session).data,
            message='Session fetched successfully.',
        )

    @extend_schema(
        summary='Cancel Billing Session',
        responses={204: OpenApiResponse(description='Session cancelled')},
        tags=['Billing'],
    )
    def delete(self, request, pk):
        session = self._get_session(pk)
        if not session:
            return error_response(message='Session not found.', status_code=404)

        try:
            BillingSessionService.cancel_session(session)
            return no_content_response()
        except ValueError as exc:
            return error_response(message=str(exc), status_code=422)


class BillingSessionItemView(APIView):
    """
    POST /api/v1/billing/sessions/{id}/items/
    Add item to cart (or increase quantity if already exists).
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AddItemSerializer,
        responses={
            200: BillingSessionSerializer,
            400: OpenApiResponse(description='Validation error'),
            422: OpenApiResponse(description='Out of stock / inactive medicine'),
        },
        summary='Add Item to Cart',
        description='Add a medicine to the billing session. If already in cart, quantity is increased.',
        tags=['Billing'],
    )
    def post(self, request, pk):
        session = BillingSessionSelector.get_by_id(pk)
        if not session:
            return error_response(message='Session not found.', status_code=404)

        serializer = AddItemSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message='Validation failed.',
                errors=serializer.errors,
                status_code=400,
            )

        try:
            BillingSessionService.add_item(
                session=session,
                medicine_id=str(serializer.validated_data['medicine_id']),
                quantity=serializer.validated_data['quantity'],
                discount_percentage=serializer.validated_data.get('discount_percentage', 0),
            )
            # Re-fetch session from DB to get updated totals
            updated_session = BillingSessionSelector.get_by_id(pk)
            return success_response(
                data=BillingSessionSerializer(updated_session).data,
                message='Item added to cart.',
            )
        except ValueError as exc:
            return error_response(message=str(exc), status_code=422)


class BillingSessionItemDetailView(APIView):
    """
    PATCH  /api/v1/billing/sessions/{id}/items/{item_id}/  — Update quantity
    DELETE /api/v1/billing/sessions/{id}/items/{item_id}/  — Remove item
    """
    permission_classes = [IsAuthenticated]

    def _get_session_and_item(self, session_id, item_id):
        session = BillingSessionSelector.get_by_id(session_id)
        item = BillingSessionSelector.get_item_by_id(item_id)
        return session, item

    @extend_schema(
        request=UpdateItemSerializer,
        summary='Update Cart Item',
        responses={200: BillingSessionSerializer},
        tags=['Billing'],
    )
    def patch(self, request, pk, item_pk):
        session, item = self._get_session_and_item(pk, item_pk)
        if not session:
            return error_response(message='Session not found.', status_code=404)
        if not item or str(item.session_id) != str(pk):
            return error_response(message='Item not found in this session.', status_code=404)

        serializer = UpdateItemSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(
                message='Validation failed.',
                errors=serializer.errors,
                status_code=400,
            )

        try:
            BillingSessionService.update_item(
                session=session,
                item=item,
                quantity=serializer.validated_data.get('quantity', item.quantity),
                discount_percentage=serializer.validated_data.get('discount_percentage'),
            )
            return success_response(
                data=BillingSessionSerializer(
                    BillingSessionSelector.get_by_id(pk)
                ).data,
                message='Cart item updated.',
            )
        except ValueError as exc:
            return error_response(message=str(exc), status_code=422)

    @extend_schema(
        summary='Remove Cart Item',
        responses={204: OpenApiResponse(description='Item removed')},
        tags=['Billing'],
    )
    def delete(self, request, pk, item_pk):
        session, item = self._get_session_and_item(pk, item_pk)
        if not session:
            return error_response(message='Session not found.', status_code=404)
        if not item or str(item.session_id) != str(pk):
            return error_response(message='Item not found in this session.', status_code=404)

        try:
            BillingSessionService.remove_item(session=session, item=item)
            return no_content_response()
        except ValueError as exc:
            return error_response(message=str(exc), status_code=422)
