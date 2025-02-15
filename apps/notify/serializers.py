from rest_framework import serializers

from apps.notify.models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = (
            "title",
            "description",
            "notify_type",
            "data",
            "created_at",
            "is_viewed",
        )
