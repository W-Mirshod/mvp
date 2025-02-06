import logging

from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

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

    @swagger_auto_schema(
        operation_summary="List tariffs",
        operation_description="Retrieve a list of available tariffs.\nLog the listing action.\nReturn serialized tariff data."
    )
    def list(self, request, *args, **kwargs):
        logger.info(f"Listing tariffs for user: {request.user}")
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve tariff details",
        operation_description="Fetch details of a specific tariff.\nLog retrieval action.\nReturn detailed serialized data."
    )
    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving tariff details for user: {request.user}, tariff_id: {kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)
