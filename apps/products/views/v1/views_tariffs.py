import logging

from rest_framework.permissions import IsAuthenticated

from apps.products.models.tariffs import Tariff
from apps.products.serializers import TariffSerializer
from utils.permissions import IsTokenValid
from utils.views import MultiSerializerViewSet


logger = logging.getLogger(__name__)


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

    def list(self, request, *args, **kwargs):
        logger.info(f"Listing tariffs for user: {request.user}")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving tariff details for user: {request.user}, tariff_id: {kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)
    