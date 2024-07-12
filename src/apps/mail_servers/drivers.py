from django.core.mail import EmailMessage, get_connection
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from constance import config
from .models import SMTPServer, IMAPServer, ProxyServer
from apps.mailers.models import Event
from apps.mailers.choices import StatusType
from apps.mail_servers.models.models_servers import Server


class BaseDriver:
    def __init__(self, server_name):
        self.server_name = server_name
        self.server = Server.objects.get(url=self.server_name)
        self.settings = self.get_server_settings()

    def get_server_settings(self):
        raise ImproperlyConfigured("Subclasses must implement this method")

    def send_mail(self, subject, message, recipient_list):
        raise ImproperlyConfigured("Subclasses must implement this method")

    def add_message_to_queue(self, subject, message, recipient_list):
        Event.create_new_event(
            user=None,
            server=self.server,
            template=message,
            results={
                "subject": subject,
                "recipient_list": recipient_list
            }
        )

    def process_queue(self):
        events = Event.objects.filter(server=self.server, status=StatusType.NEW)
        for event in events:
            self.send_mail(
                subject=event.sent_message.results["subject"],
                message=event.sent_message.template,
                recipient_list=event.sent_message.results["recipient_list"]
            )
            event.status = StatusType.IN_PROCESS
            event.save()


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
