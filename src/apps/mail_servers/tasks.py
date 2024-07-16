from celery import shared_task
from celery.utils.log import get_task_logger
from apps.mailers.models import Event
from apps.mailers.choices import StatusType
from apps.mail_servers.drivers import SMTPDriver, IMAPDriver
from django.core.exceptions import ObjectDoesNotExist




logger = get_task_logger(__name__)


@shared_task
def test_periodic_task():
    logger.info("The periodic task is running.")
    return "Periodic task executed"


@shared_task
def process_events():
    events = Event.objects.select_related('server').filter(status=StatusType.NEW).only('server__type', 'sent_message')

    for event in events:
        try:
            driver = None
            if event.server.type == 'SMTP':
                driver = SMTPDriver(event.server.url)
            elif event.server.type == 'IMAP':
                driver = IMAPDriver(event.server.url)

            if driver and driver.enable:
                event.status = StatusType.IN_PROCESS
                event.save()

                driver.send_mail(
                    subject=event.sent_message.template,
                    message=event.sent_message.results.get('message', ''),
                    recipient_list=[event.sent_message.user.email]
                )
            else:
                event.status = StatusType.FAILED
                event.save()
        except ObjectDoesNotExist:
            logger.error(f"Server settings not found for event {event.id}")
            event.status = StatusType.FAILED
            event.save()
        except Exception as e:
            logger.error(f"Failed to process event {event.id}: {e}")
            event.status = StatusType.FAILED
            event.save()
