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
    @transaction.atomic
    def server_list(self, request, *args, **kwargs):
        try:
            queryset = self.queryset
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def server_by_id(self, request, pk=None, *args, **kwargs):
        try:
            queryset = self.queryset
            server = get_object_or_404(queryset, pk=pk)
            serializer = self.get_serializer(server)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except self.queryset.model.DoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SMTPServerView(MailServerView):
    queryset = SMTPServer.objects.all()
    serializer_class = SMTPServerSerializer


class IMAPServerView(MailServerView):
    queryset = IMAPServer.objects.all()
    serializer_class = IMAPServerSerializer


class ProxyServerView(MailServerView):
    queryset = ProxyServer.objects.all()
    serializer_class = ProxyServerSerializer


class MessageTemplateView(MailServerView):
    queryset = MessageTemplate.objects.all()
    serializer_class = MessageTemplateSerializer
