from django.db import transaction
from rest_framework import serializers

from apps.mailers.models.event import Event
from apps.mailers.models.message import SentMessage


class SentMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentMessage
        fields = (
            "id",
            "user",
            "server",
            "template",
            "results",
            "is_deleted",
            "created_at",
            "updated_at",
        )


class SentMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentMessage
        fields = (
            "id",
            "user",
            "server",
            "template",
        )

    def create(self, validated_data):
        with transaction.atomic():
            msg = SentMessage.objects.create(**validated_data)
            event = Event.objects.create(
                server=validated_data["server"],
                sent_message=msg,
            )
        return msg, event
