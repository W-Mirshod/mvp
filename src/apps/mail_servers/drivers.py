from django.core.mail import EmailMessage, get_connection
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from constance import config
from .models import SMTPServer, IMAPServer

class BaseDriver:
    def __init__(self, server_name):
        self.server_name = server_name
        self.settings = self.get_server_settings()

    def get_server_settings(self):
        raise ImproperlyConfigured("Subclasses must implement this method")

    def send_mail(self, subject, message, recipient_list):
        raise ImproperlyConfigured("Subclasses must implement this method")

class SMTPDriver(BaseDriver):
    def __init__(self, server_name):
        super().__init__(server_name)
        self.enable = config.ENABLE_SMTP_SENDING

    def get_server_settings(self):
        try:
            settings = SMTPServer.objects.get(url=self.server_name, is_active=True)
        except SMTPServer.DoesNotExist:
            raise ObjectDoesNotExist("Active SMTP settings for the server not found")
        return settings

    def send_mail(self, subject, message, recipient_list):
        if not self.enable:
            raise ImproperlyConfigured("SMTP sending is disabled")

        with get_connection(
            host=self.settings.url,
            port=self.settings.port,
            username=self.settings.username,
            password=self.settings.password,
            use_tls=self.settings.email_use_tls
        ) as connection:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=self.settings.username,
                to=recipient_list,
                connection=connection
            )
            email.send()

class IMAPDriver(BaseDriver):
    def __init__(self, server_name):
        super().__init__(server_name)
        self.enable = config.ENABLE_IMAP_SENDING

    def get_server_settings(self):
        try:
            settings = IMAPServer.objects.get(url=self.server_name, is_active=True)
        except IMAPServer.DoesNotExist:
            raise ObjectDoesNotExist("Active IMAP settings for the server not found")
        return settings

    def send_mail(self, subject, message, recipient_list):
        if not self.enable:
            raise ImproperlyConfigured("IMAP sending is disabled")
        with get_connection(
            host=self.settings.url,
            port=self.settings.port,
            username=self.settings.username,
            password=self.settings.password,
            use_tls=self.settings.email_use_tls
        ) as connection:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=self.settings.username,
                to=recipient_list,
                connection=connection
            )
            email.send()
