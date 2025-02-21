import logging
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from apps.smtp_checker.choises import TaskStatus
from apps.smtp_checker.utils.smtp_service import check_server_task
from apps.smtp_checker.view_logic.statics_view import SMTPStatisticsQuerySet


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

logger = logging.getLogger(__name__)


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
        if getattr(self, "swagger_fake_view", False):
            return SMTPCheckerSettings.objects.none()
        return SMTPCheckerSettings.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Ensure the user is set before saving"""
        serializer.save(user=self.request.user)
        logger.info(f"SMTP settings created for user {self.request.user.id}")

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
        operation_description="Retrieve a list of all SMTP checker settings for the authenticated user.",
    )
    def list(self, request, *args, **kwargs):
        logger.debug(f"Listing SMTP settings for user {request.user.id}")
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create SMTP Settings",
        operation_description="Create new SMTP checker settings.",
    )
    def create(self, request, *args, **kwargs):
        logger.debug(f"Creating SMTP settings for user {request.user.id}")
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve SMTP Settings",
        operation_description="Retrieve specific SMTP checker settings.",
    )
    def retrieve(self, request, *args, **kwargs):
        logger.debug(f"Retrieving SMTP settings for user {request.user.id}")
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update SMTP Settings",
        operation_description="Update SMTP checker settings.",
    )
    def update(self, request, *args, **kwargs):
        logger.debug(f"Updating SMTP settings for user {request.user.id}")
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update SMTP Settings",
        operation_description="Partially update SMTP checker settings.",
    )
    def partial_update(self, request, *args, **kwargs):
        logger.debug(f"Partially updating SMTP settings for user {request.user.id}")
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete SMTP Settings",
        operation_description="Delete SMTP checker settings.",
    )
    def destroy(self, request, *args, **kwargs):
        logger.debug(f"Deleting SMTP settings for user {request.user.id}")
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
        if getattr(self, "swagger_fake_view", False):
            return SMTPCheckerTask.objects.none()
        return SMTPCheckerTask.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Ensure the user is set before saving"""
        serializer.save(user=self.request.user)
        logger.info(f"SMTP task created for user {self.request.user.id}")

    @swagger_auto_schema(
        operation_summary="Run SMTP Check Task",
        operation_description="Initiate an asynchronous SMTP server check task.",
    )
    @action(detail=True, methods=["post"], url_path="run-task")
    def run_task(self, request, pk=None):
        """Runs the server check task asynchronously"""
        task = self.get_object()

        if task.status in [TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED]:
            logger.warning(f"Attempted to run already processed task {task.id}")
            return Response(
                {"detail": "Task is already being processed or completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            logger.info(f"Starting SMTP check task {task.id} for user {request.user.id}")
            task.status = TaskStatus.IN_PROGRESS
            task.save()
            
            check_server_task.delay(task.id, task.settings.id)
            
            return Response(
                {"detail": "Task has been queued for processing."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Failed to queue task {task.id}: {str(e)}")
            task.status = TaskStatus.FAILED
            task.save()
            return Response(
                {"detail": "Failed to queue task. Please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

    @swagger_auto_schema(
        operation_summary="List SMTP Tasks",
        operation_description="Retrieve a list of all SMTP checker tasks.",
    )
    def list(self, request, *args, **kwargs):
        logger.debug(f"Listing SMTP tasks for user {request.user.id}")
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create SMTP Task",
        operation_description="Create a new SMTP checker task.",
    )
    def create(self, request, *args, **kwargs):
        logger.debug(f"Creating SMTP task for user {request.user.id}")
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve SMTP Task",
        operation_description="Retrieve a specific SMTP checker task.",
    )
    def retrieve(self, request, *args, **kwargs):
        logger.debug(f"Retrieving SMTP task for user {request.user.id}")
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update SMTP Task",
        operation_description="Update an SMTP checker task.",
    )
    def update(self, request, *args, **kwargs):
        logger.debug(f"Updating SMTP task for user {request.user.id}")
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update SMTP Task",
        operation_description="Partially update an SMTP checker task.",
    )
    def partial_update(self, request, *args, **kwargs):
        logger.debug(f"Partially updating SMTP task for user {request.user.id}")
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete SMTP Task",
        operation_description="Delete an SMTP checker task.",
    )
    def destroy(self, request, *args, **kwargs):
        logger.debug(f"Deleting SMTP task for user {request.user.id}")
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
        if getattr(self, "swagger_fake_view", False):
            return SMTPCheckerTaskResult.objects.none()
        return SMTPCheckerTaskResult.objects.filter(task__user=self.request.user)

    def get_permissions(self):
        """Only allow authenticated users to access results"""
        return [permission() for permission in (IsAuthenticated, IsTokenValid)]

    @swagger_auto_schema(
        operation_summary="List SMTP Results",
        operation_description="Retrieve a list of all SMTP checker results.",
    )
    def list(self, request, *args, **kwargs):
        logger.debug(f"Listing SMTP results for user {request.user.id}")
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create SMTP Result",
        operation_description="Create a new SMTP checker result.",
    )
    def create(self, request, *args, **kwargs):
        logger.debug(f"Creating SMTP result for user {request.user.id}")
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve SMTP Result",
        operation_description="Retrieve a specific SMTP checker result.",
    )
    def retrieve(self, request, *args, **kwargs):
        logger.debug(f"Retrieving SMTP result for user {request.user.id}")
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update SMTP Result",
        operation_description="Update an SMTP checker result.",
    )
    def update(self, request, *args, **kwargs):
        logger.debug(f"Updating SMTP result for user {request.user.id}")
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update SMTP Result",
        operation_description="Partially update an SMTP checker result.",
    )
    def partial_update(self, request, *args, **kwargs):
        logger.debug(f"Partially updating SMTP result for user {request.user.id}")
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete SMTP Result",
        operation_description="Delete an SMTP checker result.",
    )
    def destroy(self, request, *args, **kwargs):
        logger.debug(f"Deleting SMTP result for user {request.user.id}")
        return super().destroy(request, *args, **kwargs)


class SMTPStatisticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = SMTPStatisticsQuerySet()
        total_processed = SMTPCheckerTaskResult.objects.filter(task__user=request.user).count()
        
        tasks_data = queryset.get_tasks_data()
        results_data = queryset.get_results_data()
        smtp_time_passed = queryset.get_time_passed()
        estimated_remaining_time = queryset.get_estimated_remaining_time(
            total_processed, 
            tasks_data['remaining_tasks']
        )

        data = {
            "smtp_for_check": tasks_data['total'],
            "sending_per_minute": results_data['sending_per_minute'],
            "stopped": tasks_data['stopped'],
            "smtp_in_clipboard": queryset.current_stats.smtp_in_clipboard if queryset.current_stats else 0,
            "proxy_on": results_data['proxy_success'],
            "recipients_queue": queryset.current_stats.recipients_queue if queryset.current_stats else 0,
            "sent": results_data['successful'],
            "invalid_recipients": results_data['invalid_recipients'],
            "active_threads": tasks_data['active'],
            "valid_smtp": results_data['successful'],
            "time_passed": str(smtp_time_passed).split('.')[0] if smtp_time_passed else "00:00:00",
            "time_left": str(estimated_remaining_time).split('.')[0]
        }
        
        return JsonResponse(data)
