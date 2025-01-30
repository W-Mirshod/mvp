import logging
from typing import List

from apps.sentry.sentry_constants import SentryConstants
from apps.sentry.sentry_scripts import SendToSentry
from apps.backend_mailer.models import Email

logger = logging.getLogger(__name__)


class CRUDEmail:
    @staticmethod
    def get_email_by_id(
        obj_id: str,
        with_fk: bool = False,
    ) -> Email | None:
        try:
            if with_fk:
                return (
                    Email.objects.filter(id=obj_id)
                    .select_related(
                        "author",
                    )
                    .first()
                )
            else:
                return Email.objects.get(id=obj_id)

        except Email.DoesNotExist:
            logger.error(f"Failed get email by id email does not exist")
            return None

        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"CRUDEmail.get_email_by_id(): Email.get Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"{obj_id = }",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error(f"Failed get email by id: {ex}")
            return None

    @staticmethod
    def update_status(
        object_id: int | List[Email], status: str, is_campaign=False
    ) -> int | None:
        try:
            if is_campaign:
                is_ok = Email.objects.filter(campaign__id=object_id).update(
                    status=status
                )
                logger.info(
                    f"Updated {is_ok} emails for campaign ID {object_id} to status '{status}'."
                )
            else:
                is_ok = Email.objects.filter(id__in=object_id).update(status=status)
                logger.info(
                    f"Updated {is_ok} emails for email ID {object_id} to status '{status}'."
                )
            return is_ok
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"CRUDEmail.update_status(): Email.update Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"Object id {object_id = }",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error(f"Failed to update emails: {ex}")
            return None

    @staticmethod
    def bulk_email_create(
        create_objects: List[Email], batch_size: int = 1000
    ) -> bool | None:
        if not create_objects:
            return None
        try:
            total_objects = len(create_objects)
            for i in range(0, total_objects, batch_size):
                batch = create_objects[i : i + batch_size]
                Email.objects.bulk_create(objs=batch, batch_size=batch_size)
                logger.info(
                    f"Created {len(batch)} emails (batch {i // batch_size + 1})."
                )
            logger.info(
                f"Successfully created {total_objects} emails in batches of {batch_size}."
            )
            return True
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"CRUDEmail.bulk_email_create(): Email.bulk_create Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"Error during create emails {create_objects = }",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error(f"Failed to create emails: {ex}")
            return False

    @staticmethod
    def bulk_email_update(
        update_objects: List[Email], batch_size: int = 1000
    ) -> bool | None:
        if not update_objects:
            return None
        try:
            total_objects = len(update_objects)
            for i in range(0, total_objects, batch_size):
                batch = update_objects[i : i + batch_size]
                Email.objects.bulk_update(
                    objs=batch,
                    batch_size=batch_size,
                    fields=("status", "scheduled_time", "number_of_retries"),
                )
                logger.info(
                    f"Updated {len(batch)} emails (batch {i // batch_size + 1})."
                )
            logger.info(
                f"Successfully updated {total_objects} emails in batches of {batch_size}."
            )
            return True
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"CRUDEmail.bulk_email_update(): Email.bulk_update Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"Error during create emails {update_objects = }",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error(f"Failed to update emails: {ex}")
            return False
