from django.urls import path
from apps.mail_servers.views.v1.views_mail_servers import (
    ProxyServerView,
    IMAPServerView,
    SMTPServerView,
)
from apps.mail_servers.views.v1.file_upload import FileUploadView, ExportView

app_name = "servers_api"


urlpatterns = [
    path(
        "smtp-servers/",
        SMTPServerView.as_view({"get": "list"}),
        name="smtp-server_list",
    ),
    path(
        "smtp-servers/<int:pk>/",
        SMTPServerView.as_view({"get": "retrieve"}),
        name="smtp-server_by_id",
    ),
    path(
        "imap-servers/",
        IMAPServerView.as_view({"get": "list"}),
        name="imap-server_list",
    ),
    path(
        "imap-servers/<int:pk>/",
        IMAPServerView.as_view({"get": "retrieve"}),
        name="imap-server_by_id",
    ),
    path(
        "proxy-servers/",
        ProxyServerView.as_view({"get": "list"}),
        name="proxy-server_list",
    ),
    path(
        "proxy-servers/<int:pk>/",
        ProxyServerView.as_view({"get": "retrieve"}),
        name="proxy-server_by_id",
    ),
    path(
        "upload/",
        FileUploadView.as_view(),
        name="file_upload",
    ),
    path(
        "export/<str:type>/<str:session>/",
        ExportView.as_view(),
        name="export_data",
    ),
]
