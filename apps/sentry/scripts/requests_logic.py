import logging
from typing import Dict

import requests
from requests import Response
from config.settings import DISCORD_ALERT

logger = logging.getLogger(__name__)


class DiscordAlertLogic:
    """Using requests lib"""

    @staticmethod
    def do_request(
        url: str,
        json_data: dict,
    ) -> tuple[bool, Response | None]:
        """tba"""

        connect_timeout = 10
        read_timeout = 10
        try:
            response_obj = requests.post(
                url=url,
                json=json_data,
                timeout=(connect_timeout, read_timeout),
            )
            logger.info("TEst sending ")
        except Exception:
            return False, None
        else:
            if response_obj is None:
                return False, None
            else:
                return True, response_obj

    @classmethod
    def send_msg_discord(cls, scope_data: Dict) -> None:
        if DISCORD_ALERT:
            message = scope_data.get("message")
            level = scope_data.get("level")
            tag = scope_data.get("tag")
            detail = scope_data.get("detail")
            extra_detail = scope_data.get("extra_detail")

            content = {
                "content": f"Message : {message}\n"
                f"Level: {level}\n"
                f"Tag: {tag}\n"
                f"Detail: {detail}\n"
                f"Extra detail: {extra_detail}"
            }

            cls.do_request(
                url=DISCORD_ALERT,
                json_data=content,
            )

            return
