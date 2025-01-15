from rest_framework.permissions import IsAuthenticated

from src.apps.mail_servers.models import IMAPServer, ProxyServer, SMTPServer
from src.apps.mail_servers.serializers import (
    IMAPServerSerializer,
    ProxyServerSerializer,
    SMTPServerSerializer,
)
from src.utils.permissions import IsTokenValid
from src.utils.views import MultiSerializerViewSet


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
