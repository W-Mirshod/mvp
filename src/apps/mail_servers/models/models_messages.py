from django.db import models
from django.db.models.signals import post_delete, post_save
from django.utils.translation import gettext_lazy as _

from apps.changelog.mixins import ChangeloggableMixin
from apps.changelog.signals import journal_delete_handler, journal_save_handler
from utils.models import DateModelMixin, DeleteModelMixin


class MessageTemplate(ChangeloggableMixin, DeleteModelMixin, DateModelMixin, models.Model):
    from_address = models.CharField(max_length=255, blank=True, null=True)
    template = models.TextField(blank=True, null=True)
    message = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = _("MessageTemplate")
        verbose_name_plural = _("MessageTemplates")


post_save.connect(journal_save_handler, sender=MessageTemplate)
post_delete.connect(journal_delete_handler, sender=MessageTemplate)
