from django.utils.translation import gettext_lazy as _
from collections import namedtuple


class NotifyConstants:
    """NotifyConstants"""

    TITLE_MAX_DIGITS = 100
    DESCRIPTION_MAX_DIGITS = 500

    """Notify type ->"""
    NOTIFICATIONS = namedtuple("NOTIFICATIONS", "order payment item general")._make(
        range(4)
    )
    NOTIFY_TYPE_CHOICES = (
        (NOTIFICATIONS.order, _("Order")),
        (NOTIFICATIONS.payment, _("Payment")),
        (NOTIFICATIONS.item, _("Item")),
        (NOTIFICATIONS.general, _("General")),
    )
    """<- Notify type"""
