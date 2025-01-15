from rest_framework.permissions import IsAuthenticated

from src.apps.products.models import Product
from src.apps.products.serializers import ProductSerializer
from src.utils.permissions import IsTokenValid
from src.utils.views import MultiSerializerViewSet


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
