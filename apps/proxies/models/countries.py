from django.db import models
from django.db.models.signals import post_save, post_delete
from django.utils.translation import gettext_lazy as _

from apps.changelog.signals import journal_save_handler, journal_delete_handler


class Country(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ("name", )
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return self.name

post_save.connect(journal_save_handler, sender=Country)
post_delete.connect(journal_delete_handler, sender=Country)
