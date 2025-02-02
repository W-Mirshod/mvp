from celery.utils.log import get_task_logger
from apps.sentry.scripts.requests_logic import DiscordAlertLogic
from celery_scripts.celery_app import celery_app
from celery_scripts.constants import CeleryConstants

logger = get_task_logger(__name__)


@celery_app.task(
    name=f"{CeleryConstants.DATA_PROCESSING_TASK_PREFIX}_task.send_discord_alert",
    queue=CeleryConstants.DATA_PROCESSING_QUEUE,
    ignore_result=False,
)
def task_send_discord_alert(message: str, detail: str) -> bool:
    try:

        DiscordAlertLogic.send_msg_discord(msg=message, detail=detail)
    except Exception:
        return False
    logger.info(f"Done")

    return True
