from apps.mailers.models import Campaign
from rest_framework import serializers

from utils.get_user_from_request import RequestContext


class CreateCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = (
            "campaign_id",
            "campaign_name",
            "shipping_type",
            "message_type",
            "comment",
            "message",
            "country_tag",
        )

    def validate(self, attrs: dict) -> dict:
        user_obj = RequestContext.get_user_from_request(self.context)
        if user_obj is None:
            raise serializers.ValidationError({"detail": "Unknown user."})

        attrs["author"] = user_obj

        return attrs


class RetrieveCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = (
            "id",
            "author",
            "campaign_id",
            "campaign_name",
            "shipping_type",
            "message_type",
            "comment",
            "open_rate",
            "visitor_clicks",
            "status",
            "message",
            "country_tag",
            "created_at",
            "updated_at",
        )


class StartCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ("status",)
