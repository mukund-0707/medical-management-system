"""
URL routes for Medicine module.
Mounted at: /api/v1/medicines/
"""

from django.urls import path
from .views import MedicineListCreateView, MedicineDetailView, MedicineBarcodeView

app_name = 'medicine'

urlpatterns = [
    path('', MedicineListCreateView.as_view(), name='medicine-list-create'),
    path('<uuid:pk>/', MedicineDetailView.as_view(), name='medicine-detail'),
    path('barcode/<str:barcode>/', MedicineBarcodeView.as_view(), name='medicine-barcode'),
]
