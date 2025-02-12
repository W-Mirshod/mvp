from apps.mailers.models import Campaign
from rest_framework import serializers

from utils.get_user_from_request import RequestContext


class CreateCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = (
            "campaign_id",
            "campaign_name",
            "campaign_tag",
            "country",
            "email_content",
        )

    def validate(self, attrs: dict) -> dict:
        user_obj = RequestContext.get_user_from_request(self.context)
        if user_obj is None:
            raise serializers.ValidationError({"detail": "Unknown user."})

        attrs["author"] = user_obj

        return attrs


class RetrieveCampaignSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()

    def get_country(self, obj):
        return str(obj.country) if obj.country else None


    class Meta:
        model = Campaign
        fields = (
            "id",
            "author",
            "campaign_id",
            "campaign_name",
            "campaign_tag",
            "country",
            "email_content",
            "open_rate",
            "visitor_clicks",
            "status",
            "message",
            "created_at",
            "updated_at",
        )


class StartCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ("status",)
