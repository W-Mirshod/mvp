from django.urls import path

from apps.backend_mailer.views.v1.email_views import SentMessageView
from apps.backend_mailer.views.v1.email_template_views import EmailTemplateView
from apps.backend_mailer.views.v1.email_backend import EmailBackendView


app_name = "backend_email"

urlpatterns = [
    path(
        "",
        SentMessageView.as_view({"get": "list", "post": "create"}),
        name="product_list",
    ),
    path(
        "<int:pk>/",
        SentMessageView.as_view({"get": "retrieve", "delete": "destroy"}),
        name="product_by_id",
    ),
    path(
        "message-templates/",
        EmailTemplateView.as_view({"get": "list", "post": "create"}),
        name="message-template_list",
    ),
    path(
        "message-templates/<int:pk>/",
        EmailTemplateView.as_view({"get": "retrieve", "delete": "destroy"}),
        name="message-template_by_id",
    ),
    path(
        "email-backend/",
        EmailBackendView.as_view({"get": "list", "post": "create"}),
        name="email-backend_list",
    ),
    path(
        "email-backend/<int:pk>/",
        EmailBackendView.as_view({"get": "retrieve", "delete": "destroy"}),
        name="email-backend_by_id",
    ),
]
