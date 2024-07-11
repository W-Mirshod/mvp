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
from utils.views import MultiSerializerViewSet


class SMTPServerView(MultiSerializerViewSet):
    queryset = SMTPServer.objects.all()
    serializers = {
        "retrieve": SMTPServerSerializer,
        "list": SMTPServerSerializer,
    }


class IMAPServerView(MultiSerializerViewSet):
    queryset = IMAPServer.objects.all()
    serializers = {
        "retrieve": IMAPServerSerializer,
        "list": IMAPServerSerializer,
    }


class ProxyServerView(MultiSerializerViewSet):
    queryset = ProxyServer.objects.all()
    serializers = {
        "retrieve": ProxyServerSerializer,
        "list": ProxyServerSerializer,
    }


class MessageTemplateView(MultiSerializerViewSet):
    queryset = MessageTemplate.objects.all()
    serializers = {
        "retrieve": MessageTemplateSerializer,
        "list": MessageTemplateSerializer,
    }
