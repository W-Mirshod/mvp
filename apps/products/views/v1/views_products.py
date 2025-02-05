import logging

from rest_framework.permissions import IsAuthenticated

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

    def list(self, request, *args, **kwargs):
        logger.info(f"Listing products for user: {request.user}")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving product with id: {kwargs.get('pk')} for user: {request.user}")
        return super().retrieve(request, *args, **kwargs)
    