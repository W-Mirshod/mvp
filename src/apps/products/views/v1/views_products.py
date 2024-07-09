from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from apps.products.models import Product
from utils.views import MultiSerializerViewSet


class GetProductsView(MultiSerializerViewSet):
    queryset = Product.objects.none()
    authentication_classes = []
    permission_classes = []

    @transaction.atomic
    def product_list(self, request):
        products = Product.objects.all()
        products_list = [
            {"id": product.id, "title": product.title, "description": product.description}
            for product in products
        ]
        return Response(products_list, status=status.HTTP_200_OK)

    @transaction.atomic
    def product_by_id(self, request, id):
        try:
            product = Product.objects.get(pk=id)
            product_data = {
                "id": product.id,
                "title": product.title,
                "description": product.description,
            }
            return Response(product_data, status=status.HTTP_200_OK)
        except Product.DoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
