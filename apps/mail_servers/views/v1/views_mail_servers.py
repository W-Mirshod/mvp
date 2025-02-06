import logging

from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

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

    @swagger_auto_schema(
        operation_summary="List SMTP servers",
        operation_description="Retrieve a list of SMTP servers.\nLog the listing action.\nReturn serialized server data."
    )
    def list(self, request, *args, **kwargs):
        logger.info(f"Listing SMTP servers for user: {request.user}")
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve SMTP server details",
        operation_description="Fetch details of a specific SMTP server.\nLog retrieval action.\nReturn detailed serialized data."
    )
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

    @swagger_auto_schema(
        operation_summary="List IMAP servers",
        operation_description="Retrieve a list of IMAP servers.\nLog the listing action.\nReturn serialized server data."
    )
    def list(self, request, *args, **kwargs):
        logger.info(f"Listing IMAP servers for user: {request.user}")
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve IMAP server details",
        operation_description="Fetch details of a specific IMAP server.\nLog retrieval action.\nReturn detailed serialized data."
    )
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

    @swagger_auto_schema(
        operation_summary="List proxy servers",
        operation_description="Retrieve a list of proxy servers.\nLog the listing action.\nReturn serialized server data."
    )
    def list(self, request, *args, **kwargs):
        logger.info(f"Listing proxy servers for user: {request.user}")
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve proxy server details",
        operation_description="Fetch details of a specific proxy server.\nLog retrieval action.\nReturn detailed serialized data."
    )
    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving proxy server details for user: {request.user}")
        return super().retrieve(request, *args, **kwargs)
