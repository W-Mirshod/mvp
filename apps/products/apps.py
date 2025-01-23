from django.apps import AppConfig
from health_check.plugins import plugin_dir

from apps.products.health_check.v1.hc_product import ProductHealthCheck
from apps.products.health_check.v1.hc_tariff import TariffHealthCheck


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"

    def ready(self):

        plugin_dir.register(ProductHealthCheck)
        plugin_dir.register(TariffHealthCheck)
