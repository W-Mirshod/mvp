from rest_framework.permissions import IsAuthenticated

from src.apps.products.models import Tariff
from src.apps.products.serializers import TariffSerializer
from src.utils.permissions import IsTokenValid
from src.utils.views import MultiSerializerViewSet


class TariffView(MultiSerializerViewSet):
    queryset = Tariff.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    serializers = {
        "retrieve": TariffSerializer,
        "list": TariffSerializer,
    }
