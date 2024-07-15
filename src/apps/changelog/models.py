from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import ActionsType


class ChangeLog(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Author of the change"),
        on_delete=models.CASCADE,
        null=True,
    )
    changed = models.DateTimeField(auto_now=True, verbose_name=_("Date/time of change"))
    model = models.CharField(max_length=255, verbose_name=_("Table"), null=True)
    record_id = models.IntegerField(verbose_name=_("ID of the record"), null=True)
    action_on_model = models.CharField(
        choices=ActionsType.CHOICES, max_length=50, verbose_name=_("Action"), null=True
    )
    data = models.JSONField(verbose_name=_("Variable model data"), default=dict)
    ipaddress = models.CharField(max_length=15, verbose_name=_("IP address"), null=True)

    class Meta:
        verbose_name = _("Change log")
        verbose_name_plural = _("Change logs")
        ordering = ("changed",)

    def __str__(self):
        return f"{self.model} {self.record_id} {self.action_on_model} by {self.user}"

    @classmethod
    def add(
        cls,
        instance,
        user,
        ipaddress: str,
        action_on_model: ActionsType,
        data: dict,
        id: int = None,
    ) -> int:
        """Creating an entry in the change log"""
        log = ChangeLog.objects.get(id=id) if id else ChangeLog()
        log.model = instance.__class__.__name__
        log.record_id = instance.pk
        if user:
            log.user = user
        log.ipaddress = ipaddress
        log.action_on_model = action_on_model
        log.data = data
        log.save()
        return log.pk
