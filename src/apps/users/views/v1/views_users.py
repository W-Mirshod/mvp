import logging

from django.contrib.auth import get_user_model
from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny


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

class RefreshTokenView(TokenRefreshView, MultiSerializerViewSet):
    authentication_classes = ()
    permission_classes = [AllowAny]

    def refresh(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        data = serializer.validated_data
        refresh = serializer.token_class(data["refresh"])

        data["user_id"] = refresh.payload["user_id"]

        return Response(data, status=status.HTTP_200_OK)


