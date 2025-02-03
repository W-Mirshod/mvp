from collections import namedtuple
from django.utils.translation import gettext_lazy as _


class CampaignConstants:

    MAX_CAMPAIGN_ID_LENGTH = 255
    MAX_CAMPAIGN_NAME_LENGTH = 500
    MAX_COUNTRY_TAG_LENGTH = 3

    """SHIPPING TYPE ->"""
    SHIPPING = namedtuple("SHIPPING", "default speed extra_speed")._make(range(3))

    SHIPPING_TYPE_CHOICES = [
        (SHIPPING.default, _("Default")),
        (SHIPPING.speed, _("Speed")),
        (SHIPPING.extra_speed, _("Extra Speed")),
    ]

    """<- SHIPPING TYPE"""

    """MESSAGE TYPE ->"""
    MESSAGE_TYPE = namedtuple(
        "MESSAGE_TYPE", "default promotion_options newsletter transactional"
    )._make(range(4))

    MESSAGE_TYPE_CHOICES = [
        (MESSAGE_TYPE.default, _("Default")),
        (MESSAGE_TYPE.promotion_options, _("Promotion options")),
        (MESSAGE_TYPE.newsletter, _("Newsletter")),
        (MESSAGE_TYPE.transactional, _("Transactional")),
    ]

    """<- MESSAGE TYPE"""

    """ STATUS ->"""
    STATUS = namedtuple(
        "STATUS", "created started completed stopped error ai_mailing sending "
    )._make(range(7))

    STATUS_CHOICES = [
        (STATUS.created, _("created")),
        (STATUS.started, _("started")),
        (STATUS.completed, _("Completed")),
        (STATUS.stopped, _("Stopped")),
        (STATUS.error, _("Error")),
        (STATUS.ai_mailing, _("AI Mailing")),
        (STATUS.sending, _("Sending")),
    ]
    """ STATUS ->"""
