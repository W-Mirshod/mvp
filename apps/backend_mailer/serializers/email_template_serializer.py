from apps.backend_mailer.models import EmailTemplate
from rest_framework import serializers


class CreateEmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = (
            "name",
            "description",
            "subject",
            "content",
            "html_content",
            "language",
            "default_template",
        )


class RetrieveEmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = (
            "id",
            "name",
            "description",
            "subject",
            "content",
            "html_content",
            "language",
            "default_template",
            "created",
            "last_updated",
        )
