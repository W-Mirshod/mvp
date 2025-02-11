from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from apps.proxies.models import Country
from apps.proxies.serializers.country import CountrySerializer
from utils.permissions import IsTokenValid


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsAuthenticated, IsTokenValid)


    @swagger_auto_schema(
        operation_summary="List Countries",
        operation_description="Retrieve a list of all countries."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Country",
        operation_description="Create a new country instance."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Country",
        operation_description="Retrieve a specific country."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Country",
        operation_description="Update a country instance."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update Country",
        operation_description="Partially update a country instance."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Country",
        operation_description="Delete a country instance."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)