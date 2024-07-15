from constance import config
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.core.mail import EmailMessage, get_connection

from apps.mail_servers.models import ProxyServer

from .base_driver import BaseDriver


class ProxyDriver(BaseDriver):
    def __init__(self, server_name):
        super().__init__(server_name)
        self.enable = config.ENABLE_PROXY_SENDING

    def get_server_settings(self):
        try:
            settings = ProxyServer.objects.get(url=self.server_name, is_active=True)
        except ProxyServer.DoesNotExist:
            raise ObjectDoesNotExist("Active Proxy settings for the server not found")
        return settings

    def send_mail(self, subject, message, recipient_list):
        if not self.enable:
            raise ImproperlyConfigured("Proxy sending is disabled")

        with get_connection(
            host=self.settings.url,
            port=self.settings.port,
            username=self.settings.username,
            password=self.settings.password,
            use_tls=self.settings.email_use_tls,
        ) as connection:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=self.settings.username,
                to=recipient_list,
                connection=connection,
            )
            email.send()
