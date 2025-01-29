from rest_framework.permissions import IsAuthenticated

from apps.backend_mailer.serializers.email_serializers import (
    CreateEmailSerializer,
    RetrieveEmailSerializer,
)
from apps.backend_mailer.view_logic.email_qs import EmailQueryset
from utils.permissions import IsTokenValid
from utils.views import MultiSerializerViewSet


class SentMessageView(MultiSerializerViewSet):
    queryset = None  # see get_queryset
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    serializers = {
        "list": RetrieveEmailSerializer,
        "create": CreateEmailSerializer,
        "retrieve": RetrieveEmailSerializer,
    }

    def get_queryset(self):
        return EmailQueryset.email_queryset(
            user_obj=self.request.user,
            action=self.action,
            kwargs=self.kwargs,
        )
