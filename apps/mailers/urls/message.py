from django.urls import path

from apps.mailers.views.v1.message import SentMessageView
from apps.mailers.views.v1.template import MessageTemplateView

app_name = "message_api"

urlpatterns = [
    path(
        "",
        SentMessageView.as_view({"get": "list", "post": "create"}),
        name="product_list",
    ),
    path(
        "<int:pk>/",
        SentMessageView.as_view({"get": "retrieve"}),
        name="product_by_id",
    ),
    path(
        "message-templates/",
        MessageTemplateView.as_view({"get": "list"}),
        name="message-template_list",
    ),
    path(
        "message-templates/<int:pk>/",
        MessageTemplateView.as_view({"get": "retrieve"}),
        name="message-template_by_id",
    ),
]
