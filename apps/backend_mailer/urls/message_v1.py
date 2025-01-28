from django.urls import path

from apps.backend_mailer.views.v1.email_views import SentMessageView
from apps.backend_mailer.views.v1.email_tamplate_views import EmailTemplateView
app_name = "backend_email"

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
        EmailTemplateView.as_view({"get": "list",  "post": "create"}),
        name="message-template_list",
    ),
    path(
        "message-templates/<int:pk>/",
        EmailTemplateView.as_view({"get": "retrieve"}),
        name="message-template_by_id",
    ),
]
