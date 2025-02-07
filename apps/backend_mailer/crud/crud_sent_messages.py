import logging
from typing import List

from apps.sentry.sentry_constants import SentryConstants
from apps.sentry.sentry_scripts import SendToSentry
from apps.backend_mailer.models import SentMessages

logger = logging.getLogger(__name__)


class CRUDSentMessages:
    @staticmethod
    def get_sent_messages_by_id(
        obj_id: str,
        with_fk: bool = False,
    ) -> SentMessages | None:
        try:
            if with_fk:
                return (
                    SentMessages.objects.filter(id=obj_id)
                    .select_related(
                        "email",
                    )
                    .first()
                )
            else:
                return SentMessages.objects.get(id=obj_id)

        except SentMessages.DoesNotExist:
            logger.error(f"Failed get sent messages  by id messages does not exist")
            return None

        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"CRUDSentMessages.get_sent_messages_by_id(): SentMessages.get Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"{obj_id = }",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error(f"Failed get sent messages by id by id: {ex}")
            return None

    @staticmethod
    def update_status(object_id: int | List[SentMessages], status: str) -> int | None:
        try:
            is_ok = SentMessages.objects.filter(id__in=object_id).update(status=status)
            logger.info(
                f"Updated {is_ok} sent messages for messages ID {object_id} to status '{status}'."
            )
            return is_ok
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"CRUDSentMessages.update_status(): SentMessages.update Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"Object id {object_id = }",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error(f"Failed to update sent messages: {ex}")
            return None

    @staticmethod
    def bulk_sent_messages_create(
        create_objects: List[SentMessages], batch_size: int = 1000
    ) -> bool | None:
        if not create_objects:
            return None
        try:
            total_objects = len(create_objects)
            for i in range(0, total_objects, batch_size):
                batch = create_objects[i : i + batch_size]
                SentMessages.objects.bulk_create(objs=batch, batch_size=batch_size)
                logger.info(
                    f"Created {len(batch)} sent messages (batch {i // batch_size + 1})."
                )
            logger.info(
                f"Successfully created {total_objects} sent messages in batches of {batch_size}."
            )
            return True
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"CRUDSentMessages.bulk_sent_messages_create(): SentMessages.bulk_create Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"Error during create sent messages {create_objects = }",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error(f"Failed to create sent messages: {ex}")
            return False

    @staticmethod
    def bulk_sent_messages_update(
        update_objects: List[SentMessages], batch_size: int = 1000
    ) -> bool | None:
        if not update_objects:
            return None
        try:
            total_objects = len(update_objects)
            for i in range(0, total_objects, batch_size):
                batch = update_objects[i : i + batch_size]
                SentMessages.objects.bulk_update(
                    objs=batch,
                    batch_size=batch_size,
                    fields=("status",),
                )
                logger.info(
                    f"Updated {len(batch)} sent messages (batch {i // batch_size + 1})."
                )
            logger.info(
                f"Successfully updated {total_objects} sent messages in batches of {batch_size}."
            )
            return True
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"CRUDSentMessages.bulk_sent_messages_update(): SentMessages.bulk_update Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"Error during update sent messages {update_objects = }",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error(f"Failed to update sent messages: {ex}")
            return False
