from django.db import models
from django.db.models.signals import post_delete, post_save
from django.utils.translation import gettext_lazy as _

from apps.changelog.mixins import ChangeloggableMixin
from apps.users.models import User
from apps.changelog.signals import journal_delete_handler, journal_save_handler
from utils.models import DateModelMixin, DeleteModelMixin


class Company(ChangeloggableMixin, DeleteModelMixin, DateModelMixin, models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    employees = models.ManyToManyField(User, related_name='companies')

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ("-id",)

    def __str__(self):
        return self.title


post_save.connect(journal_save_handler, sender=User)
post_delete.connect(journal_delete_handler, sender=User)
