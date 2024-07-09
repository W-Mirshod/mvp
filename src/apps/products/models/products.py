from django.db import models

from utils.models import DateModelMixin, DeleteModelMixin


class Product(DateModelMixin, DeleteModelMixin):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
