import logging

from rest_framework.permissions import IsAuthenticated

from apps.backend_mailer.serializers.email_serializers import (
    CreateEmailSerializer,
    RetrieveEmailSerializer,
)
from apps.backend_mailer.view_logic.email_qs import EmailQueryset
from utils.permissions import IsTokenValid, IsOwner
from utils.views import MultiSerializerViewSet

logger = logging.getLogger(__name__)


class SentMessageView(MultiSerializerViewSet):
    queryset = None  # see get_queryset
    permission_classes = None  # see get_permissions
    serializers = {
        "list": RetrieveEmailSerializer,
        "create": CreateEmailSerializer,
        "retrieve": RetrieveEmailSerializer,
    }

    def get_queryset(self):
        logger.info(f"Getting queryset for user {self.request.user} with action {self.action}")
        return EmailQueryset.email_queryset(
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
        