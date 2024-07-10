from rest_framework import serializers

from .models import IMAPServer, MessageTemplate, ProxyServer, SMTPServer


class SMTPServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMTPServer
        fields = "__all__"


class IMAPServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = IMAPServer
        fields = "__all__"


class ProxyServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProxyServer
        fields = "__all__"


class MessageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        fields = "__all__"
