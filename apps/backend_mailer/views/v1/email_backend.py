from rest_framework.permissions import IsAuthenticated

from apps.backend_mailer.serializers.email_backend import (
    CreateEmailBackendSerializer,
    RetrieveEmailBackendSerializer,
)
from apps.backend_mailer.view_logic.email_backend_qs import EmailBackendQueryset
from utils.permissions import IsTokenValid, IsOwner
from utils.views import MultiSerializerViewSet


class EmailBackendView(MultiSerializerViewSet):
    queryset = None  # see get_queryset
    permission_classes = None  # see get_permissions

    serializers = {
        "list": RetrieveEmailBackendSerializer,
        "create": CreateEmailBackendSerializer,
        "retrieve": RetrieveEmailBackendSerializer,
    }

    def get_queryset(self):
        return EmailBackendQueryset.email_backend_queryset(
            user_obj=self.request.user,
            action=self.action,
            kwargs=self.kwargs,
        )

    def get_permissions(self):

        if self.action in ("list", "retrieve", "update", "partial_update", "destroy"):
            return [
                permission() for permission in (IsAuthenticated, IsTokenValid, IsOwner)
            ]
        else:
            return [permission() for permission in (IsAuthenticated, IsTokenValid)]
