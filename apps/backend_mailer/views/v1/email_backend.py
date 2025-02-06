import logging

from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

from apps.backend_mailer.serializers.email_backend import (
    CreateEmailBackendSerializer,
    RetrieveEmailBackendSerializer,
)
from apps.backend_mailer.view_logic.email_backend_qs import EmailBackendQueryset
from utils.permissions import IsTokenValid, IsOwner
from utils.views import MultiSerializerViewSet

logger = logging.getLogger(__name__)


@method_decorator(name='list', decorator=swagger_auto_schema(operation_description="List email backends"))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_description="Create an email backend"))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_description="Retrieve an email backend"))


class EmailBackendView(MultiSerializerViewSet):
    queryset = None  # see get_queryset
    permission_classes = None  # see get_permissions

    serializers = {
        "list": RetrieveEmailBackendSerializer,
        "create": CreateEmailBackendSerializer,
        "retrieve": RetrieveEmailBackendSerializer,
    }

    def get_queryset(self):
        logger.info(f"Getting queryset for user {self.request.user} with action {self.action}")
        return EmailBackendQueryset.email_backend_queryset(
            user_obj=self.request.user,
            action=self.action,
            kwargs=self.kwargs,
        )

    def get_permissions(self):
        logger.info(f"Getting permissions for action {self.action}")
        if self.action in ("list", "retrieve", "update", "partial_update", "destroy"):
            return [
                permission() for permission in (IsAuthenticated, IsTokenValid, IsOwner)
            ]
        else:
            return [permission() for permission in (IsAuthenticated, IsTokenValid)]
