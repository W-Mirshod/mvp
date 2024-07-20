from rest_framework import serializers

from apps.mailers.models.template import MessageTemplate


class MessageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        fields = ("id", "from_address", "template", "message")
