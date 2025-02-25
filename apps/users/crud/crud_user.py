import logging

from apps.sentry.sentry_constants import SentryConstants
from apps.sentry.sentry_scripts import SendToSentry
from apps.users.models import User

logger = logging.getLogger(__name__)


class CRUDUser:
    @staticmethod
    async def async_user_exists(user_id: str) -> bool:
        try:
            return await User.objects.filter(id=user_id).aexists()
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"async_user_exists(): User.aget Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_DB_MODEL,
                    "detail": f"{user_id = }",
                    "extra_detail": f"{ex = }",
                }
            )
            return False
