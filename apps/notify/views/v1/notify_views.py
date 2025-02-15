import logging

from rest_framework.generics import UpdateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from drf_yasg.utils import swagger_auto_schema
from utils.permissions import IsTokenValid
from utils.pagination import StandardResultsSetPagination
from apps.notify.models import Notification
from apps.notify.serializers import NotificationSerializer

logger = logging.getLogger(__name__)


class NotificationViewSet(ListModelMixin, GenericViewSet, UpdateAPIView):
    permission_classes = (IsAuthenticated, IsTokenValid)
    queryset = None  # see get_queryset
    serializer_class = NotificationSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Notification.objects.filter(user_id=self.request.user.id)

    @swagger_auto_schema(
        operation_summary="Notification list",
        operation_description="Retrieve a list of all notifications.",
    )
    def list(self, request, *args, **kwargs):
        logger.info(f"Notification list request received from user {request.user}")
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Notification",
        operation_description="Update a Notification.",
    )
    def update(self, request, *args, **kwargs):
        logger.info(
            f"Update request received from user {request.user} for notification {kwargs.get('pk')}"
        )
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Notification Update ",
        operation_description="Partially update a notification.",
    )
    def partial_update(self, request, *args, **kwargs):
        logger.info(
            f"Partial update request received from user {request.user} for notification {kwargs.get('pk')}"
        )
        return super().partial_update(request, *args, **kwargs)
