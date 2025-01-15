from django.db import models
from django.db.models.signals import post_delete, post_save

from src.apps.changelog.mixins import ChangeloggableMixin
from src.apps.changelog.signals import journal_delete_handler, journal_save_handler
from src.apps.products.models import Product
from src.utils.models import DateModelMixin, DeleteModelMixin


class Tariff(ChangeloggableMixin, DateModelMixin, DeleteModelMixin):
    title = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="tariffs"
    )

    def __str__(self):
        return self.title


post_save.connect(journal_save_handler, sender=Tariff)
post_delete.connect(journal_delete_handler, sender=Tariff)
