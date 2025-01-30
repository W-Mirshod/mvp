import logging
from typing import List
from django.db.models import Q, QuerySet

from apps.sentry.sentry_constants import SentryConstants
from apps.sentry.sentry_scripts import SendToSentry
from apps.mailers.models import Campaign
from apps.backend_mailer.models import Email

logger = logging.getLogger(__name__)


class CRUDCampaign:
    @staticmethod
    def update_campaign_status(
        object_id: List[Email] | int, status: str, is_campaign=None
    ) -> int | None:
        try:
            if is_campaign:
                is_ok = Campaign.objects.filter(id=object_id).update(status=status)
            else:
                is_ok = Campaign.objects.filter(message_id__in=object_id).update(
                    status=status
                )
            logger.info(f"Successfully update campaigns status: {is_ok}")
            return is_ok
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"CRUDCampaign.update_campaign_status(): Campaign.update Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"Error during updating campaign by email ids {object_id = }",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error(f"Failed update campaigns status: {ex}", exc_info=True)
            return None

    @staticmethod
    def filter_campaign(
        query: Q, fields: List[str] = None
    ) -> QuerySet[Campaign] | list:
        try:
            if fields:
                is_ok = Campaign.objects.filter(query).only(*fields)
            else:
                is_ok = Campaign.objects.filter(query)

            logger.info(f"Successfully return filtered campaigns: {is_ok}")
            return is_ok
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"CRUDCampaign.filter_campaign(): Campaign..get Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"Error getting campaign by query and fields {query = } {fields=}",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error(f"Failed to filter campaigns: {ex}", exc_info=True)
            return []
