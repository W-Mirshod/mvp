from rest_framework import serializers

from .models import IMAPServer, MessageTemplate, ProxyServer, SMTPServer


class SMTPServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMTPServer
        fields = ("id", "type", "url", "port", "password", "username", "email_use_tls", "is_active")


class IMAPServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = IMAPServer
        fields = ("id", "type", "url", "port", "password", "username", "email_use_tls", "is_active")


class ProxyServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProxyServer
        fields = ("id", "type", "url", "port", "password", "username", "email_use_tls", "is_active")


class MessageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        fields = ("id", "from_address", "template", "message")
