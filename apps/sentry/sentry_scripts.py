import logging

from sentry_sdk import capture_message, push_scope
from apps.sentry.sentry_constants import SentryConstants
from apps.sentry.tasks import task_send_discord_alert
from config.settings import USE_SENTRY

logger = logging.getLogger(__name__)


class SendToSentry:
    @staticmethod
    def send_msg(msg: str, msg_lvl: str) -> None:
        """
        Usage:
            from apps.sentry.sentry_scripts import SendToSentry
            from apps.sentry.sentry_constants import SentryConstants
            SendToSentry.send_msg(msg="Test", msg_lvl=CoreConstants.SENTRY_MSG_ERROR)
        """
        if USE_SENTRY:
            capture_message(msg, level=msg_lvl)
        return None

    @staticmethod
    def send_scope_msg(scope_data: dict) -> None:
        """
        Usage:
            from apps.sentry.sentry_scripts import SendToSentry
            from apps.sentry.sentry_constants import SentryConstants

            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"Test_message",
                    "level": CoreConstants.SENTRY_MSG_ERROR,
                    "tag": CoreConstants.SENTRY_TAG_GENERAL,
                    "detail": f"Detail_text",
                    "extra_detail": f"Extra_detail",
                }
            )
        """
        message = scope_data.get("message")
        level = scope_data.get("level")
        tag = scope_data.get("tag")
        detail = scope_data.get("detail")
        extra_detail = scope_data.get("extra_detail")

        if USE_SENTRY:
            with push_scope() as scope:
                scope.set_tag(key="tag", value=tag)
                scope.set_extra(key="detail", value=detail)
                scope.set_extra(key="extra_detail", value=extra_detail)
                if level == SentryConstants.SENTRY_MSG_INFO:
                    scope.clear_breadcrumbs()
                capture_message(message=message, level=level)

            task_send_discord_alert.s(message=message, detail=detail).apply_async()

        else:
            """if debug"""
            logger_msg = f"{message} | {detail} | {extra_detail} | {tag}"

            if level == SentryConstants.SENTRY_MSG_DEBUG:
                logger.debug(logger_msg)
            elif level == SentryConstants.SENTRY_MSG_INFO:
                logger.info(logger_msg)
            elif level == SentryConstants.SENTRY_MSG_WARNING:
                logger.warning(logger_msg)
            else:
                logger.error(logger_msg)

        return None
