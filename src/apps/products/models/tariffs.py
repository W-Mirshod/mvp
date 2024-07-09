from django.db import models

from apps.products.models import Product
from utils.models import DateModelMixin, DeleteModelMixin


class Tariff(DateModelMixin, DeleteModelMixin):
    title = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="tariffs")

    def __str__(self):
        return self.title
