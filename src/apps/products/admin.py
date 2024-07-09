from django.contrib import admin

from apps.products.models import Product, Tariff


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


@admin.register(Tariff)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "rate", "product")
