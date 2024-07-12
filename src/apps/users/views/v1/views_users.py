import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView

from apps.users.models.jwt import BlackListedAccessToken
from apps.users.serializers import (
    EmailTokenGenerationSerializer,
    RestorePasswordSerializer,
    TokenSerializer,
    UserDetailSerializer,
    UserRegistrationSerializer,
)
from apps.users.services.jwt import create_one_time_jwt
from apps.users.tasks import send_one_time_jwt_task, send_verification_email_task
from utils.permissions import IsOneTimeTokenValid, IsTokenValid
from utils.views import MultiSerializerViewSet

logger = logging.getLogger(__name__)
User = get_user_model()


class LoginTokenView(TokenObtainPairView, MultiSerializerViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = TokenSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Schema(
                title="User`s token",
                type=openapi.TYPE_OBJECT,
                properties={
                    "user_id": openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        title="User`s ID",
                        readOnly=True,
                    ),
                    "refresh": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        title="Refresh token",
                        readOnly=True,
                    ),
                    "access": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        title="Access token",
                        readOnly=True,
                    ),
                },
            ),
        }
    )
    @transaction.atomic
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        current_status = status.HTTP_200_OK

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            current_status = status.HTTP_401_UNAUTHORIZED
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Can`t login to service: {e}")
            current_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if "error" in serializer.validated_data.keys():
            current_status = status.HTTP_401_UNAUTHORIZED
        return Response(serializer.validated_data, status=current_status)


class BlacklistTokenView(TokenBlacklistView, MultiSerializerViewSet):
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = (IsAuthenticated,)

    def logout(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            with transaction.atomic():
                serializer.is_valid(raise_exception=True)
                refresh_token = OutstandingToken.objects.filter(
                    token=request.data.get("refresh")
                ).first()
                BlackListedAccessToken.objects.create(
                    jti=request.auth.payload.get("jti"),
                    jti_refresh=refresh_token.jti,
                    token=request.auth,
                    user=request.user,
                    created_at=refresh_token.created_at,
                    expires_at=refresh_token.expires_at,
                )

        except TokenError as ex:
            logger.error(f"Can`t logout (token error): {ex.args[0]}")
            return Response("Can`t logout", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            logger.error(f"Can`t logout: {ex}")
            return Response("Can`t logout", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        context = serializer.validated_data
        context["logout"] = "success"
        return Response(context, status=status.HTTP_200_OK)


class RegistrationViewSet(MultiSerializerViewSet):
    queryset = User.objects.none()
    serializers = {
        "registration": UserRegistrationSerializer,
        "get_one_time_jwt": EmailTokenGenerationSerializer,
    }
    authentication_classes = []
    permission_classes = []
    http_method_names = [
        "post",
    ]

    def registration(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                # check of input data
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data

                # create user
                response = super().create(request, *args, **kwargs)
                if response.status_code == status.HTTP_201_CREATED:
                    new_user = User.objects.get(email=response.data["email"])
                    new_user.is_active = True
                    new_user.save()
                    token = create_one_time_jwt(new_user)

                    if settings.CELERY_BROKER_URL:
                        send_verification_email_task.delay(
                            settings.DEFAULT_FROM_EMAIL,
                            data.get("email"),
                            token,
                        )
                    else:
                        send_verification_email_task(
                            settings.DEFAULT_FROM_EMAIL,
                            data.get("email"),
                            token,
                        )

        except ValidationError as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(f"Can`t register a new user: {ex}")
            if isinstance(ex.args, tuple):
                text = ", ".join([str(e) for e in ex.args])
            else:
                full_text = str(ex.detail)
                text = full_text.split("ErrorDetail(string='")[1].split("'")[0]
            return Response({"error": text}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({"status": "Ok"}, status=status.HTTP_201_CREATED)
        logger.info(f'Crated a new user (email:{data.get("email")})')
        return response

    def get_one_time_jwt(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        context, _ = create_one_time_jwt(serializer.validated_data)

        if settings.CELERY_BROKER_URL:
            send_one_time_jwt_task.delay(
                settings.DEFAULT_FROM_EMAIL,
                request.data.get("email"),
                context.get("access"),
            )
        else:
            send_one_time_jwt_task(
                settings.DEFAULT_FROM_EMAIL,
                request.data.get("email"),
                context.get("access"),
            )

        return Response("Successfully regenerated the new JWT.", status=status.HTTP_200_OK)

    def _generate_access_token(self, user):
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return str(access)


class EmailVerificationView(MultiSerializerViewSet):
    authentication_classes = []
    permission_classes = []

    @transaction.atomic
    def email_verify(self, request, *args, **kwargs):
        jwt_authenticator = JWTAuthentication()
        raw_token = request.GET.get("token")

        if raw_token is None:
            return Response({"detail": "Missing token"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            validated_token = jwt_authenticator.get_validated_token(raw_token)
            user = jwt_authenticator.get_user(validated_token)
        except InvalidToken:
            return Response({"detail": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response(
                {"detail": "An error occurred during verification"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        user.is_verified = True
        user.save()
        return Response({"detail": "Email verified"}, status=status.HTTP_200_OK)


class UserViewSet(MultiSerializerViewSet):
    queryset = User.objects.filter(is_active=True).all()
    serializers = {
        "retrieve": UserDetailSerializer,
    }
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )

    def retrieve(self, request, *args, **kwargs):
        """
        User`s view
        """
        return super().retrieve(request, *args, **kwargs)


class OneTimeJWTFunctionsViewSet(MultiSerializerViewSet):
    queryset = User.objects.filter(is_active=True)
    serializers = {
        "restore_password": RestorePasswordSerializer,
    }
    permission_classes = (
        IsAuthenticated,
        IsOneTimeTokenValid,
    )
    http_method_names = [
        "patch",
    ]

    def restore_password(self, request):
        request.data["user_id"] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = request.user
        user.restore_password(data.get("new_password"))

        return Response(
            {"message": _("Successfully set a new password for the user.")},
            status=status.HTTP_200_OK,
        )
