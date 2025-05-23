from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.backend_mailer.constants import BackendConstants
from apps.backend_mailer.models import Email


class SentMessages(models.Model):
    email = models.ForeignKey(
        to=Email, on_delete=models.SET_NULL, blank=True, null=True
    )
    to = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_("Email To"),
        help_text=_("Email To"),
    )

    status = models.PositiveSmallIntegerField(
        _("Status"),
        choices=BackendConstants.STATUS_CHOICES,
        db_index=True,
        default=BackendConstants.STATUS.created,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("SentMessages")
        verbose_name_plural = _("SentMessages")
