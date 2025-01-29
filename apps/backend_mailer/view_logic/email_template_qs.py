import logging

from django.db.models import Q, QuerySet

from apps.sentry.sentry_constants import SentryConstants
from apps.sentry.sentry_scripts import SendToSentry
from apps.backend_mailer.models import EmailTemplate
from apps.users.models import User


logger = logging.getLogger(__name__)


class EmailTemplateQueryset:
    @classmethod
    def email_template_queryset(
        cls,
        user_obj: User,
        action: str,
        kwargs: dict,
    ) -> list[EmailTemplate] | QuerySet[EmailTemplate]:
        """tba"""

        query, order_by = cls.queryset(user_obj=user_obj, action=action, kwargs=kwargs)
        email_templates_qs = cls.filter_email_templates(query, order_by)

        return email_templates_qs

    @staticmethod
    def queryset(
        user_obj: User,
        action: str,
        kwargs: dict,
    ) -> tuple[Q, list[str]]:
        """tba"""

        order_by = [
            "-created",
        ]

        if action == "retrieve":
            email_template_id = kwargs.get("pk")
            if email_template_id is None or not email_template_id:
                return Q(id=None), order_by

            query = Q(
                id=email_template_id,
                email_set__author_id=user_obj.id,
            )
        else:
            query = Q(
                email_set__author_id=user_obj.id,
            )

        return query, order_by

    @staticmethod
    def filter_email_templates(
        query: Q, order_by: list[str]
    ) -> QuerySet[EmailTemplate] | list:
        try:
            return (
                EmailTemplate.objects.filter(query)
                .order_by(*order_by)
                .select_related(
                    "email_set",
                )
            )
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"EmailTemplateQueryset.filter_email_templates(): EmailTemplate.filter Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"{query = }",
                    "extra_detail": f"{ex = }",
                }
            )
            return []
