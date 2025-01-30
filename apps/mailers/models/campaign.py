from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.mailers.constants import CampaignConstants
from apps.backend_mailer.models import Email
from apps.users.models import User

from utils.models import DateModelMixin, DeleteModelMixin


class Campaign(DeleteModelMixin, DateModelMixin, models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="campaign_to_user",
    )
    campaign_id = models.CharField(
        max_length=CampaignConstants.MAX_CAMPAIGN_ID_LENGTH,
        help_text=_("Campaign it"),
        verbose_name=_("Campaign id"),
    )
    campaign_name = models.CharField(
        max_length=CampaignConstants.MAX_CAMPAIGN_NAME_LENGTH,
        help_text=_("Campaign name"),
        verbose_name=_("Campaign name"),
    )
    shipping_type = models.PositiveSmallIntegerField(
        choices=CampaignConstants.SHIPPING_TYPE_CHOICES,
        default=CampaignConstants.SHIPPING.default,
        help_text=_("Campaign shipping type"),
    )
    message_type = models.PositiveSmallIntegerField(
        choices=CampaignConstants.MESSAGE_TYPE_CHOICES,
        default=CampaignConstants.MESSAGE_TYPE.default,
        help_text=_("Campaign message type"),
    )
    comment = models.TextField(help_text=_("Campaign comment"))
    open_rate = models.IntegerField(help_text=_("Campaign open rate"), default=0)
    visitor_clicks = models.IntegerField(
        help_text=_("Campaign visitor clicks"), default=0
    )

    status = models.PositiveSmallIntegerField(
        choices=CampaignConstants.STATUS_CHOICES,
        default=CampaignConstants.STATUS.created,
        help_text=_("Campaign status"),
    )

    message = models.ForeignKey(
        Email, on_delete=models.CASCADE, help_text=_("Message for campaign")
    )
    country_tag = models.CharField(
        max_length=CampaignConstants.MAX_COUNTRY_TAG_LENGTH,
        help_text=_("Country filed"),
        verbose_name=_("Country filed"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
