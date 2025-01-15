from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.mail_servers.models.servers import Server
from src.apps.mailers.models.template import MessageTemplate
from src.apps.users.models.users import User
from src.utils.models import DateModelMixin, DeleteModelMixin


class SentMessage(DeleteModelMixin, DateModelMixin, models.Model):
    user = models.ForeignKey(
        User, related_name="messages", on_delete=models.CASCADE, null=True, blank=True
    )
    server = models.ForeignKey(
        Server, related_name="messages", on_delete=models.CASCADE, null=True, blank=True
    )
    template = models.ForeignKey(
        MessageTemplate,
        related_name="messages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    message = models.TextField(_("Message"), blank=True, null=True)
    results = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = _("Sent message")
        verbose_name_plural = _("Sent messages")
