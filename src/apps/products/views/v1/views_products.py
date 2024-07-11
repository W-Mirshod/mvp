from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from utils.views import MultiSerializerViewSet


class ProductView(MultiSerializerViewSet):
    queryset = Product.objects.all()
    serializers = {
        "retrieve": ProductSerializer,
        "list": ProductSerializer,
    }
