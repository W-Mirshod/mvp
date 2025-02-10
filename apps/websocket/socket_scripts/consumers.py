import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    """Uses 'channel_layer.group_*' for Redis Channel Layer."""

    async def connect(self):
        """
        Get user ID from kwargs.
        If user exists - connect.
        """
        from apps.users.crud.crud_user import CRUDUser

        user_id = self.scope.get("url_route", {}).get("kwargs", {}).get("user_id", None)
        exists = await CRUDUser.async_user_exists(user_id)

        self.room_name = user_id
        self.room_group_name = f"user_{self.room_name}"

        if not exists:
            logger.warning(f"connect(): user does not exists; {user_id = }")
            await self.disconnect("tba")
            await self.close("tba")
            return None

        logger.info(f"connect(): {self.room_name = }")

        """Join room group"""
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        logger.debug(f"connect(): connection done")
        await self.accept()

    async def disconnect(self, close_code):
        """Leave room group"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    @staticmethod
    async def send_ws_msg(group_name: str, data: dict, msg_type: str) -> None:
        """Send message or notification to room group"""
        channel_layer = get_channel_layer()

        await channel_layer.group_send(
            group_name,
            {
                "type": f"chat.{msg_type}",
                "msg_data": data,
            },
        )
        # logger.debug(f"send_ws_msg(): {msg_type} sent to {group_name}; data = {data}")

    async def chat_message(self, event: dict):
        """Send message to WebSocket"""
        await self.send(
            text_data=json.dumps(
                {
                    "msg_data": event.get("msg_data"),
                    "type": "message",
                }
            )
        )

    # logger.debug(f"chat_message(): message sent; {event = }")

    async def chat_notification(self, event: dict):
        """Handles notifications"""
        await self.send(
            text_data=json.dumps(
                {
                    "notification_data": event.get("msg_data"),
                    "type": "notification",
                }
            )
        )
        # logger.debug(f"chat_notification(): notification sent; {event = }")
