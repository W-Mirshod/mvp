from django.db import models
from django.db.models.signals import post_delete, post_save

from apps.changelog.mixins import ChangeloggableMixin
from apps.changelog.signals import journal_delete_handler, journal_save_handler
from utils.models import DateModelMixin, DeleteModelMixin


class Product(ChangeloggableMixin, DateModelMixin, DeleteModelMixin):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


post_save.connect(journal_save_handler, sender=Product)
post_delete.connect(journal_delete_handler, sender=Product)
