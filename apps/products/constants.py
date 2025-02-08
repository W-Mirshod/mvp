from collections import namedtuple
from django.utils.translation import gettext_lazy as _

class TariffConstants:
    """TARIFF  ->"""

    TARIFF = namedtuple("TARIFF", "basic premium deluxe")._make(range(3))

    TARIFF_CHOICES = [
        (TARIFF.basic, _("Basic")),
        (TARIFF.premium, _("Premium")),
        (TARIFF.deluxe, _("Deluxe")),
    ]
    """<- TARIFF """