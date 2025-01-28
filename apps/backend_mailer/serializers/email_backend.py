from apps.backend_mailer.models import EmailBackend
from rest_framework import serializers

from utils.get_user_from_request import RequestContext


class CreateEmailBackendSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailBackend
        fields = (
            "mailing_type",
            "config",
        )

    def validate(self, attrs: dict) -> dict:
        user_obj = RequestContext.get_user_from_request(self.context)
        if user_obj is None:
            raise serializers.ValidationError({"detail": "Unknown user."})

        attrs["author"] = user_obj

        return attrs


class RetrieveEmailBackendSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailBackend
        fields = (
            "author",
            "mailing_type",
            "config",
            "created_at",
        )
