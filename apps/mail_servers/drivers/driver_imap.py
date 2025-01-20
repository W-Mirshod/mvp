import imaplib
import logging

from constance import config
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.core.mail import EmailMessage, get_connection

from apps.mail_servers.drivers.base_driver import BaseDriver
from apps.mail_servers.models import IMAPServer
from apps.sentry.sentry_scripts import SendToSentry
from apps.sentry.sentry_constants import SentryConstants

logger = logging.getLogger(__name__)


class IMAPDriver(BaseDriver):

    @property
    def enable(self):
        return config.ENABLE_IMAP_SENDING

    def get_server_settings(self):
        try:
            settings = IMAPServer.objects.get(url=self.server_name, is_active=True)
        except IMAPServer.DoesNotExist as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"IMAPDriver.get_server_settings(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_GENERAL,
                    "detail": "Active IMAP config for the server not found",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error("Active IMAP config for the server not found")
            raise ObjectDoesNotExist("Active IMAP config for the server not found")
        return settings

    def send_mail(self, subject, message, recipient_list):
        if not self.enable:
            logger.error("IMAP sending is disabled")
            raise ImproperlyConfigured("IMAP sending is disabled")

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
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"IMAPDriver.send_mail(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_GENERAL,
                    "detail": "Failed to send email",
                    "extra_detail": f"{e = }",
                }
            )
            logger.error("Failed to send email: %s", e)
            raise

    def check_connection(self):
        try:
            client = imaplib.IMAP4_SSL(self.settings.url, self.settings.port)
            response, _ = client.login(self.settings.username, self.settings.password)
            client.logout()
        except (ConnectionRefusedError, TimeoutError) as e:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"IMAPDriver.check_connection(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_GENERAL,
                    "detail": "Checking connection failed",
                    "extra_detail": f"{e = }",
                }
            )
            logger.error("Checking connection failed: %s", e)
            return False
        except imaplib.IMAP4.error as e:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"IMAPDriver.check_connection(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_GENERAL,
                    "detail": "IMAP error occurred",
                    "extra_detail": f"{e = }",
                }
            )
            logger.error("IMAP error occurred: %s", e)
            return False
        except Exception as e:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"IMAPDriver.check_connection(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_GENERAL,
                    "detail": "Unexpected error occurred while checking connection",
                    "extra_detail": f"{e = }",
                }
            )
            logger.error("Unexpected error occurred while checking connection: %s", e)
            return False

        if response == "OK":
            return True

        logger.error("Checking connection failed: %s", response)
        return False

    def login(self):
        try:
            client = imaplib.IMAP4_SSL(self.settings.url, self.settings.port)
            response, _ = client.login(self.settings.username, self.settings.password)
            client.logout()
            return response == "OK"
        except Exception as e:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"IMAPDriver.login(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_GENERAL,
                    "detail": "Login failed",
                    "extra_detail": f"{e = }",
                }
            )
            logger.error("Login failed: %s", e)
            raise

    def logout(self):
        try:
            client = imaplib.IMAP4_SSL(self.settings.url, self.settings.port)
            response, _ = client.logout()
            return response == "BYE"
        except Exception as e:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"IMAPDriver.logout(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_GENERAL,
                    "detail": "Logout failed",
                    "extra_detail": f"{e = }",
                }
            )
            logger.error("Logout failed: %s", e)
            raise

    def send_message(self, subject, message, recipient):
        if not self.enable:
            logger.error("IMAP sending is disabled")
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"IMAPDriver.send_message(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_GENERAL,
                    "detail": "IMAP sending is disabled",
                    "extra_detail": f"",
                }
            )
            raise ImproperlyConfigured("IMAP sending is disabled")

        self.send_mail(subject, message, [recipient])
