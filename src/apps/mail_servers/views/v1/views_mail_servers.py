from rest_framework.permissions import IsAuthenticated

from apps.mail_servers.models import (
    IMAPServer,
    MessageTemplate,
    ProxyServer,
    SMTPServer,
)
from apps.mail_servers.serializers import (
    IMAPServerSerializer,
    MessageTemplateSerializer,
    ProxyServerSerializer,
    SMTPServerSerializer,
)
from utils.permissions import IsTokenValid
from utils.views import MultiSerializerViewSet


class SMTPServerView(MultiSerializerViewSet):
    queryset = SMTPServer.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    serializers = {
        "retrieve": SMTPServerSerializer,
        "list": SMTPServerSerializer,
    }


class IMAPServerView(MultiSerializerViewSet):
    queryset = IMAPServer.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    serializers = {
        "retrieve": IMAPServerSerializer,
        "list": IMAPServerSerializer,
    }


class ProxyServerView(MultiSerializerViewSet):
    queryset = ProxyServer.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    serializers = {
        "retrieve": ProxyServerSerializer,
        "list": ProxyServerSerializer,
    }


class MessageTemplateView(MultiSerializerViewSet):
    queryset = MessageTemplate.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    serializers = {
        "retrieve": MessageTemplateSerializer,
        "list": MessageTemplateSerializer,
    }
