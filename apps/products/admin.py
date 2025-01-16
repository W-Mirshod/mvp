from django.contrib import admin

from apps.products.models.products import Product
from apps.products.models.tariffs import Tariff


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ("title", "rate", "product")
