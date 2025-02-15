from django.conf import settings
from django.db import models

from apps.notify.constants import NotifyConstants


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_to_user",
    )

    title = models.CharField(
        max_length=NotifyConstants.TITLE_MAX_DIGITS,
    )
    description = models.CharField(
        max_length=NotifyConstants.DESCRIPTION_MAX_DIGITS,
        default="",
    )
    notify_type = models.PositiveSmallIntegerField(
        choices=NotifyConstants.NOTIFY_TYPE_CHOICES,
        default=NotifyConstants.NOTIFICATIONS.general,
    )
    is_viewed = models.BooleanField(default=False, null=True, blank=True)
    data = models.JSONField(
        default=dict,
        help_text="Any useful data.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"Notification '{self.id}'"

    class Meta:
        ordering = ("-created_at",)
