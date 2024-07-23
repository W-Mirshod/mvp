import logging
import imaplib


from constance import config
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.core.mail import EmailMessage, get_connection

from apps.mail_servers.models import ProxyServer

from .base_driver import BaseDriver

logger = logging.getLogger(__name__)


class ProxyDriver(BaseDriver):

    @property
    def enable(self):
        return config.ENABLE_PROXY_SENDING

    def get_server_settings(self):
        try:
            settings = ProxyServer.objects.get(url=self.server_name, is_active=True)
        except ProxyServer.DoesNotExist:
            logger.error("Active Proxy settings for the server not found")
            raise ObjectDoesNotExist("Active Proxy settings for the server not found")
        return settings

    def send_mail(self, subject, message, recipient_list):
        if not self.enable:
            logger.error("Proxy sending is disabled")
            raise ImproperlyConfigured("Proxy sending is disabled")

        try:
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
        except Exception as e:
            logger.error("Failed to send email: %s", e)
            raise

    def check_connection(self):
        try:
            client = imaplib.IMAP4_SSL(self.settings.hostname, self.settings.port)
            response, _ = client.login(self.settings.username, self.settings.password)
            client.logout()
        except (ConnectionRefusedError, TimeoutError) as e:
            logger.error("Checking connection failed: %s", e)
            return False
        except imaplib.IMAP4.error as e:
            logger.error("Proxy server error occurred: %s", e)
            return False
        except Exception as e:
            logger.error("Unexpected error occurred while checking connection: %s", e)
            return False

        if response == "OK":
            return True

        logger.error("Checking connection failed: %s", response)
        return False

    def login(self):
        try:
            client = imaplib.IMAP4_SSL(self.settings.hostname, self.settings.port)
            response, _ = client.login(self.settings.username, self.settings.password)
            client.logout()
            return response == "OK"
        except Exception as e:
            logger.error("Login failed: %s", e)
            raise

    def logout(self):
        try:
            client = imaplib.IMAP4_SSL(self.settings.hostname, self.settings.port)
            response, _ = client.logout()
            return response == "BYE"
        except Exception as e:
            logger.error("Logout failed: %s", e)
            raise

    def send_message(self, subject, message, recipient):
        if not self.enable:
            logger.error("Proxy sending is disabled")
            raise ImproperlyConfigured("Proxy sending is disabled")

        self.send_mail(subject, message, [recipient])
