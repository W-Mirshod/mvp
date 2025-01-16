from rest_framework.permissions import IsAuthenticated

from apps.products.models.products import Product
from apps.products.serializers import ProductSerializer
from utils.permissions import IsTokenValid
from utils.views import MultiSerializerViewSet


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
