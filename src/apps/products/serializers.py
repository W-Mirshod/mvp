from rest_framework import serializers

from src.apps.products.models import Product, Tariff


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "title", "description")


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ("id", "title", "rate", "product")
