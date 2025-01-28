from apps.backend_mailer.models.email import Email
from rest_framework import serializers

from utils.get_user_from_request import RequestContext


class CreateEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = (
            "from_email",
            "to",
            "cc",
            "bcc",
            "subject",
            "message",
            "html_message",
            "priority",
            "scheduled_time",
            "expires_at",
            "headers",
            "template",
            "message_type",
            "email_backend",
        )

    def validate(self, attrs: dict) -> dict:
        user_obj = RequestContext.get_user_from_request(self.context)
        if user_obj is None:
            raise serializers.ValidationError({"detail": "Unknown user."})

        attrs["author"] = user_obj

        return attrs



class RetrieveEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = (
            "author",
            "message_id",
            "from_email",
            "to",
            "cc",
            "bcc",
            "subject",
            "message",
            "html_message",
            "priority",
            "scheduled_time",
            "expires_at",
            "status",
            "headers",
            "template",
            "message_type",
            "email_backend",
        )
