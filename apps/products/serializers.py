from rest_framework import serializers

from apps.products.models.products import Product
from apps.products.models.tariffs import Tariff


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "title", "description")


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ("id", "title", "rate", "product")
