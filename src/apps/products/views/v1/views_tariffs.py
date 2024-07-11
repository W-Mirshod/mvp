from apps.products.models import Tariff
from apps.products.serializers import TariffSerializer
from utils.views import MultiSerializerViewSet


class TariffView(MultiSerializerViewSet):
    queryset = Tariff.objects.all()
    serializers = {
        "retrieve": TariffSerializer,
        "list": TariffSerializer,
    }
