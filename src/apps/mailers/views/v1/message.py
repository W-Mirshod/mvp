from rest_framework.permissions import IsAuthenticated

from apps.mailers.models import SentMessage
from apps.mailers.serializers import SentMessageCreateSerializer, SentMessageSerializer
from utils.permissions import IsTokenValid
from utils.views import MultiSerializerViewSet


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
