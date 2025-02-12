from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
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
        null=True,
        blank=True,
    )
    campaign_name = models.CharField(
        max_length=CampaignConstants.MAX_CAMPAIGN_NAME_LENGTH,
        help_text=_("Campaign name"),
        verbose_name=_("Campaign name"),
    )
    campaign_tag = models.CharField(
        max_length=CampaignConstants.MAX_CAMPAIGN_TAG_LENGTH,
        help_text=_("Campaign tag"),
        verbose_name=_("Campaign tag"),
        null=True,
        blank=True,
    )
    country = CountryField(
        blank_label="(select country)",
        blank=True,
        null=True,
        help_text=_("Campaign country"),
    )
    email_content = models.TextField(
        help_text=_("Email content"),
        blank=True,
        null=True,
    )
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
