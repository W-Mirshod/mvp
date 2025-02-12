import logging
from drf_yasg import openapi
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

    @swagger_auto_schema(
        operation_summary="List Companies",
        operation_description="Retrieve a list of all companies.",
        responses={200: CompanySerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        logger.info(f"Listing all companies requested by user {request.user.id}")
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Company",
        operation_description="Create a new company instance.",
        request_body=CompanySerializer,
        responses={201: CompanySerializer}
    )
    def create(self, request, *args, **kwargs):
        logger.info(f"Creating new company requested by user {request.user.id}")
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Company",
        operation_description="Retrieve a specific company.",
        responses={200: CompanySerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving company {kwargs.get('pk')} requested by user {request.user.id}")
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Company",
        operation_description="Update a company instance.",
        request_body=CompanyActivitySerializer,
        responses={200: CompanyActivitySerializer}
    )
    def update(self, request, *args, **kwargs):
        logger.info(f"Updating company {kwargs.get('pk')} requested by user {request.user.id}")
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update Company",
        operation_description="Partially update a company instance.",
        request_body=CompanyActivitySerializer,
        responses={200: CompanyActivitySerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        logger.info(f"Partially updating company {kwargs.get('pk')} requested by user {request.user.id}")
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Company",
        operation_description="Delete a company instance.",
        responses={204: openapi.Response(description="No content")}
    )
    def destroy(self, request, *args, **kwargs):
        logger.info(f"Deleting company {kwargs.get('pk')} requested by user {request.user.id}")
        return super().destroy(request, *args, **kwargs)
    