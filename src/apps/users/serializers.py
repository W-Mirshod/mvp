from typing import Any, Dict

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from .models import User, UserTariff


class TokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
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
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = (
            "email",
            "password",
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
            "last_login",
            "is_superuser",
            "is_active",
            "date_joined",
            "email",
            "is_verified",
            "is_staff",
            "user_tariff",
        )

    def get_user_tariff(self, obj):
        user_tariffs = obj.tariff.all().order_by("-created_at")

        for user_tariff in user_tariffs:
            if user_tariff.expired_at > timezone.now():
                return UserTariffSerializer(user_tariff).data

        return None
