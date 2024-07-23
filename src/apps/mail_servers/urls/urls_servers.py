from django.urls import path

from .. import views

app_name = "servers_api"

urlpatterns = [
    path("smtp-servers/", views.SMTPServerView.as_view({"get": "list"}), name="smtp-server_list"),
    path(
        "smtp-servers/<int:pk>/",
        views.SMTPServerView.as_view({"get": "retrieve"}),
        name="smtp-server_by_id",
    ),
    path("imap-servers/", views.IMAPServerView.as_view({"get": "list"}), name="imap-server_list"),
    path(
        "imap-servers/<int:pk>/",
        views.IMAPServerView.as_view({"get": "retrieve"}),
        name="imap-server_by_id",
    ),
    path(
        "proxy-servers/", views.ProxyServerView.as_view({"get": "list"}), name="proxy-server_list"
    ),
    path(
        "proxy-servers/<int:pk>/",
        views.ProxyServerView.as_view({"get": "retrieve"}),
        name="proxy-server_by_id",
    ),
]
