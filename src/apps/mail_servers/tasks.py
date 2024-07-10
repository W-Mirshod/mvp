from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def test_periodic_task():
    logger.info("The periodic task is running.")
    return "Periodic task executed"

