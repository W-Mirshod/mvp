import logging
from drf_yasg.utils import swagger_auto_schema 

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

    @swagger_auto_schema(operation_description="Retrieve company details\nLog retrieval action\nReturn serialized data")
    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving company with id {kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="List all companies\nLog listing action\nReturn serialized list")
    def list(self, request, *args, **kwargs):
        logger.info("Listing all companies")
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new company\nLog creation action\nValidate and save data")
    def create(self, request, *args, **kwargs):
        logger.info(f"Creating new company with data: {request.data}")
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete a company\nLog deletion action\nRemove instance by id")
    def destroy(self, request, *args, **kwargs):
        logger.info(f"Deleting company with id {kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Update a company\nLog update action\nValidate, update, and return data")
    def update(self, request, *args, **kwargs):
        logger.info(f"Updating company with id {kwargs.get('pk')}")
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Partially update a company\nLog partial update action\nValidate and update selected fields")
    def partial_update(self, request, *args, **kwargs):
        logger.info(f"Partially updating company with id {kwargs.get('pk')}")
        return super().partial_update(request, *args, **kwargs)
