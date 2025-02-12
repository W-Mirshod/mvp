import logging
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from apps.proxies.models import Judge
from apps.proxies.serializers.judge import JudgeSerializer
from utils.permissions import IsTokenValid

logger = logging.getLogger(__name__)


class JudgeViewSet(viewsets.ModelViewSet):
    queryset = Judge.objects.all()
    serializer_class = JudgeSerializer
    permission_classes = (IsAuthenticated, IsTokenValid)

    @swagger_auto_schema(
        operation_summary="List Judges",
        operation_description="Retrieve a list of all judges."
    )
    def list(self, request, *args, **kwargs):
        logger.info("Retrieving list of judges")
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Judge",
        operation_description="Create a new judge instance."
    )
    def create(self, request, *args, **kwargs):
        logger.info("Creating new judge")
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Judge",
        operation_description="Retrieve a specific judge."
    )
    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving judge with id {kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Judge",
        operation_description="Update a judge instance."
    )
    def update(self, request, *args, **kwargs):
        logger.info(f"Updating judge with id {kwargs.get('pk')}")
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update Judge",
        operation_description="Partially update a judge instance."
    )
    def partial_update(self, request, *args, **kwargs):
        logger.info(f"Partially updating judge with id {kwargs.get('pk')}")
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Judge",
        operation_description="Delete a judge instance."
    )
    def destroy(self, request, *args, **kwargs):
        logger.info(f"Deleting judge with id {kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)
    