from django.db import models
from django.db.models.signals import post_delete, post_save
from django.utils.translation import gettext_lazy as _

from apps.changelog.mixins import ChangeloggableMixin
from apps.changelog.signals import journal_save_handler, journal_delete_handler
from apps.mail_servers.choices import ServerType
from utils.models import DateModelMixin, DeleteModelMixin


class Server(ChangeloggableMixin, DeleteModelMixin, DateModelMixin, models.Model):
    type = models.CharField(max_length=255, choices=ServerType.CHOICES)
    url = models.URLField()
    port = models.IntegerField()
    password = models.CharField(max_length=255, blank=True, null=True)
    username = models.EmailField(
        default="default_smtp@example.com", blank=True, null=True
    )
    email_use_tls = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Server")
        verbose_name_plural = _("Servers")
        ordering = ("-id",)

    def __str__(self):
        return f"{self.type} server({self.id}): {self.url}:{self.port}"


class SMTPManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(type=ServerType.SMTP)
        return qs


class SMTPServer(Server):
    objects = SMTPManager()

    class Meta:
        proxy = True
        verbose_name = _("SMTP server")
        verbose_name_plural = _("SMTP servers")

    def __str__(self):
        return f"SMTP server({self.id}): {self.url}:{self.port}"


class IMAPManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(type=ServerType.IMAP)
        return qs


class IMAPServer(Server):
    objects = IMAPManager()

    class Meta:
        proxy = True
        verbose_name = _("IMAP server")
        verbose_name_plural = _("IMAP servers")

        def __str__(self):
            return f"IMAP server({self.id}): {self.url}:{self.port}"


class PROXYManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(type=ServerType.PROXY)
        return qs


class ProxyServer(Server):
    objects = PROXYManager()

    class Meta:
        proxy = True
        verbose_name = _("Proxy server")
        verbose_name_plural = _("Proxy servers")

    def __str__(self):
        return f"Proxy server({self.id}): {self.url}:{self.port}"


post_save.connect(journal_save_handler, sender=SMTPServer)
post_delete.connect(journal_delete_handler, sender=SMTPServer)

post_save.connect(journal_save_handler, sender=IMAPServer)
post_delete.connect(journal_delete_handler, sender=IMAPServer)

post_save.connect(journal_save_handler, sender=ProxyServer)
post_delete.connect(journal_delete_handler, sender=ProxyServer)
