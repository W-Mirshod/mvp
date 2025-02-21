from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from apps.smtp_checker.choises import TaskStatus, TaskResult
from apps.smtp_checker.models.models import SMTPCheckerTask, SMTPCheckerTaskResult, TaskStatistics


from django.db.models.query import QuerySet

class SMTPStatisticsQuerySet(QuerySet):
    def __init__(self, model=None, query=None, using=None, hints=None):
        super().__init__(model=model, query=query, using=using, hints=hints)
        self.user = None
        self.current_stats = None

    def for_user(self, user):
        self.user = user
        self.current_stats, _ = TaskStatistics.objects.get_or_create(user=user)
        return self

    def get_time_passed(self):
        if self.current_stats and self.current_stats.smtp_check_start_time:
            end_time = self.current_stats.smtp_check_end_time or timezone.now()
            return end_time - self.current_stats.smtp_check_start_time
        return None

    def get_tasks_data(self):
        return SMTPCheckerTask.objects.filter(user=self.user).aggregate(
            total=Count('id'),
            active=Count('id', filter=Q(status=TaskStatus.IN_PROGRESS)),
            stopped=Count('id', filter=Q(status=TaskStatus.FAILED)),
            remaining_tasks=Count('id', filter=Q(status=TaskStatus.PENDING))
        )

    def get_results_data(self):
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        return SMTPCheckerTaskResult.objects.filter(task__user=self.user).aggregate(
            successful=Count('id', filter=Q(result=TaskResult.SUCCESS)),
            invalid_recipients=Count('id', filter=Q(error_message__icontains="invalid recipient")),
            proxy_success=Count('id', filter=Q(server__type__iexact="proxy") & Q(result=TaskResult.SUCCESS)),
            sending_per_minute=Count('id', filter=Q(
                task__created_at__gte=one_minute_ago,
                result=TaskResult.SUCCESS
            ))
        )

    def get_estimated_remaining_time(self, total_processed, remaining_tasks):
        if total_processed > 0 and self.get_time_passed():
            avg_time_per_task = self.get_time_passed().total_seconds() / total_processed
            return timedelta(seconds=avg_time_per_task * remaining_tasks)
        return timedelta(hours=24)
    