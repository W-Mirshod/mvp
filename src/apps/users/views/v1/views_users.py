import logging

from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.serializers import TokenSerializer
from utils.views import MultiSerializerViewSet

logger = logging.getLogger(__name__)


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


class EmailVerificationView(GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        jwt_authenticator = JWTAuthentication()
        user_auth = jwt_authenticator.authenticate(request)

        if user_auth is None:
            return Response(
                {"detail": "Invalid or missing token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        user, token = user_auth
        user.is_verified = True
        user.save()
        return Response({"detail": "Email verified", "user_id": user.id}, status=status.HTTP_200_OK)
