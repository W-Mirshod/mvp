from django.db import models
from django.db.models.signals import post_delete, post_save
from django.utils.translation import gettext_lazy as _

from apps.campaign.constants import CampaignConstants
from apps.changelog.mixins import ChangeloggableMixin
from apps.changelog.signals import journal_save_handler, journal_delete_handler
from utils.models import DateModelMixin, DeleteModelMixin
from apps.users.models.users import User
from utils.model_fields import EncryptedJSONField


class EmailBackend(ChangeloggableMixin, DateModelMixin, DeleteModelMixin):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="backend_to_user",
    )
    mailing_type = models.PositiveSmallIntegerField(
        choices=CampaignConstants.MAILING_TYPE_CHOICES,
        help_text=_("Backend mailing type"),
    )
    config = EncryptedJSONField(help_text=_("User config for chosen backend"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("EmailBackend")
        verbose_name_plural = _("EmailBackend")


post_save.connect(journal_save_handler, sender=EmailBackend)
post_delete.connect(journal_delete_handler, sender=EmailBackend)
