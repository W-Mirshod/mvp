from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

from apps.smtp_checker.models.models import SMTPCheckerTask, SMTPCheckerTaskResult, TaskStatistics
from apps.smtp_checker.choises import TaskStatus, TaskResult

@receiver(post_save, sender=SMTPCheckerTask)
def update_task_statistics(sender, instance, created, **kwargs):
    stats = TaskStatistics.get_or_create_current()
    
    if instance.status == TaskStatus.IN_PROGRESS:
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        sending_rate = SMTPCheckerTaskResult.objects.filter(
            task__status=TaskStatus.IN_PROGRESS,
            result=TaskResult.SUCCESS,
            task__settings__created_at__gte=one_minute_ago
        ).count()
        stats.update_sending_rate(sending_rate)

@receiver(post_save, sender=SMTPCheckerTaskResult)
def update_result_statistics(sender, instance, created, **kwargs):
    if created:
        stats = TaskStatistics.get_or_create_current()
        
        pending_results = SMTPCheckerTaskResult.objects.filter(
            result=TaskResult.PENDING
        ).count()
        stats.update_recipients_queue(pending_results)

@receiver([post_save, post_delete], sender=SMTPCheckerTask)
def update_clipboard_count(sender, **kwargs):
    stats = TaskStatistics.get_or_create_current()
    
    clipboard_count = SMTPCheckerTask.objects.filter(
        status=TaskStatus.PENDING
    ).count()
    stats.update_smtp_clipboard(clipboard_count)

@receiver(post_save, sender=SMTPCheckerTask)
def track_smtp_check_timing(sender, instance, created, **kwargs):
    stats = TaskStatistics.get_or_create_current()
    
    if created and instance.status == TaskStatus.PENDING:
        stats.start_smtp_check()
    elif instance.status == TaskStatus.COMPLETED:
        pending_tasks = SMTPCheckerTask.objects.filter(
            status__in=[TaskStatus.PENDING, TaskStatus.IN_PROGRESS]
        ).exists()
        if not pending_tasks:
            stats.end_smtp_check()

    total_smtp = SMTPCheckerTask.objects.count()
    valid_smtp = SMTPCheckerTaskResult.objects.filter(result=TaskResult.SUCCESS).count()
    stats.update_smtp_counts(total_smtp, valid_smtp)
