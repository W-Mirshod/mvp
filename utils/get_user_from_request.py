import logging

from apps.sentry.sentry_scripts import SendToSentry
from apps.sentry.sentry_constants import SentryConstants
from apps.users.models import User

logger = logging.getLogger(__name__)


class RequestContext:
    @staticmethod
    def get_user_from_request(context: dict) -> User | None:
        try:
            return context.get("request").user
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"get_user_from_request(): context Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": f"",
                    "extra_detail": f"{ex = }",
                }
            )
            return None
