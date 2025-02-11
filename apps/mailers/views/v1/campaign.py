import logging
from rest_framework.permissions import IsAuthenticated

from apps.mailers.serializers.campaign import (
    CreateCampaignSerializer,
    RetrieveCampaignSerializer,
    StartCampaignSerializer,
)
from apps.mailers.view_logic.campaign_qs import CampaignQueryset
from utils.permissions import IsTokenValid, IsOwner
from utils.views import MultiSerializerViewSet
from drf_yasg.utils import swagger_auto_schema



logger = logging.getLogger(__name__)


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
        logger.info(f"Getting queryset for user {self.request.user} with action {self.action}")
        return CampaignQueryset.campaign_queryset(
            user_obj=self.request.user,
            action=self.action,
            kwargs=self.kwargs,
        )

    def get_permissions(self):
        logger.info(f"Getting permissions for action {self.action}")
        if self.action in ("list", "retrieve", "update", "partial_update", "destroy"):
            return [
                permission() for permission in (IsAuthenticated, IsTokenValid, IsOwner)
            ]
        else:
            return [permission() for permission in (IsAuthenticated, IsTokenValid)]
    

    @swagger_auto_schema(
        operation_summary="List Campaigns",
        operation_description="Retrieve a list of all campaigns."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Campaign",
        operation_description="Create a new campaign instance."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Campaign",
        operation_description="Retrieve a specific campaign."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Campaign",
        operation_description="Update a campaign instance."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Start Campaign",
        operation_description="Start a campaign instance."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Campaign",
        operation_description="Delete a campaign instance."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)