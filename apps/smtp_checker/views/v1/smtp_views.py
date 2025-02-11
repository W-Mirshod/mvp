from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from apps.smtp_checker.utils.smtp_service import check_server_task

from apps.smtp_checker.models.models import (
    SMTPCheckerSettings,
    SMTPCheckerTask,
    SMTPCheckerTaskResult,
)
from apps.smtp_checker.serializers.smtp_serializers import (
    SMTPCheckerSettingsSerializer,
    SMTPCheckerTaskSerializer,
    SMTPCheckerTaskResultSerializer,
)
from utils.permissions import IsTokenValid, IsOwner
from utils.views import MultiSerializerViewSet


class ServerCheckerSettingsAPIView(MultiSerializerViewSet):
    """
    API for managing server checker settings.
    Allows users to create, retrieve, update, and delete SMTP checker settings.
    Only authenticated users can access this API.
    """

    queryset = SMTPCheckerSettings.objects.all()
    serializer_class = SMTPCheckerSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SMTPCheckerSettings.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Ensure the user is set before saving"""
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """Set different permissions for different actions"""
        if self.action in ("list", "retrieve", "destroy"):
            return [
                permission() for permission in (IsAuthenticated, IsTokenValid, IsOwner)
            ]
        else:
            return [permission() for permission in (IsAuthenticated, IsTokenValid)]
    
    @swagger_auto_schema(
        operation_summary="List SMTP Settings",
        operation_description="Retrieve a list of all SMTP checker settings for the authenticated user."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create SMTP Settings",
        operation_description="Create new SMTP checker settings."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve SMTP Settings",
        operation_description="Retrieve specific SMTP checker settings."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update SMTP Settings",
        operation_description="Update SMTP checker settings."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update SMTP Settings",
        operation_description="Partially update SMTP checker settings."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete SMTP Settings",
        operation_description="Delete SMTP checker settings."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ServerCheckerTaskAPIView(MultiSerializerViewSet):
    """
    API for managing SMTP Checker tasks.
    Allows users to create and run SMTP checker tasks.
    Tasks are processed asynchronously.
    """

    queryset = SMTPCheckerTask.objects.all()
    serializer_class = SMTPCheckerTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SMTPCheckerTask.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Ensure the user is set before saving"""
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="Run SMTP Check Task",
        operation_description="Initiate an asynchronous SMTP server check task."
    )
    @action(detail=True, methods=["post"], url_path="run-task")
    def run_task(self, request, pk=None):
        """Runs the server check task asynchronously"""
        task = self.get_object()

        if task.status in ["in_progress", "completed"]:
            return Response(
                {"detail": "Task is already being processed or completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        check_server_task.delay(task.id, task.settings.id)

        return Response(
            {"detail": "Task has been queued for processing."},
            status=status.HTTP_200_OK,
        )
    
    @swagger_auto_schema(
        operation_summary="List SMTP Tasks",
        operation_description="Retrieve a list of all SMTP checker tasks."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create SMTP Task",
        operation_description="Create a new SMTP checker task."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve SMTP Task",
        operation_description="Retrieve a specific SMTP checker task."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update SMTP Task",
        operation_description="Update an SMTP checker task."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update SMTP Task",
        operation_description="Partially update an SMTP checker task."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete SMTP Task",
        operation_description="Delete an SMTP checker task."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ServerCheckerTaskResultAPIView(MultiSerializerViewSet):
    """
    API for retrieving server checker results (SMTP, IMAP, Proxy).
    Provides access to the results of completed SMTP checker tasks.
    Only authenticated users can access this API.
    """

    queryset = SMTPCheckerTaskResult.objects.all()
    serializer_class = SMTPCheckerTaskResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SMTPCheckerTaskResult.objects.filter(task__user=self.request.user)

    def get_permissions(self):
        """Only allow authenticated users to access results"""
        return [permission() for permission in (IsAuthenticated, IsTokenValid)]

    @swagger_auto_schema(
        operation_summary="List SMTP Results",
        operation_description="Retrieve a list of all SMTP checker results."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create SMTP Result",
        operation_description="Create a new SMTP checker result."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve SMTP Result",
        operation_description="Retrieve a specific SMTP checker result."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update SMTP Result",
        operation_description="Update an SMTP checker result."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update SMTP Result",
        operation_description="Partially update an SMTP checker result."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete SMTP Result",
        operation_description="Delete an SMTP checker result."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    