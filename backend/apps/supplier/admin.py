from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile', 'email', 'gst_number', 'city', 'status', 'created_at']
    list_filter = ['status', 'city', 'state']
    search_fields = ['name', 'mobile', 'gst_number', 'contact_person']
    readonly_fields = ['id', 'created_at', 'updated_at', 'created_by']
    ordering = ['name']
