from typing import Any, Dict

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty
from rest_framework.serializers import as_serializer_error
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from apps.users.models import User
from apps.users.models.tariffs import UserTariff
from utils import password_validation
from apps.sentry.sentry_scripts import SendToSentry
from apps.sentry.sentry_constants import SentryConstants

import logging


logger = logging.getLogger(__file__)


class TokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"TokenSerializer.validate(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": "KeyError",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error(f"KeyError in TokenSerializer.validate {ex=}")
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not self.user:
            return {"error": "Invalid credentials, try again"}
        if not self.user.is_active:
            return {"error": "Account disabled, contact admin"}
        if not self.user.is_verified:
            return {"error": "Email is not verified"}
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            return {"error": "Invalid user credentials"}

        refresh = self.get_token(self.user)

        data = {
            "user_id": self.user.id,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "telegram_username",
        )

    def validate_email(self, attr):
        if User.objects.filter(email=attr).exists():
            raise ValidationError(
                {"error": _("User with this e-mail already exists.")},
                code="invalid_email",
            )
        return attr

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            telegram_username=validated_data["telegram_username"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class UserTariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTariff
        fields = (
            "id",
            "tariff",
            "expired_at",
        )


class UserDetailSerializer(serializers.ModelSerializer):
    user_tariff = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "last_login",
            "is_superuser",
            "is_active",
            "date_joined",
            "email",
            "role",
            "position",
            "is_verified",
            "is_staff",
            "user_tariff",
            "telegram_username",
            "birth_date",
            "gender",
            "bio",
            "avatar",
        )

    def get_user_tariff(self, obj):
        user_tariffs = obj.tariff.all().order_by("-created_at")

        for user_tariff in user_tariffs:
            if user_tariff.expired_at > timezone.now():
                return UserTariffSerializer(user_tariff).data

        return None


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "role",
            "position",
            "telegram_username",
            "birth_date",
            "gender",
            "bio",
            "avatar",
        )


class RestorePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = User.objects.get(id=self.user_id)

        new_password = attrs["new_password"]
        if new_password:
            try:
                password_validation.validate_password(new_password, user)
            except ValidationError as exc:
                SendToSentry.send_scope_msg(
                    scope_data={
                        "message": f"RestorePasswordSerializer.validate(): Ex",
                        "level": SentryConstants.SENTRY_MSG_ERROR,
                        "tag": SentryConstants.SENTRY_TAG_REQUEST,
                        "detail": f"Password doesn't valid {new_password=}",
                        "extra_detail": f"{exc = }",
                    }
                )
                logger.error(f"Password doesn't valid {new_password=}")
                raise ValidationError(detail=as_serializer_error(exc))

        return super().validate(attrs)

    def run_validation(self, data=empty):
        self.user_id = data.get("user_id")
        return super().run_validation(data=data)


class EmailTokenGenerationSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

    def validate(self, attrs):
        user = self.check_existence_user_by_email(attrs)

        current_timezone = timezone.get_current_timezone()
        now = timezone.localtime(timezone.now(), current_timezone)

        self.check_pause(current_timezone, now, user)

        return user

    def check_existence_user_by_email(self, attrs, is_verified: bool = True):
        # checking the existence of the user
        try:
            user = User.objects.get(email=attrs["email"], is_verified=is_verified)
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"EmailTokenGenerationSerializer.check_existence_user_by_email(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": f"Invalid email",
                    "extra_detail": f"{ex = }",
                }
            )
            logger.error("Invalid email")
            raise ValidationError(
                {"error": _("Invalid email.")},
                code="invalid_email",
            )
        return user

    def check_pause(self, current_timezone, now, user):
        # checking the pause between OTP input
        jwt_max_out = (
            timezone.localtime(user.jwt_max_out, current_timezone)
            if user.jwt_max_out
            else user.jwt_max_out
        )
        if jwt_max_out and now < jwt_max_out:
            raise ValidationError(
                {"error": _("Max JWT try reached, try after an hour.")},
                code="invalid_otp",
            )

class TelegramAuthSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField(required=False, allow_null=True)
    username = serializers.CharField(required=False, allow_null=True)
    auth_date = serializers.IntegerField()
    hash = serializers.CharField()
