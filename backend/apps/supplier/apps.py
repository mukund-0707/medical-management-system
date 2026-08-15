from django.apps import AppConfig


class SupplierConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.supplier'
    label = 'supplier'
    verbose_name = 'Supplier'
