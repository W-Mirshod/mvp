from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.utils.translation import gettext_lazy as _

from apps.changelog.mixins import ChangeloggableMixin
from apps.changelog.signals import journal_save_handler, journal_delete_handler
from utils.models import DateModelMixin, DeleteModelMixin


class Proxy(ChangeloggableMixin, DateModelMixin, DeleteModelMixin):
    host = models.CharField(max_length=15)
    port = models.PositiveIntegerField()
    is_active = models.BooleanField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    country_code = models.CharField(max_length=5, blank=True, null=True)
    anonymity = models.CharField(max_length=15, blank=True, null=True)
    timeout = models.PositiveIntegerField(blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-id", )
        verbose_name = _("Proxy")
        verbose_name_plural = _("Proxies")

    def __str__(self):
        return f"{self.host}:{self.port}"


post_save.connect(journal_save_handler, sender=Proxy)
post_delete.connect(journal_delete_handler, sender=Proxy)
