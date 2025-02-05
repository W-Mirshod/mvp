from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.mail_servers.models import Server
from apps.smtp_checker.choises import TaskStatus, TaskResult


class SMTPCheckerSettings(models.Model):
    """SMTP server check settings"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="smtp_checker_settings")
    name = models.CharField(max_length=255, default="Default")
    threads_count = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    connection_timeout = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(60)])
    attempts_for_sending_count = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        verbose_name = "SMTP Checker Settings"
        verbose_name_plural = "SMTP Checker Settings"


class SMTPCheckerTask(models.Model):
    """SMTP checker tasks"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="smtp_check_tasks")
    settings = models.ForeignKey(SMTPCheckerSettings, on_delete=models.CASCADE, related_name="smtp_check_tasks")
    servers = models.ManyToManyField(Server, related_name="check_tasks")
    status = models.CharField(max_length=50, choices=TaskStatus.CHOICES, default="pending")

    class Meta:
        verbose_name = "SMTP Checker Task"
        verbose_name_plural = "SMTP Checker Task"


class SMTPCheckerTaskResult(models.Model):
    """SMTP server test results"""
    task = models.ForeignKey(SMTPCheckerTask, on_delete=models.CASCADE, related_name="results")
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="results")
    result = models.CharField(max_length=50, choices=TaskResult.CHOICES, default="failure")
    response_time = models.FloatField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "SMTP Checker Task Result"
