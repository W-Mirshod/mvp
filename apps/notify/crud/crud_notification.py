from apps.sentry.sentry_scripts import SendToSentry
from apps.sentry.sentry_constants import SentryConstants
from apps.notify.models import Notification
from apps.websocket.socket_scripts.consumers import ChatConsumer
from asgiref.sync import async_to_sync


class CRUDNotification:

    @staticmethod
    def create_notification(data: dict) -> Notification | None:
        try:
            user_id = data.get("user_id")
            title = data.get("title")
            description = data.get("description")

            obj = Notification(
                user_id=user_id,
                title=title,
                description=description,
                notify_type=data.get("notify_type"),
                data=data.get("data"),
            )
            obj.save()

            notification_date = {
                "notification_id": obj.id,
                "title": title,
                "description": description,
            }

            async_to_sync(ChatConsumer.send_ws_msg)(
                group_name=f"user_{user_id}",
                data=notification_date,
                msg_type="notification",
            )

        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"create_notification(): save Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_PROCESSING,
                    "detail": f"",
                    "extra_detail": f"{ex = }",
                }
            )
            return None

        return obj
