from health_check.backends import BaseHealthCheckBackend
from rest_framework.reverse import reverse_lazy
from rest_framework import status

from apps.sentry.sentry_constants import SentryConstants
from apps.sentry.sentry_scripts import SendToSentry
from config.settings import MAIN_HOST
import requests


class CampaignHealthCheck(BaseHealthCheckBackend):
    """
    Health check backend for Campaign API.
    Verifies that the Campaign API is accessible and returns the expected status code.
    This check ensures the basic functionality of the Campaign API.
    """

    critical_service = False

    def check_status(self) -> bool:
        try:
            url = MAIN_HOST + reverse_lazy("campaign_api:campaign_list")
            response = requests.get(url=url, timeout=5)

            if response.status_code != status.HTTP_401_UNAUTHORIZED:
                raise Exception(f"Unexpected status code: {response.status_code}")

            return True
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"SentMessagesHealthCheck.check_status: Exception",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": f"Sent messages API health check failed",
                    "extra_detail": str(ex),
                }
            )
            self.add_error(str(ex))
            return False

    def identifier(self):
        return self.__class__.__name__
