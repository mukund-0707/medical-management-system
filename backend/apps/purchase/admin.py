from django.contrib import admin
from .models import Purchase, PurchaseItem


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 0
    readonly_fields = ['id', 'total_amount', 'created_at']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'supplier', 'invoice_date', 'status', 'created_at']
    list_filter = ['status', 'invoice_date']
    search_fields = ['invoice_number', 'supplier__name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'finalized_at', 'cancelled_at']
    inlines = [PurchaseItemInline]
