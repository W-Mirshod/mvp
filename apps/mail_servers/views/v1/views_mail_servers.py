import logging

from rest_framework.permissions import IsAuthenticated

from apps.mail_servers.models import IMAPServer, ProxyServer, SMTPServer
from apps.mail_servers.serializers import (
    IMAPServerSerializer,
    ProxyServerSerializer,
    SMTPServerSerializer,
)
from utils.permissions import IsTokenValid
from utils.views import MultiSerializerViewSet

logger = logging.getLogger(__name__)


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

    def list(self, request, *args, **kwargs):
        logger.info(f"Listing SMTP servers for user: {request.user}")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving SMTP server details for user: {request.user}")
        return super().retrieve(request, *args, **kwargs)


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

    def list(self, request, *args, **kwargs):
        logger.info(f"Listing IMAP servers for user: {request.user}")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving IMAP server details for user: {request.user}")
        return super().retrieve(request, *args, **kwargs)


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

    def list(self, request, *args, **kwargs):
        logger.info(f"Listing proxy servers for user: {request.user}")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving proxy server details for user: {request.user}")
        return super().retrieve(request, *args, **kwargs)
    