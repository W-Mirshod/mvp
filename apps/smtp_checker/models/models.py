from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.mail_servers.models import Server
from apps.smtp_checker.choises import TaskStatus, TaskResult
from django.utils import timezone


class SMTPCheckerSettings(models.Model):
    """SMTP server check settings"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="smtp_checker_settings",
    )
    name = models.CharField(max_length=255, default="Default")
    threads_count = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    connection_timeout = models.IntegerField(
        default=5, validators=[MinValueValidator(1), MaxValueValidator(60)]
    )
    attempts_for_sending_count = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        verbose_name = "SMTP Checker Settings"
        verbose_name_plural = "SMTP Checker Settings"


class SMTPCheckerTask(models.Model):
    """SMTP checker tasks"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="smtp_check_tasks",
    )
    settings = models.ForeignKey(
        SMTPCheckerSettings, on_delete=models.CASCADE, related_name="smtp_check_tasks"
    )
    servers = models.ManyToManyField(Server, related_name="check_tasks")
    status = models.CharField(
        max_length=50, choices=TaskStatus.CHOICES, default=TaskStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "SMTP Checker Task"
        verbose_name_plural = "SMTP Checker Task"


class SMTPCheckerTaskResult(models.Model):
    """SMTP server test results"""

    task = models.ForeignKey(
        SMTPCheckerTask, on_delete=models.CASCADE, related_name="results"
    )
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="results")
    result = models.CharField(
        max_length=50, choices=TaskResult.CHOICES, default=TaskResult.FAILURE
    )
    response_time = models.FloatField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "SMTP Checker Task Result"


class TaskStatistics(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    smtp_check_start_time = models.DateTimeField(null=True, blank=True)
    smtp_check_end_time = models.DateTimeField(null=True, blank=True)
    recipients_queue = models.IntegerField(default=0)
    smtp_in_clipboard = models.IntegerField(default=0)
    sending_per_minute = models.IntegerField(default=0)
    total_smtp_count = models.IntegerField(default=0)
    valid_smtp_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Task Statistics"
        verbose_name_plural = "Task Statistics"

    @classmethod
    def get_or_create_current(cls):
        qs = cls.objects.filter(end_time__isnull=True).order_by('-start_time')
        if qs.exists():
            return qs.first()
        else:
            return cls.objects.create()
    
    def update_smtp_clipboard(self, count):
        self.smtp_in_clipboard = count
        self.save()

    def update_recipients_queue(self, count):
        self.recipients_queue = count
        self.save()

    def update_sending_rate(self, rate):
        self.sending_per_minute = rate
        self.save()

    def complete_statistics(self):
        self.end_time = timezone.now()
        self.save()

    def start_smtp_check(self):
        if not self.smtp_check_start_time:
            self.smtp_check_start_time = timezone.now()
            self.save()

    def end_smtp_check(self):
        self.smtp_check_end_time = timezone.now()
        self.save()

    def update_smtp_counts(self, total, valid):
        self.total_smtp_count = total
        self.valid_smtp_count = valid
        self.save()
