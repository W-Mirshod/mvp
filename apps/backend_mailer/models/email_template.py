from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.backend_mailer import cache
from apps.backend_mailer.logutils import setup_loghandlers
from apps.backend_mailer.validators import validate_template_syntax


logger = setup_loghandlers("INFO")


class EmailTemplateManager(models.Manager):
    def get_by_natural_key(self, name, language, default_template):
        return self.get(name=name, language=language, default_template=default_template)


class EmailTemplate(models.Model):
    """
    Model to hold template information from db
    """

    name = models.CharField(
        _("Name"), max_length=255, help_text=_("e.g: 'welcome_email'")
    )
    description = models.TextField(
        _("Description"), blank=True, help_text=_("Description of this template.")
    )
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    subject = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Subject"),
        validators=[validate_template_syntax],
    )
    content = models.TextField(
        blank=True, verbose_name=_("Content"), validators=[validate_template_syntax]
    )
    html_content = models.TextField(
        blank=True,
        verbose_name=_("HTML content"),
        validators=[validate_template_syntax],
    )
    language = models.CharField(
        max_length=12,
        verbose_name=_("Language"),
        help_text=_("Render template in alternative language"),
        default="",
        blank=True,
    )
    default_template = models.ForeignKey(
        "self",
        related_name="translated_templates",
        null=True,
        default=None,
        verbose_name=_("Default template"),
        on_delete=models.CASCADE,
    )

    objects = EmailTemplateManager()

    class Meta:

        unique_together = ("name", "language", "default_template")
        verbose_name = _("Email Template")
        verbose_name_plural = _("Email Templates")
        ordering = ["name"]

    def __str__(self):
        return "%s %s" % (self.name, self.language)

    def natural_key(self):
        return (self.name, self.language, self.default_template)

    def save(self, *args, **kwargs):
        # If template is a translation, use default template's name
        if self.default_template and not self.name:
            self.name = self.default_template.name

        template = super().save(*args, **kwargs)
        cache.delete(self.name)
        return template
