from django.urls import path

from apps.mailers.views.v1.campaign import CampaignView

app_name = "campaign_api"

urlpatterns = [
    path(
        "",
        CampaignView.as_view({"get": "list", "post": "create"}),
        name="campaign_list",
    ),
    path(
        "<int:pk>/",
        CampaignView.as_view({"get": "retrieve"}),
        name="campaign_by_id",
    ),
]
