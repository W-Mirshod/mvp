from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import DateModelMixin, DeleteModelMixin


class MessageTemplate(DeleteModelMixin, DateModelMixin, models.Model):
    from_address = models.CharField(max_length=255, blank=True, null=True)
    template = models.TextField(blank=True, null=True)
    message = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = _("MessageTemplate")
        verbose_name_plural = _("MessageTemplates")
