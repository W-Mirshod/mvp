from rest_framework.permissions import IsAuthenticated

from apps.products.models import Tariff
from apps.products.serializers import TariffSerializer
from utils.permissions import IsTokenValid
from utils.views import MultiSerializerViewSet


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
