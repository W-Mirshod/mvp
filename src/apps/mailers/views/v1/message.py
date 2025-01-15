from rest_framework.permissions import IsAuthenticated

from src.apps.mailers.models import SentMessage
from src.apps.mailers.serializers import (
    SentMessageCreateSerializer,
    SentMessageSerializer,
)
from src.utils.permissions import IsTokenValid
from src.utils.views import MultiSerializerViewSet


class SentMessageView(MultiSerializerViewSet):
    queryset = SentMessage.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    serializers = {
        "list": SentMessageSerializer,
        "create": SentMessageCreateSerializer,
        "retrieve": SentMessageSerializer,
    }
