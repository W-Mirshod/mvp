from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from apps.smtp_checker.choises import TaskStatus, TaskResult
from apps.smtp_checker.models.models import SMTPCheckerTask, SMTPCheckerTaskResult, TaskStatistics


class SMTPStatisticsAPIView(APIView):
    permission_classes = []

    def get(self, request):
        current_stats = TaskStatistics.objects.first()
        if not current_stats:
            current_stats = TaskStatistics.objects.create()

        smtp_time_passed = None
        if current_stats.smtp_check_start_time:
            end_time = current_stats.smtp_check_end_time or timezone.now()
            smtp_time_passed = end_time - current_stats.smtp_check_start_time

        total_processed = SMTPCheckerTaskResult.objects.count()
        remaining_tasks = SMTPCheckerTask.objects.filter(status=TaskStatus.PENDING).count()
        
        if total_processed > 0 and smtp_time_passed:
            avg_time_per_task = smtp_time_passed.total_seconds() / total_processed
            estimated_remaining_time = timedelta(seconds=avg_time_per_task * remaining_tasks)
        else:
            estimated_remaining_time = timedelta(hours=24)

        tasks_data = SMTPCheckerTask.objects.aggregate(
            total=Count('id'),
            active=Count('id', filter=Q(status=TaskStatus.IN_PROGRESS)),
            stopped=Count('id', filter=Q(status=TaskStatus.FAILED))
        )

        one_minute_ago = timezone.now() - timedelta(minutes=1)
        sending_per_minute = SMTPCheckerTaskResult.objects.filter(
            task__created_at__gte=one_minute_ago,
            result=TaskResult.SUCCESS
        ).count()

        results_data = SMTPCheckerTaskResult.objects.aggregate(
            successful=Count('id', filter=Q(result=TaskResult.SUCCESS)),
            invalid_recipients=Count('id', filter=Q(error_message__icontains="invalid recipient")),
            proxy_success=Count('id', filter=Q(server__type__iexact="proxy") & Q(result=TaskResult.SUCCESS))
        )

        data = {
            "smtp_for_check": tasks_data['total'],
            "sending_per_minute": sending_per_minute,
            "stopped": tasks_data['stopped'],
            "smtp_in_clipboard": current_stats.smtp_in_clipboard,
            "proxy_on": results_data['proxy_success'],
            "recipients_queue": current_stats.recipients_queue,
            "sent": results_data['successful'],
            "invalid_recipients": results_data['invalid_recipients'],
            "active_threads": tasks_data['active'],
            "valid_smtp": results_data['successful'],
            "time_passed": str(smtp_time_passed).split('.')[0] if smtp_time_passed else "00:00:00",
            "time_left": str(estimated_remaining_time).split('.')[0]
        }
        
        return JsonResponse(data)
