from django.db import models
from django.db.models.signals import post_delete, post_save
from django.utils.translation import gettext_lazy as _

from apps.campaign.constants import CampaignConstants
from apps.changelog.mixins import ChangeloggableMixin
from apps.changelog.signals import journal_save_handler, journal_delete_handler
from apps.users.models.users import User
from apps.campaign.models.backend import EmailBackend
from utils.models import DateModelMixin, DeleteModelMixin


class Campaign(ChangeloggableMixin, DateModelMixin, DeleteModelMixin):
    campaign_id = models.CharField(
        max_length=CampaignConstants.ID_MAX_LENGTH,
        unique=True,
        help_text=_("Campaign id from user"),
    )
    campaign_name = models.CharField(
        max_length=CampaignConstants.ID_MAX_LENGTH, help_text=_("Campaign name")
    )
    email_backend = models.ForeignKey(
        to=EmailBackend,
        on_delete=models.SET_NULL,
        related_name=_("campaign_to_backend"),
        null=True,
    )
    shipping_type = models.PositiveSmallIntegerField(
        choices=CampaignConstants.SHIPPING_TYPE_CHOICES,
        help_text=_("Campaign shipping type"),
    )
    status = models.PositiveSmallIntegerField(
        choices=CampaignConstants.CAMPAIGN_STATUS_CHOICES,
        default=CampaignConstants.NEW_CAMPAIGN_STATUS,
        help_text=_("Campaign shipping type"),
    )
    visitors = models.IntegerField(default=0, help_text=_("Visitor clicks"))
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name=_("campaign_to_user"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.campaign_id

    class Meta:
        verbose_name = _("Campaign")
        verbose_name_plural = _("Campaign")


post_save.connect(journal_save_handler, sender=Campaign)
post_delete.connect(journal_delete_handler, sender=Campaign)
