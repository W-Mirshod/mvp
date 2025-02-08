import logging

from rest_framework import serializers

from apps.proxies.models import ProxyConfig, Judge, Country
from apps.proxies.serializers.country import CountrySerializer
from apps.proxies.serializers.judge import JudgeSerializer
from apps.sentry.sentry_constants import SentryConstants
from apps.sentry.sentry_scripts import SendToSentry


logger = logging.getLogger(__name__)


class ProxyConfigSerializer(serializers.ModelSerializer):
    judge = JudgeSerializer(many=True)
    countries = CountrySerializer(many=True)

    class Meta:
        model = ProxyConfig
        fields = ["id", "author", "judge", "timeout", "countries", "anonymity"]

    def validate_judge(self, value):
        if not value:
            raise serializers.ValidationError("At least one judge is required.")
        return value

    def validate_countries(self, value):
        if not value:
            raise serializers.ValidationError("At least one country is required.")
        return value

    def _create_or_update_related_objects(
        self, instance, related_field, related_model, related_data
    ):
        """Helper method to handle creation/updating of related objects."""
        getattr(instance, related_field).clear()
        related_objects = [
            related_model(proxy_config=instance, **data) for data in related_data
        ]
        related_model.objects.bulk_create(related_objects)

    def create(self, validated_data):
        judges_data = validated_data.pop("judge")
        countries_data = validated_data.pop("countries")

        try:
            proxy_config = ProxyConfig.objects.create(**validated_data)
            self._create_or_update_related_objects(
                proxy_config, "judge", Judge, judges_data
            )
            self._create_or_update_related_objects(
                proxy_config, "countries", Country, countries_data
            )
            return proxy_config
        except Exception as e:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"ProxyConfigSerializer.create: Exception",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": f"Creating proxy serializer failed",
                    "extra_detail": str(e),
                }
            )
            logger.error(f"Creating proxy serializer failed {e}")
            raise serializers.ValidationError(f"Error creating ProxyConfig: {str(e)}")

    def update(self, instance, validated_data):
        judges_data = validated_data.pop("judge", None)
        countries_data = validated_data.pop("countries", None)

        try:
            instance.timeout = validated_data.get("timeout", instance.timeout)
            instance.anonymity = validated_data.get("anonymity", instance.anonymity)
            instance.save()

            if judges_data is not None:
                self._create_or_update_related_objects(
                    instance, "judge", Judge, judges_data
                )

            if countries_data is not None:
                self._create_or_update_related_objects(
                    instance, "countries", Country, countries_data
                )

            return instance
        except Exception as e:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"ProxyConfigSerializer.update: Exception",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": f"Updating proxy serializer failed",
                    "extra_detail": str(e),
                }
            )
            logger.error(f"Updating proxy serializer failed {e}")
            raise serializers.ValidationError(f"Error updating ProxyConfig: {str(e)}")
