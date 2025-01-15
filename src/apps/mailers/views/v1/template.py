from rest_framework.permissions import IsAuthenticated

from src.apps.mailers.models.template import MessageTemplate
from src.apps.mailers.serializers import MessageTemplateSerializer
from src.utils.permissions import IsTokenValid
from src.utils.views import MultiSerializerViewSet


class MessageTemplateView(MultiSerializerViewSet):
    queryset = MessageTemplate.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    serializers = {
        "list": MessageTemplateSerializer,
        "retrieve": MessageTemplateSerializer,
    }
