import smtplib
import logging

from constance import config
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.core.mail import EmailMessage, get_connection

from apps.mail_servers.models import SMTPServer

from .base_driver import BaseDriver

logger = logging.getLogger(__name__)


class SMTPDriver(BaseDriver):

    @property
    def enable(self):
        return config.ENABLE_SMTP_SENDING

    def get_server_settings(self):
        try:
            settings = SMTPServer.objects.get(url=self.server_name, is_active=True)
        except SMTPServer.DoesNotExist:
            logger.error("Active SMTP settings for the server not found")
            raise ObjectDoesNotExist("Active SMTP settings for the server not found")
        return settings

    def send_mail(self, subject, message, recipient_list):
        if not self.enable:
            logger.error("SMTP sending is disabled")
            raise ImproperlyConfigured("SMTP sending is disabled")

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
            with smtplib.SMTP(self.settings.hostname, self.settings.port) as client:
                if self.settings.use_tls:
                    client.starttls()
                client.login(self.settings.username, self.settings.password)
                client.quit()
                return True
        except (ConnectionRefusedError, TimeoutError) as e:
            logger.error("Checking connection failed: %s", e)
            return False
        except smtplib.SMTPException as e:
            logger.error("SMTP error occurred: %s", e)
            return False
        except Exception as e:
            logger.error("Unexpected error occurred while checking connection: %s", e)
            return False

    def login(self):
        try:
            with smtplib.SMTP(self.settings.hostname, self.settings.port) as client:
                if self.settings.use_tls:
                    client.starttls()
                response = client.login(self.settings.username, self.settings.password)
                client.quit()
                return response[0] == 235
        except Exception as e:
            logger.error("Login failed: %s", e)
            raise

    def logout(self):
        try:
            with smtplib.SMTP(self.settings.hostname, self.settings.port) as client:
                if self.settings.use_tls:
                    client.starttls()
                client.login(self.settings.username, self.settings.password)
                response = client.quit()
                return response[0] == 221
        except Exception as e:
            logger.error("Logout failed: %s", e)
            raise

    def send_message(self, subject, message, recipient):
        if not self.enable:
            logger.error("SMTP sending is disabled")
            raise ImproperlyConfigured("SMTP sending is disabled")

        self.send_mail(subject, message, [recipient])
