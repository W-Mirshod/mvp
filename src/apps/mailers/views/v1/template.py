from rest_framework.permissions import IsAuthenticated

from apps.mailers.models.template import MessageTemplate
from apps.mailers.serializers import MessageTemplateSerializer
from utils.permissions import IsTokenValid
from utils.views import MultiSerializerViewSet


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
