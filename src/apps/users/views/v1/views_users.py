import logging

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.serializers import TokenSerializer, UserRegistrationSerializer
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


class LogoutViewSet(MultiSerializerViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TokenSerializer

    @transaction.atomic
    def logout(self, request, *args, **kwargs):
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

        access_token = serializer.validated_data["access"]
        refresh_token = serializer.validated_data["refresh"]
        current_user = request.user
        current_user.is_active = False
        current_user.save()
        OutstandingToken.objects.create(
            token=access_token,
            created_at=timezone.now(),
            expires_at=timezone.now() + timezone.timedelta(minutes=25),
            user=current_user,
            jti=refresh_token,
        )
        return Response(serializer.validated_data, status=current_status)
