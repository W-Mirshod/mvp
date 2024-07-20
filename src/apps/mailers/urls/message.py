from django.urls import path

from .. import views

app_name = "message_api"

urlpatterns = [
    path("", views.SentMessageView.as_view({"get": "list", "post": "create"}), name="product_list"),
    path("<int:pk>/", views.SentMessageView.as_view({"get": "retrieve"}), name="product_by_id"),
    path(
        "message-templates/",
        views.MessageTemplateView.as_view({"get": "list"}),
        name="message-template_list",
    ),
    path(
        "message-templates/<int:pk>/",
        views.MessageTemplateView.as_view({"get": "retrieve"}),
        name="message-template_by_id",
    ),
]
