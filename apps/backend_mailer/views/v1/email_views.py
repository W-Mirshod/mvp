import logging

from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

from apps.backend_mailer.serializers.email_serializers import (
    CreateEmailSerializer,
    RetrieveEmailSerializer,
)
from apps.backend_mailer.view_logic.email_qs import EmailQueryset
from utils.permissions import IsTokenValid, IsOwner
from utils.views import MultiSerializerViewSet

logger = logging.getLogger(__name__)

@method_decorator(name='list', decorator=swagger_auto_schema(operation_description="List sent messages"))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_description="Create a sent message"))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_description="Retrieve a sent message"))


class SentMessageView(MultiSerializerViewSet):
    queryset = None  # see get_queryset
    permission_classes = None  # see get_permissions
    serializers = {
        "list": RetrieveEmailSerializer,
        "create": CreateEmailSerializer,
        "retrieve": RetrieveEmailSerializer,
    }

    def get_queryset(self):
        logger.info(f"Getting queryset for user {self.request.user} with action {self.action}")
        return EmailQueryset.email_queryset(
            user_obj=self.request.user,
            action=self.action,
            kwargs=self.kwargs,
        )

    def get_permissions(self):
        logger.info(f"Getting permissions for action {self.action}")
        if self.action in ("list", "retrieve", "update", "partial_update", "destroy"):
            return [
                permission() for permission in (IsAuthenticated, IsTokenValid, IsOwner)
            ]
        else:
            return [permission() for permission in (IsAuthenticated, IsTokenValid)]        
    
    @swagger_auto_schema(
        operation_summary="List Sent Messages",
        operation_description="Retrieve a list of all sent messages."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Sent Message",
        operation_description="Create a new sent message."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Sent Message",
        operation_description="Retrieve a specific sent message."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Sent Message",
        operation_description="Update a sent message."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update Sent Message",
        operation_description="Partially update a sent message."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Sent Message",
        operation_description="Delete a sent message."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    