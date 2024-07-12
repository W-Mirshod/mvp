from celery import shared_task
from celery.utils.log import get_task_logger
from apps.mail_servers.models.models_servers import Server
from apps.mail_servers.drivers import SMTPDriver, IMAPDriver, ProxyDriver
from apps.mail_servers.choices import ServerType
from apps.mailers.choices import StatusType


logger = get_task_logger(__name__)


@shared_task
def test_periodic_task():
    logger.info("The periodic task is running.")
    return "Periodic task executed"


@shared_task
def process_mail_queue(status):
    servers = Server.objects.filter(is_active=True)
    for server in servers:
        if server.type == ServerType.SMTP:
            driver = SMTPDriver(server.url)
        elif server.type == ServerType.IMAP:
            driver = IMAPDriver(server.url)
        elif server.type == ServerType.PROXY:
            driver = ProxyDriver(server.url)
        else:
            continue

        try:
            driver.process_queue(status)
            logger.info(f"Processed queue for server {server.url} with status {status}")
        except Exception as e:
            logger.error(f"Error processing queue for server {server.url}: {e}")
            return "FAILURE"

    return "SUCCESS"


@shared_task
def process_new_mail_queue():
    return process_mail_queue(StatusType.NEW)


@shared_task
def process_in_process_mail_queue():
    return process_mail_queue(StatusType.IN_PROCESS)
