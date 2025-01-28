from apps.backend_mailer.models.email import Email
from rest_framework import serializers


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


class RetrieveEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = (
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
