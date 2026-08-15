from django.contrib import admin
from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ['id', 'medicine', 'inventory_batch', 'quantity',
                       'unit_price', 'line_total', 'created_at']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'sale_date', 'payment_mode',
                    'grand_total', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'payment_mode', 'sale_date']
    search_fields = ['invoice_number']
    readonly_fields = ['id', 'invoice_number', 'billing_session_id',
                       'created_at', 'updated_at', 'cancelled_at']
    inlines = [SaleItemInline]

    def has_delete_permission(self, request, obj=None):
        return False  # Sales records are permanent
