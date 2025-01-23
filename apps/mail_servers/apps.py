from django.apps import AppConfig
from health_check.plugins import plugin_dir
from apps.mail_servers.health_check.v1.hc_imap import IMAPHealthCheck
from apps.mail_servers.health_check.v1.hс_smtp import SMTPHealthCheck
from apps.mail_servers.health_check.v1.hc_proxy import ProxyHealthCheck


class MailServersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.mail_servers"

    def ready(self):

        plugin_dir.register(IMAPHealthCheck)
        plugin_dir.register(SMTPHealthCheck)
        plugin_dir.register(ProxyHealthCheck)
