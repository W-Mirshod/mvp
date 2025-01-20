from celery import shared_task
from celery.utils.log import get_task_logger

from django.core.exceptions import ObjectDoesNotExist

from apps.mail_servers.choices import ServerType
from apps.mail_servers.drivers.driver_imap import IMAPDriver
from apps.mail_servers.drivers.driver_proxy import ProxyDriver
from apps.mail_servers.drivers.driver_smtp import SMTPDriver
from apps.mail_servers.models.servers import Server
from apps.mailers.choices import StatusType
from apps.mailers.models.event import Event
from apps.sentry.sentry_scripts import SendToSentry
from apps.sentry.sentry_constants import SentryConstants


logger = get_task_logger(__name__)


def get_driver(server_type, server_url):
    if server_type == ServerType.SMTP:
        return SMTPDriver(server_url)
    elif server_type == ServerType.IMAP:
        return IMAPDriver(server_url)
    elif server_type == ServerType.PROXY:
        return ProxyDriver(server_url)
    return None


@shared_task
def test_periodic_task():
    logger.info("The periodic task is running.")
    return "Periodic task executed"


@shared_task
def process_events():
    events = (
        Event.objects.select_related("server")
        .filter(status=StatusType.NEW)
        .only("server__type", "sent_message")
    )

    for event in events:
        try:
            driver = get_driver(event.server.type, event.server.url)

            if driver and driver.enable:
                event.status = StatusType.IN_PROCESS
                event.save()

                driver.send_mail(
                    subject=event.sent_message.template,
                    message=event.sent_message.results.get("message", ""),
                    recipient_list=[event.sent_message.user.email],
                )
            else:
                event.status = StatusType.FAILED
                event.save()
        except ObjectDoesNotExist as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"process_events(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_CELERY_TASK,
                    "detail": f"Server settings not found for event {event.id}",
                    "extra_detail": f"{ex= }",
                }
            )
            logger.error(f"Server settings not found for event {event.id}")
            event.status = StatusType.FAILED
            event.save()
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"process_events(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_CELERY_TASK,
                    "detail": f"Failed to process event {event.id}",
                    "extra_detail": f"{ex= }",
                }
            )
            logger.error(f"Failed to process event {event.id}: {ex}")
            event.status = StatusType.FAILED
            event.save()


def process_mail_queue(status):
    servers = Server.objects.filter(is_active=True)
    for server in servers:
        driver = get_driver(server.type, server.url)
        if not driver:
            continue
        try:
            driver.process_queue(status)
            logger.info(f"Processed queue for server {server.url} with status {status}")
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"process_mail_queue(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_CELERY_TASK,
                    "detail": f"Error processing queue for server {server.url}",
                    "extra_detail": f"{ex= }",
                }
            )
            logger.error(f"Error processing queue for server {server.url}: {ex}")
            return "FAILURE"

    return "SUCCESS"


@shared_task
def process_new_mail_queue():
    return process_mail_queue(StatusType.NEW)


@shared_task
def process_in_process_mail_queue():
    return process_mail_queue(StatusType.IN_PROCESS)
