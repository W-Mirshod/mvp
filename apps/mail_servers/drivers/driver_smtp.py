import smtplib
import logging

from constance import config
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.core.mail import EmailMessage, get_connection

from apps.mail_servers.drivers.base_driver import BaseDriver
from apps.mail_servers.models import SMTPServer
from apps.sentry.sentry_scripts import SendToSentry
from apps.sentry.sentry_constants import SentryConstants

logger = logging.getLogger(__name__)


class SMTPDriver(BaseDriver):

    @property
    def enable(self):
        return config.ENABLE_SMTP_SENDING

    def get_server_settings(self):
        try:
            settings = SMTPServer.objects.get(url=self.server_name, is_active=True)
        except SMTPServer.DoesNotExist as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"SMTPDriver.get_server_settings(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_GENERAL,
                    "detail": "Active SMTP config for the server not found",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error("Active SMTP config for the server not found")
            raise ObjectDoesNotExist("Active SMTP config for the server not found")
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
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"SMTPDriver.send_mail(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_GENERAL,
                    "detail": "Failed to send email",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error("Failed to send email: %s", ex)
            raise

    def check_connection(self):
        try:
            server = smtplib.SMTP(self.settings.url, self.settings.port)
            server.starttls() if self.settings.email_use_tls else None
            server.login(self.settings.username, self.settings.password)
            server.quit()
        except (ConnectionRefusedError, TimeoutError) as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"SMTPDriver.check_connection(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_GENERAL,
                    "detail": "Checking connection failed",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error("Checking connection failed: %s", ex)
            return False
        except smtplib.SMTPException as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"SMTPDriver.check_connection(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_GENERAL,
                    "detail": "SMTP server error occurred",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error("SMTP error occurred: %s", ex)
            return False
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"SMTPDriver.check_connection(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_GENERAL,
                    "detail": "Unexpected error occurred while checking connection",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error("Unexpected error occurred while checking connection: %s", ex)
            return False

        return True

    def login(self):
        try:
            server = smtplib.SMTP(self.settings.url, self.settings.port)
            server.starttls() if self.settings.email_use_tls else None
            response = server.login(self.settings.username, self.settings.password)
            server.quit()
            return response[0] == 235
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"SMTPDriver.login(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_GENERAL,
                    "detail": "Login failed",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error("Login failed: %s", ex)
            raise

    def logout(self):
        try:
            server = smtplib.SMTP(self.settings.url, self.settings.port)
            server.quit()
            return True
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"SMTPDriver.logout(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_GENERAL,
                    "detail": "Logout failed",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error("Logout failed: %s", ex)
            raise

    def send_message(self, subject, message, recipient):
        if not self.enable:
            logger.error("SMTP sending is disabled")
            raise ImproperlyConfigured("SMTP sending is disabled")

        self.send_mail(subject, message, [recipient])
