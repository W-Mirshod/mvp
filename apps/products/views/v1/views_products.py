import logging

from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from apps.products.models.products import Product
from apps.products.serializers import ProductSerializer
from utils.permissions import IsTokenValid
from utils.views import MultiSerializerViewSet


logger = logging.getLogger(__name__)


class ProductView(MultiSerializerViewSet):
    queryset = Product.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    serializers = {
        "retrieve": ProductSerializer,
        "list": ProductSerializer,
    }

    @swagger_auto_schema(
        operation_summary="List products",
        operation_description="Retrieve a list of available products.\nLog the listing action.\nReturn serialized product data."
    )
    def list(self, request, *args, **kwargs):
        logger.info(f"Listing products for user: {request.user}")
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve product details",
        operation_description="Fetch details of a specific product.\nLog retrieval action.\nReturn detailed serialized data."
    )
    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving product with id: {kwargs.get('pk')} for user: {request.user}")
        return super().retrieve(request, *args, **kwargs)
