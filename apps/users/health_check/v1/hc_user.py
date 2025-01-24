from health_check.backends import BaseHealthCheckBackend
from rest_framework.reverse import reverse_lazy
from rest_framework import status

from apps.sentry.sentry_constants import SentryConstants
from apps.sentry.sentry_scripts import SendToSentry
from config.settings import MAIN_HOST
import requests


class UserHealthCheck(BaseHealthCheckBackend):

    critical_service = False

    def check_status(self) -> bool:
        try:
            url = f"{MAIN_HOST}{reverse_lazy('users_api:manage', kwargs={'pk': 1})}"
            response = requests.get(url=url, timeout=5)

            if response.status_code != status.HTTP_401_UNAUTHORIZED:
                raise Exception(f"Unexpected status code: {response.status_code}")

            return True
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"UserHealthCheck.check_status: Exception",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": f"user api health check failed",
                    "extra_detail": str(ex),
                }
            )
            self.add_error(str(ex))
            return False

    def identifier(self):
        return self.__class__.__name__
