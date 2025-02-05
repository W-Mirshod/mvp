from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from apps.smtp_checker.utils.smtp_service import check_server_task

from apps.smtp_checker.models.models import SMTPCheckerSettings, SMTPCheckerTask, SMTPCheckerTaskResult
from apps.smtp_checker.serializers.smtp_serializers import (
    SMTPCheckerSettingsSerializer, SMTPCheckerTaskSerializer, SMTPCheckerTaskResultSerializer
)
from utils.permissions import IsTokenValid, IsOwner


class ServerCheckerSettingsAPIView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """API for managing server checker settings"""
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
            return [permission() for permission in (IsAuthenticated, IsTokenValid, IsOwner)]
        else:
            return [permission() for permission in (IsAuthenticated, IsTokenValid)]


class ServerCheckerTaskAPIView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """API for managing SMTP Checker tasks"""
    queryset = SMTPCheckerTask.objects.all()
    serializer_class = SMTPCheckerTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SMTPCheckerTask.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Ensure the user is set before saving"""
        serializer.save(user=self.request.user)

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

        return Response({"detail": "Task has been queued for processing."}, status=status.HTTP_200_OK)

class ServerCheckerTaskResultAPIView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """API for retrieving server checker results (SMTP, IMAP, Proxy)"""
    queryset = SMTPCheckerTaskResult.objects.all()
    serializer_class = SMTPCheckerTaskResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SMTPCheckerTaskResult.objects.filter(task__user=self.request.user)

    def get_permissions(self):
        """Only allow authenticated users to access results"""
        return [permission() for permission in (IsAuthenticated, IsTokenValid)]
