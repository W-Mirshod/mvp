from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import DateModelMixin, DeleteModelMixin


class MailServer(DeleteModelMixin, DateModelMixin, models.Model):
    url = models.URLField()
    port = models.IntegerField()
    password = models.CharField(max_length=255, blank=True, null=True)
    username = models.EmailField(default="default_smtp@example.com", blank=True, null=True)
    email_use_tls = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class SMTPServer(MailServer):

    class Meta:
        verbose_name = _("SMTPServer")
        verbose_name_plural = _("SMTPServers")


class IMAPServer(MailServer):

    class Meta:
        verbose_name = _("IMAPServer")
        verbose_name_plural = _("IMAPServers")


class ProxyServer(MailServer):

    class Meta:
        verbose_name = _("IMAPServer")
        verbose_name_plural = _("IMAPServers")
