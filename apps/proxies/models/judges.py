from django.db import models
from django.db.models.signals import post_save, post_delete
from django.utils.translation import gettext_lazy as _

from apps.changelog.signals import journal_save_handler, journal_delete_handler


class Judge(models.Model):
    url = models.URLField()

    class Meta:
        ordering = ("-id",)
        verbose_name = _("Judge")
        verbose_name_plural = _("Judges")

    def __str__(self):
        return self.url

post_save.connect(journal_save_handler, sender=Judge)
post_delete.connect(journal_delete_handler, sender=Judge)
