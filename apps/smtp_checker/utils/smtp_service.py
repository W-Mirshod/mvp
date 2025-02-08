import smtplib
import imaplib
import requests
import time
import logging
from celery import shared_task
from apps.smtp_checker.models.models import (
    SMTPCheckerTask,
    SMTPCheckerTaskResult,
    SMTPCheckerSettings,
)

logger = logging.getLogger(__name__)


@shared_task
def check_server_task(task_id, settings_id):
    """
    Runs the appropriate check (SMTP, IMAP, Proxy) based on the server type for a given task.
    Applies settings for timeout, retries, etc.
    """

    task = SMTPCheckerTask.objects.get(id=task_id)
    settings = SMTPCheckerSettings.objects.get(id=settings_id)
    task.status = "in_progress"
    task.save()

    for server in task.servers.all():
        result = "failure"
        error_message = None
        response_time = None

        try:
            if server.type.lower() == "smtp":
                response_time = check_smtp(server, settings)

            elif server.type.lower() == "imap":
                response_time = check_imap(server, settings)

            elif server.type.lower() == "proxy":
                response_time = check_proxy(server, settings)

            else:
                raise ValueError(f"Unknown server type: {server.type}")

            result = "success"

        except Exception as e:
            error_message = str(e)
            logger.error(
                f"Task {task_id}: Error checking {server.type.upper()} server ({server.url}): {error_message}"
            )

        SMTPCheckerTaskResult.objects.create(
            task=task,
            server=server,
            result=result,
            response_time=response_time,
            error_message=error_message,
        )

    task.status = "completed"
    task.save()


def check_smtp(server, settings):
    """Checks an SMTP server connection with user-defined settings."""
    start_time = time.time()
    attempt = 0
    success = False

    while attempt < settings.attempts_for_sending_count:
        try:
            smtp = smtplib.SMTP(
                server.url, server.port, timeout=settings.connection_timeout
            )

            if server.email_use_tls:
                smtp.starttls()

            smtp.login(server.username, server.password)
            smtp.quit()

            success = True
            break
        except Exception as e:
            attempt += 1
            if attempt >= settings.attempts_for_sending_count:
                raise e

    return round(time.time() - start_time, 3) if success else None


def check_imap(server, settings):
    """Checks an IMAP server connection with user-defined settings."""
    start_time = time.time()
    attempt = 0
    success = False

    while attempt < settings.attempts_for_sending_count:
        try:
            imap = imaplib.IMAP4_SSL(server.url, server.port)
            imap.login(server.username, server.password)
            imap.logout()

            success = True
            break
        except Exception as e:
            attempt += 1
            if attempt >= settings.attempts_for_sending_count:
                raise e

    return round(time.time() - start_time, 3) if success else None


def check_proxy(server, settings):
    """Checks a Proxy server with user-defined settings."""
    start_time = time.time()
    attempt = 0
    success = False

    while attempt < settings.attempts_for_sending_count:
        try:
            proxy_url = (
                f"http://{server.username}:{server.password}@{server.url}:{server.port}"
            )
            response = requests.get(
                "https://www.google.com",
                proxies={"http": proxy_url, "https": proxy_url},
                timeout=settings.connection_timeout,
            )

            if response.status_code != 200:
                raise Exception(f"Proxy returned status code {response.status_code}")

            success = True
            break
        except Exception as e:
            attempt += 1
            if attempt >= settings.attempts_for_sending_count:
                raise e

    return round(time.time() - start_time, 3) if success else None
