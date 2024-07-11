from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

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


class MailServerView(MultiSerializerViewSet):
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class SMTPServerView(MailServerView):
    queryset = SMTPServer.objects.all()
    serializers = {
        "retrieve": SMTPServerSerializer,
        "list": SMTPServerSerializer,
    }


class IMAPServerView(MailServerView):
    queryset = IMAPServer.objects.all()
    serializers = {
        "retrieve": IMAPServerSerializer,
        "list": IMAPServerSerializer,
    }


class ProxyServerView(MailServerView):
    queryset = ProxyServer.objects.all()
    serializers = {
        "retrieve": ProxyServerSerializer,
        "list": ProxyServerSerializer,
    }


class MessageTemplateView(MailServerView):
    queryset = MessageTemplate.objects.all()
    serializers = {
        "retrieve": MessageTemplateSerializer,
        "list": MessageTemplateSerializer,
    }
