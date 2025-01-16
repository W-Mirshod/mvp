from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.products.models.tariffs import Tariff
from apps.users.models.users import User
from utils.models import DateModelMixin, DeleteModelMixin


class UserTariff(DateModelMixin, DeleteModelMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tariff")
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    expired_at = models.DateTimeField(_("Date of expiration"), blank=True, null=True)

    class Meta:
        verbose_name = _("User`s tariff")
        verbose_name_plural = _("User`s tariffs")
