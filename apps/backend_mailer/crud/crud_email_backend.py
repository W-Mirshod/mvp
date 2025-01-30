from apps.backend_mailer.models import EmailBackend
from apps.sentry.sentry_scripts import SendToSentry
from apps.sentry.sentry_constants import SentryConstants


class CRUDEmailBackend:
    @staticmethod
    def get_email_backend_by_id(
        obj_id: int, with_fk: bool = False
    ) -> EmailBackend | None:
        try:
            if with_fk:
                return (
                    EmailBackend.objects.filter(id=obj_id)
                    .select_related(
                        "author",
                    )
                    .first()
                )
            else:
                return EmailBackend.objects.get(id=obj_id)
        except EmailBackend.DoesNotExist:
            return None
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"CRUDEmailBackend.get_email_backend_by_id(): EmailBackend.get Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"{obj_id = }",
                    "extra_detail": f"{ex = }",
                }
            )
            return None
