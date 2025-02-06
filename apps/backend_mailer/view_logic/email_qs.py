import logging

from django.db.models import Q, QuerySet

from apps.sentry.sentry_constants import SentryConstants
from apps.sentry.sentry_scripts import SendToSentry
from apps.backend_mailer.models import Email
from apps.users.models import User


logger = logging.getLogger(__name__)


class EmailQueryset:
    @classmethod
    def email_queryset(
        cls,
        user_obj: User,
        action: str,
        kwargs: dict,
    ) -> list[Email]:
        """
        Swagger:
        - Retrieves a queryset of Email objects filtered according to user and action.
        - Uses ordering and select_related to optimize the query.
        - Captures and reports exceptions via Sentry.
        """

        query, order_by = cls.queryset(user_obj=user_obj, action=action, kwargs=kwargs)
        emails_qs = cls.filter_email(query, order_by)

        return emails_qs

    @staticmethod
    def queryset(
        user_obj: User,
        action: str,
        kwargs: dict,
    ) -> tuple[Q, list[str]]:
        """tba"""

        order_by = [
            "-created",
            "status",
        ]

        if action == "retrieve":
            email_id = kwargs.get("pk")
            if email_id is None or not email_id:
                return Q(id=None), order_by

            query = Q(
                id=email_id,
                author_id=user_obj.id,
            )
        else:
            query = Q(
                author_id=user_obj.id,
            )

        return query, order_by

    @staticmethod
    def filter_email(query: Q, order_by: list[str]) -> QuerySet[Email] | list:
        try:
            return (
                Email.objects.filter(query)
                .order_by(*order_by)
                .select_related(
                    "author",
                )
            )
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"EmailQueryset.filter_email(): Email.filter Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"{query = }",
                    "extra_detail": f"{ex = }",
                }
            )
            return []
