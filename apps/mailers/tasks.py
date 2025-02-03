from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.models import Q

from apps.backend_mailer.constants import BackendConstants
from apps.backend_mailer.crud.crud_email import CRUDEmail
from apps.mailers.constants import CampaignConstants
from apps.mailers.crud.crud_campaign import CRUDCampaign
from apps.sentry.sentry_scripts import SendToSentry
from apps.sentry.sentry_constants import SentryConstants

logger = get_task_logger(__name__)


@shared_task
def process_campaign():

    campaigns = CRUDCampaign.filter_campaign(
        Q(status=CampaignConstants.STATUS.started), fields=["status"]
    )
    for campaign in campaigns:
        try:
            is_ok = CRUDEmail.update_status(
                campaign.id, status=BackendConstants.STATUS.queued, is_campaign=True
            )
            logger.info(f"Successfully process email status for emails")
            if is_ok:
                CRUDCampaign.update_campaign_status(
                    object_id=campaign.id,
                    status=CampaignConstants.STATUS.sending,
                    is_campaign=True,
                )
                logger.info(
                    f"Successfully process campaign {campaign} status {campaign.status}"
                )
                return "SUCCESS"
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"process_campaign(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_CELERY_TASK,
                    "detail": f"Failed to process event {campaign.id}",
                    "extra_detail": f"{ex= }",
                }
            )
            logger.error(f"Failed to process campaign {campaign.id}: {ex}")
            CRUDCampaign.update_campaign_status(
                object_id=campaign.id, status=CampaignConstants.STATUS.error
            )
            return "FAILURE"
