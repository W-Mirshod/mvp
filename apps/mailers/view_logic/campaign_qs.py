import logging

from django.db.models import Q, QuerySet

from apps.sentry.sentry_constants import SentryConstants
from apps.sentry.sentry_scripts import SendToSentry
from apps.mailers.models import Campaign
from apps.users.models import User


logger = logging.getLogger(__name__)


class CampaignQueryset:
    @classmethod
    def campaign_queryset(
        cls,
        user_obj: User,
        action: str,
        kwargs: dict,
    ) -> list[Campaign]:
        """tba"""

        query, order_by = cls.queryset(user_obj=user_obj, action=action, kwargs=kwargs)
        campaigns = cls.filter_campaigns(query, order_by)

        return campaigns

    @staticmethod
    def queryset(
        user_obj: User,
        action: str,
        kwargs: dict,
    ) -> tuple[Q, list[str]]:
        """tba"""

        order_by = [
            "-created_at",
            "status",
        ]

        if action == "retrieve":
            campaign_id = kwargs.get("pk")
            if campaign_id is None or not campaign_id:
                return Q(id=None), order_by

            query = Q(
                id=campaign_id,
                author_id=user_obj.id,
            )
        else:
            query = Q(
                author_id=user_obj.id,
            )

        return query, order_by

    @staticmethod
    def filter_campaigns(query: Q, order_by: list[str]) -> QuerySet[Campaign] | list:
        try:
            return (
                Campaign.objects.filter(query)
                .order_by(*order_by)
                .select_related(
                    "author",
                )
            )
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"CampaignQueryset.filter_campaigns(): Campaign.filter Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"{query = }",
                    "extra_detail": f"{ex = }",
                }
            )
            return []
