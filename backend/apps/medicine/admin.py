from django.contrib import admin
from .models import Medicine


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'barcode', 'manufacturer', 'strength', 'dosage_form', 'status', 'created_at']
    list_filter = ['status', 'dosage_form', 'category']
    search_fields = ['name', 'barcode', 'generic_name', 'manufacturer']
    readonly_fields = ['id', 'created_at', 'updated_at', 'created_by']
    ordering = ['name']
