import hashlib
import hmac
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.users.models.jwt import BlackListedAccessToken
from apps.users.serializers import (
    TokenSerializer,
    UserRegistrationSerializer,
    EmailTokenGenerationSerializer,
    UserDetailSerializer,
    RestorePasswordSerializer,
    TelegramAuthSerializer,
    UserUpdateSerializer,
)
from apps.users.services.jwt import create_one_time_jwt
from utils.permissions import IsOneTimeTokenValid, IsTokenValid
from utils.views import MultiSerializerViewSet
from apps.users.tasks import send_verification_email_task, send_one_time_jwt_task
from apps.sentry.sentry_scripts import SendToSentry
from apps.sentry.sentry_constants import SentryConstants


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
        except TokenError as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"LoginTokenView.login(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": "Can`t login to service Token error",
                    "extra_detail": f"{ex= }",
                }
            )
            logger.error(f"Can`t login to service Token error: {ex}")
            current_status = status.HTTP_401_UNAUTHORIZED
        except ValidationError as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"LoginTokenView.login(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": "Can`t login to service Validation error",
                    "extra_detail": f"{ex= }",
                }
            )
            logger.error(f"Can`t login to service Validation error: {ex}")
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"LoginTokenView.login(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": "Can`t login to service",
                    "extra_detail": f"{ex= }",
                }
            )
            logger.error(f"Can`t login to service: {ex}")
            current_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(serializer.validated_data, status=current_status)


class BlacklistTokenView(TokenBlacklistView, MultiSerializerViewSet):
    """
    Blacklists a given refresh token.
    This API allows authenticated users to logout by blacklisting their refresh token,
    effectively invalidating their access.
    """

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
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"BlacklistTokenView.logout(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": "Can`t logout (token error)",
                    "extra_detail": f"{ex= }",
                }
            )
            logger.error(f"Can`t logout (token error): {ex.args[0]}")
            return Response(
                "Can`t logout", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"BlacklistTokenView.logout(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": "Can`t logout",
                    "extra_detail": f"{ex= }",
                }
            )
            logger.error(f"Can`t logout: {ex}")
            return Response(
                "Can`t logout", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        context = serializer.validated_data
        context["logout"] = "success"
        return Response(context, status=status.HTTP_200_OK)


class RegistrationViewSet(MultiSerializerViewSet):
    """
    Registers a new user.
    Allows users to register a new account.
    Sends a verification email upon successful registration.
    """

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
                    context, _ = create_one_time_jwt(new_user)

                    if settings.CELERY_BROKER_URL:
                        send_verification_email_task.delay(
                            settings.DEFAULT_FROM_EMAIL,
                            data.get("email"),
                            context.get("access"),
                        )
                    else:
                        send_verification_email_task(
                            settings.DEFAULT_FROM_EMAIL,
                            data.get("email"),
                            context.get("access"),
                        )

        except ValidationError as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"BlacklistTokenView.logout(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": "Can`t logout (token error)",
                    "extra_detail": f"{ex= }",
                }
            )
            logger.error(f"Can`t logout (token error): {ex.args[0]}")
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(f"Can`t register a new user: {ex}")
            if isinstance(ex.args, tuple):
                result_error = []
                if isinstance(ex.args[0], str):
                    logger.error("Error: %s", ex.args[0])
                    return Response(
                        {"error": ex.args[0]},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                for errors in ex.args[0].values():
                    val = {}
                    for name, error in errors[0].items():
                        if isinstance(error, list):
                            val[name] = str(error[0])
                        elif isinstance(error, dict):
                            val[name] = str(error["error"])
                        else:
                            val[name] = str(error)
                    result_error.append(str(val))
                text = ", ".join(result_error)
            else:
                full_text = str(ex.detail)
                text = full_text.split("ErrorDetail(string='")[1].split("'")[0]
                logger.error("Error: %s", text)

            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"RegistrationViewSet.registration(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": "Can`t register a new user",
                    "extra_detail": f"{text= }",
                }
            )
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

        return Response(
            "Successfully regenerated the new JWT.", status=status.HTTP_200_OK
        )

    def _generate_access_token(self, user):
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return str(access)


class EmailVerificationView(MultiSerializerViewSet):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Email has been successfully verified",
                examples={"application/json": {"detail": "Email verified"}},
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Authentication error",
                examples={"application/json": {"error": "Invalid or missing token"}},
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Internal Server Error",
                examples={
                    "application/json": {
                        "error": "An error occurred during verification"
                    }
                },
            ),
        },
        operation_description=(
            "This endpoint verifies a user's email using a JWT token passed as a query parameter.\n\n"
            "**Example request :**"
            "`http://127.0.0.1:8000/api/1.0/users/email_verify/?token=your_token`\n\n"
            "Replace `your_token` with the actual token received."
        ),
    )
    @transaction.atomic
    def email_verify(self, request, *args, **kwargs):
        jwt_authenticator = JWTAuthentication()
        raw_token = request.GET.get("token")

        if raw_token is None:
            return Response(
                {"error": "Missing token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            validated_token = jwt_authenticator.get_validated_token(raw_token)
            user = jwt_authenticator.get_user(validated_token)
        except InvalidToken as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"EmailVerificationView.email_verify(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": f"Invalid token {raw_token=}",
                    "extra_detail": f"{ex= }",
                }
            )
            logger.error("Invalid token: %s", raw_token)
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"EmailVerificationView.email_verify(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": "An error occurred during verification",
                    "extra_detail": f"{ex= }",
                }
            )
            logger.error("An error occurred during verification: %s", ex)
            return Response(
                {"error": "An error occurred during verification"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        user.is_verified = True
        user.is_one_time_jwt_created = False
        user.save()
        return Response({"detail": "Email verified"}, status=status.HTTP_200_OK)


class UserViewSet(MultiSerializerViewSet):
    """
    Retrieves user details.
    Allows authenticated users to retrieve their own user details.
    Only authenticated users with a valid token can access this API.
    """

    queryset = User.objects.filter(is_active=True).all()
    serializers = {
        "retrieve": UserDetailSerializer,
        "partial_update": UserUpdateSerializer,
    }
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )

    parser_classes = None

    def get_parsers(self):
        if not self.request or getattr(self.request, "method", None) is None:
            return []
        if self.request.method in ("POST", "PATCH"):
            return [parser() for parser in (MultiPartParser, FormParser)]
        return [parser() for parser in (JSONParser,)]

    def retrieve(self, request, *args, **kwargs):
        """
        User`s view
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial user update.",
        operation_description="Partial user update.",
        request_body=UserUpdateSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class OneTimeJWTFunctionsViewSet(MultiSerializerViewSet):
    """
    Handles one-time JWT functions such as password restoration.
    Allows users with a valid one-time JWT to restore their password.
    Requires authentication with a valid one-time token.
    """

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


class RefreshTokenView(TokenRefreshView, MultiSerializerViewSet):
    """
    Refreshes an access token using a refresh token.
    This API allows clients to exchange a valid refresh token for a new access token,
    without requiring the user to re-authenticate.
    """

    authentication_classes = ()
    permission_classes = ()

    def refresh(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as ex:
            SendToSentry.send_scope_msg(
                scope_data={
                    "message": f"RefreshTokenView.refresh(): Ex",
                    "level": SentryConstants.SENTRY_MSG_ERROR,
                    "tag": SentryConstants.SENTRY_TAG_REQUEST,
                    "detail": f"Serializer doesn't valid {serializer=}",
                    "extra_detail": f"{ex= }",
                }
            )
            logger.error("Serializer doesn't valid: %s", ex)
            raise InvalidToken(ex.args[0])

        data = serializer.validated_data
        refresh = serializer.token_class(data["refresh"])

        data["user_id"] = refresh.payload["user_id"]

        return Response(data, status=status.HTTP_200_OK)


class TelegramLoginViewSet(MultiSerializerViewSet):
    """
    API ViewSet to authenticate users via Telegram login and return JWT tokens.
    """
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_description="Authenticate users via Telegram Login Widget and return JWT tokens.",
        request_body=TelegramAuthSerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "user_id": openapi.Schema(type=openapi.TYPE_INTEGER, title="User ID"),
                    "telegram_id": openapi.Schema(type=openapi.TYPE_INTEGER, title="Telegram ID"),
                    "telegram_username": openapi.Schema(type=openapi.TYPE_STRING, title="Telegram Username"),
                    "first_name": openapi.Schema(type=openapi.TYPE_STRING, title="First Name"),
                    "last_name": openapi.Schema(type=openapi.TYPE_STRING, title="Last Name"),
                    "email": openapi.Schema(type=openapi.TYPE_STRING, title="Email"),
                    "refresh": openapi.Schema(type=openapi.TYPE_STRING, title="Refresh Token"),
                    "access": openapi.Schema(type=openapi.TYPE_STRING, title="Access Token"),
                },
            ),
            400: openapi.Response("Bad Request"),
            403: openapi.Response("Forbidden (Invalid Hash)"),
            404: openapi.Response("User Not Found"),
        },
    )
    def create(self, request):
        bot_token = settings.TELEGRAM_BOT_TOKEN
        secret_key = hashlib.sha256(bot_token.encode()).digest()

        serializer = TelegramAuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        auth_data = serializer.validated_data
        received_hash = auth_data.pop("hash", None)

        data_check_string = "\n".join(f"{key}={value}" for key, value in sorted(auth_data.items()) if value is not None)
        expected_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        if expected_hash != received_hash:
            return Response({"error": "Invalid Telegram authentication (Hash mismatch)"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(telegram_username=auth_data.get("username"))
        except User.DoesNotExist:
            return Response({"error": "User not found. Please link your Telegram account in settings."},
                            status=status.HTTP_404_NOT_FOUND)

        token_serializer = TokenSerializer()
        refresh = token_serializer.get_token(user)

        response_data = {
            "user_id": user.id,
            "telegram_id": user.telegram_id,
            "telegram_username": user.telegram_username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response(response_data, status=status.HTTP_200_OK)
