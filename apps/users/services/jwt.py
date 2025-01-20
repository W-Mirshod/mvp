import logging

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from apps.sentry.sentry_scripts import SendToSentry
from apps.sentry.sentry_constants import SentryConstants


logger = logging.getLogger(__name__)

User = get_user_model()


def create_one_time_jwt(user: User) -> tuple[dict, str]:
    user.is_one_time_jwt_created = True

    try:
        with transaction.atomic():
            user.save()
            from ..serializers import TokenSerializer

            refresh = TokenSerializer(
                data={"username_field": user.USERNAME_FIELD}
            ).get_token(user)
    except Exception as ex:
        SendToSentry.send_scope_msg(
            scope_data={
                "message": f"create_one_time_jwt: Ex",
                "level": SentryConstants.SENTRY_MSG_ERROR,
                "tag": SentryConstants.SENTRY_TAG_GENERAL,
                "detail": "Error with generation JWT",
                "extra_detail": f"{ex = }",
            }
        )
        user.is_one_time_jwt_created = False
        user.save()
        return {"error": _("Error with generation JWT")}, status.HTTP_400_BAD_REQUEST
    context = {
        "access": str(refresh.access_token),
    }
    return context, status.HTTP_200_OK
