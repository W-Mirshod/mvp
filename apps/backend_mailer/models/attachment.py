import os
from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from apps.backend_mailer.logutils import setup_loghandlers
from apps.backend_mailer.models.email import Email

logger = setup_loghandlers("INFO")


def get_upload_path(instance, filename):
    """Overriding to store the original filename"""
    if not instance.name:
        instance.name = filename  # set original filename
    date = timezone.now().date()
    filename = "{name}.{ext}".format(name=uuid4().hex, ext=filename.split(".")[-1])

    return os.path.join(
        "post_office_attachments",
        str(date.year),
        str(date.month),
        str(date.day),
        filename,
    )


class Attachment(models.Model):
    """
    A model describing an email attachment.
    """

    file = models.FileField(_("File"), upload_to=get_upload_path)
    name = models.CharField(
        _("Name"), max_length=255, help_text=_("The original filename")
    )
    emails = models.ManyToManyField(
        Email, related_name="attachments", verbose_name=_("Emails")
    )
    mimetype = models.CharField(max_length=255, default="", blank=True)
    headers = models.JSONField(_("Headers"), blank=True, null=True)

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

    def __str__(self):
        return self.name
