"""
Dashboard Views — read-only aggregated data.
No business operations here.
"""

import logging
from datetime import date
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter

from common.responses.responses import success_response
from .services.dashboard_service import DashboardService

logger = logging.getLogger('apps.dashboard')


def _parse_date(date_str: str) -> date | None:
    """Parse YYYY-MM-DD string, return None if invalid."""
    if not date_str:
        return None
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        return None


class DashboardKPIView(APIView):
    """GET /api/v1/dashboard/ — Main KPI cards."""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Dashboard KPI Summary',
        description="Top-level KPI cards. Returns today's data by default.",
        parameters=[
            OpenApiParameter('date', str, description='Filter date YYYY-MM-DD (default: today)'),
        ],
        tags=['Dashboard'],
    )
    def get(self, request):
        filter_date = _parse_date(request.GET.get('date', ''))
        data = DashboardService.get_kpi_summary(filter_date=filter_date)
        return success_response(data=data, message='Dashboard KPIs fetched.')


class DashboardSalesView(APIView):
    """GET /api/v1/dashboard/sales/ — Sales summary."""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Sales Summary',
        parameters=[
            OpenApiParameter('date_from', str, description='YYYY-MM-DD'),
            OpenApiParameter('date_to', str, description='YYYY-MM-DD'),
        ],
        tags=['Dashboard'],
    )
    def get(self, request):
        date_from = _parse_date(request.GET.get('date_from', ''))
        date_to = _parse_date(request.GET.get('date_to', ''))
        data = DashboardService.get_sales_summary(date_from=date_from, date_to=date_to)
        return success_response(data=data, message='Sales summary fetched.')


class DashboardPurchaseView(APIView):
    """GET /api/v1/dashboard/purchases/ — Purchase summary."""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Purchase Summary',
        parameters=[
            OpenApiParameter('date_from', str, description='YYYY-MM-DD'),
            OpenApiParameter('date_to', str, description='YYYY-MM-DD'),
        ],
        tags=['Dashboard'],
    )
    def get(self, request):
        date_from = _parse_date(request.GET.get('date_from', ''))
        date_to = _parse_date(request.GET.get('date_to', ''))
        data = DashboardService.get_purchase_summary(date_from=date_from, date_to=date_to)
        return success_response(data=data, message='Purchase summary fetched.')


class DashboardInventoryView(APIView):
    """GET /api/v1/dashboard/inventory/ — Inventory health summary."""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Inventory Summary',
        description='Low stock, expiring soon, expired batches.',
        tags=['Dashboard'],
    )
    def get(self, request):
        data = DashboardService.get_inventory_summary()
        return success_response(data=data, message='Inventory summary fetched.')


class DashboardAlertsView(APIView):
    """GET /api/v1/dashboard/alerts/ — Priority-sorted alerts."""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Dashboard Alerts',
        description='Returns priority-sorted alerts: expired, expiring, low stock.',
        tags=['Dashboard'],
    )
    def get(self, request):
        data = DashboardService.get_alerts()
        return success_response(data=data, message='Alerts fetched.')
