import logging
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from apps.proxies.models import ProxyConfig
from apps.proxies.serializers.proxy_config import ProxyConfigSerializer
from utils.permissions import IsTokenValid, IsOwner


logger = logging.getLogger(__name__)


@swagger_auto_schema(tags=['Proxy Configs'])
class ProxyConfigViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing proxy configurations.
    """
    queryset = ProxyConfig.objects.none()
    serializer_class = ProxyConfigSerializer
    permission_classes = (IsAuthenticated, IsTokenValid, IsOwner)
    
    @swagger_auto_schema(
        operation_summary="List Proxy Configs",
        operation_description="Retrieve a list of all proxy configurations."
    )
    def list(self, request, *args, **kwargs):
        logger.info(f"User {request.user.pk} listing proxy configs")
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Proxy Config",
        operation_description="Create a new proxy configuration."
    )
    def create(self, request, *args, **kwargs):
        logger.info(f"User {request.user.pk} creating proxy config")
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Proxy Config",
        operation_description="Retrieve a specific proxy configuration."
    )
    def retrieve(self, request, *args, **kwargs):
        logger.info(f"User {request.user.pk} retrieving proxy config {kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Proxy Config",
        operation_description="Update a proxy configuration."
    )
    def update(self, request, *args, **kwargs):
        logger.info(f"User {request.user.pk} updating proxy config {kwargs.get('pk')}")
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update Proxy Config",
        operation_description="Partially update a proxy configuration."
    )
    def partial_update(self, request, *args, **kwargs):
        logger.info(f"User {request.user.pk} partially updating proxy config {kwargs.get('pk')}")
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Proxy Config",
        operation_description="Delete a proxy configuration."
    )
    def destroy(self, request, *args, **kwargs):
        logger.info(f"User {request.user.pk} deleting proxy config {kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)    

    def get_queryset(self):
        logger.debug(f"Filtering proxy configs for user {self.request.user.pk}")
        return ProxyConfig.objects.filter(author_id=self.request.user.pk)
    