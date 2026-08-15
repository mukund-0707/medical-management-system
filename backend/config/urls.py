"""
Root URL Configuration for MSMS.
All app URLs are versioned under /api/v1/.
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    # ── Admin ──────────────────────────────
    path('admin/', admin.site.urls),

    # ── API v1 ─────────────────────────────
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/medicines/', include('apps.medicine.urls')),
    path('api/v1/suppliers/', include('apps.supplier.urls')),
    path('api/v1/purchases/', include('apps.purchase.urls')),
    path('api/v1/inventory/', include('apps.inventory.urls')),
    path('api/v1/billing/', include('apps.billing.urls')),
    path('api/v1/sales/', include('apps.sales.urls')),
    path('api/v1/dashboard/', include('apps.dashboard.urls')),
    path('api/v1/reports/', include('apps.reports.urls')),

    # ── API Documentation ──────────────────
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
