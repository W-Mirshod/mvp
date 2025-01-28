from django.db import models
from django.db.models.signals import post_delete, post_save
from django.utils.translation import gettext_lazy as _


from apps.backend_mailer.constants import BackendConstants
from apps.backend_mailer.fields import encrypt_config
from apps.changelog.mixins import ChangeloggableMixin
from apps.changelog.signals import journal_save_handler, journal_delete_handler
from utils.models import DateModelMixin, DeleteModelMixin
from apps.users.models.users import User


class EmailBackend(ChangeloggableMixin, DateModelMixin, DeleteModelMixin):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="backend_to_user",
    )
    mailing_type = models.PositiveSmallIntegerField(
        choices=BackendConstants.MAILING_TYPE_CHOICES,
        help_text=_("Backend mailing type"),
    )
    config = models.TextField(help_text=_("User config for chosen backend"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("EmailBackend")
        verbose_name_plural = _("EmailBackend")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):

        if self.config:
            self.config = encrypt_config(self.config)
        super().save(force_insert, force_update, using, update_fields)


post_save.connect(journal_save_handler, sender=EmailBackend)
post_delete.connect(journal_delete_handler, sender=EmailBackend)
