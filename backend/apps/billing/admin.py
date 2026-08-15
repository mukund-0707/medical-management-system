from django.contrib import admin
from .models import BillingSession, BillingSessionItem


class BillingSessionItemInline(admin.TabularInline):
    model = BillingSessionItem
    extra = 0
    readonly_fields = ['id', 'line_total', 'created_at']


@admin.register(BillingSession)
class BillingSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'grand_total', 'created_by', 'created_at']
    list_filter = ['status']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [BillingSessionItemInline]
