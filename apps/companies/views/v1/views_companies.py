import logging

from rest_framework.permissions import IsAuthenticated

from apps.companies.models.company import Company
from apps.companies.serializers import CompanySerializer, CompanyActivitySerializer
from utils.permissions import IsTokenValid
from utils.views import MultiSerializerViewSet


logger = logging.getLogger(__name__)


class CompanyView(MultiSerializerViewSet):
    queryset = Company.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    serializers = {
        "retrieve": CompanySerializer,
        "list": CompanySerializer,
        "create": CompanySerializer,
        "destroy": CompanySerializer,
        "update": CompanyActivitySerializer,
    }

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving company with id {kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        logger.info("Listing all companies")
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info("Creating new company")
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.info(f"Deleting company with id {kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Updating company with id {kwargs.get('pk')}")
        return super().update(request, *args, **kwargs)
    