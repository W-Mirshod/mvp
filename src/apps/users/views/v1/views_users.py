import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.serializers import TokenSerializer, UserRegistrationSerializer
from apps.users.tasks import send_verification_email_task
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
        except TokenError as e:
            current_status = status.HTTP_401_UNAUTHORIZED
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Can`t login to service: {e}")
            current_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if "error" in serializer.validated_data.keys():
            current_status = status.HTTP_401_UNAUTHORIZED
        return Response(serializer.validated_data, status=current_status)


class RegistrationViewSet(ModelViewSet):
    queryset = User.objects.none()
    serializer_class = UserRegistrationSerializer
    authentication_classes = []
    permission_classes = []
    http_method_names = [
        "post",
    ]

    def registration(self, request, *args, **kwargs):
        try:
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

                if settings.CELERY_BROKER_URL:
                    send_verification_email_task.delay(
                        settings.DEFAULT_FROM_EMAIL,
                        data.get("email"),
                        self._generate_access_token(new_user),
                    )
                else:
                    send_verification_email_task(
                        settings.DEFAULT_FROM_EMAIL,
                        data.get("email"),
                        self._generate_access_token(new_user),
                    )

                response = Response({"status": "Ok"}, status=status.HTTP_201_CREATED)

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
        logger.info(f'Crated a new user (email:{data.get("email")})')
        return response

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
