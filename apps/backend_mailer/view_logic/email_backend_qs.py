import logging

from django.db.models import Q, QuerySet

from apps.sentry.sentry_constants import SentryConstants
from apps.sentry.sentry_scripts import SendToSentry
from apps.backend_mailer.models import EmailBackend
from apps.users.models import User


logger = logging.getLogger(__name__)


class EmailBackendQueryset:
    @classmethod
    def email_backend_queryset(
        cls,
        user_obj: User,
        action: str,
        kwargs: dict,
    ) -> list[EmailBackend]:
        """
        Swagger:
        - Returns a filtered list of EmailBackend objects based on the provided user and action.
        - Implements ordering and prefetching for efficient database retrieval.
        - Exceptions are logged and sent to Sentry for monitoring.
        """

        query, order_by = cls.queryset(user_obj=user_obj, action=action, kwargs=kwargs)
        email_backends = cls.filter_email_backends(query, order_by)

        return email_backends

    @staticmethod
    def queryset(
        user_obj: User,
        action: str,
        kwargs: dict,
    ) -> tuple[Q, list[str]]:
        """tba"""

        order_by = [
            "-created_at",
            "backend_type",
        ]

        if action == "retrieve":
            email_backend_id = kwargs.get("pk")
            if email_backend_id is None or not email_backend_id:
                return Q(id=None), order_by

            query = Q(
                id=email_backend_id,
                author_id=user_obj.id,
            )
        else:
            query = Q(
                author_id=user_obj.id,
            )

        return query, order_by

    @staticmethod
    def filter_email_backends(
        query: Q, order_by: list[str]
    ) -> QuerySet[EmailBackend] | list:
        try:
            return (
                EmailBackend.objects.filter(query)
                .order_by(*order_by)
                .select_related(
                    "author",
                )
            )
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"EmailBackendQueryset.filter_email_backends(): EmailBackend.filter Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"{query = }",
                    "extra_detail": f"{ex = }",
                }
            )
            return []
