from rest_framework.permissions import IsAuthenticated

from apps.mailers.serializers.campaign import (
    CreateCampaignSerializer,
    RetrieveCampaignSerializer,
    StartCampaignSerializer,
)
from apps.mailers.view_logic.campaign_qs import CampaignQueryset
from utils.permissions import IsTokenValid, IsOwner
from utils.views import MultiSerializerViewSet


class CampaignView(MultiSerializerViewSet):
    queryset = None  # see get_queryset
    permission_classes = None  # see get_permissions

    serializers = {
        "list": RetrieveCampaignSerializer,
        "create": CreateCampaignSerializer,
        "retrieve": RetrieveCampaignSerializer,
        "partial_update": StartCampaignSerializer,
    }

    def get_queryset(self):
        return CampaignQueryset.campaign_queryset(
            user_obj=self.request.user,
            action=self.action,
            kwargs=self.kwargs,
        )

    def get_permissions(self):

        if self.action in ("list", "retrieve", "update", "partial_update", "destroy"):
            return [
                permission() for permission in (IsAuthenticated, IsTokenValid, IsOwner)
            ]
        else:
            return [permission() for permission in (IsAuthenticated, IsTokenValid)]
