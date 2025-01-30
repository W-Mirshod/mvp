from email.mime.nonmultipart import MIMENonMultipart

from django.contrib.postgres.fields import ArrayField
from django.core.mail import get_connection
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db import models
from django.utils.encoding import smart_str
from django.utils.translation import pgettext_lazy, gettext_lazy as _

from apps.backend_mailer.logic.email_backend import EmailBackendManager
from apps.backend_mailer.logutils import setup_loghandlers
from apps.backend_mailer.settings import (
    context_field_class,
    get_log_level,
    get_template_engine,
    get_override_recipients,
)
from apps.backend_mailer.fields import decrypt_config
from apps.backend_mailer.validators import validate_email_with_name
from apps.backend_mailer.constants import BackendConstants
from apps.users.models import User

logger = setup_loghandlers("INFO")


class Email(models.Model):
    """
    A model to hold email information.
    """

    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="email_to_user",
        null=True,
        blank=True,
    )
    from_email = models.CharField(
        _("Email From"), max_length=254, validators=[validate_email_with_name]
    )
    to = ArrayField(
        models.EmailField(),
        blank=True,
        null=True,
        verbose_name=_("Email To"),
        help_text=_("Email To"),
    )
    cc = ArrayField(
        models.EmailField(),
        blank=True,
        null=True,
        verbose_name=_("Cc"),
        help_text=_("Cc"),
    )
    bcc = ArrayField(
        models.EmailField(),
        blank=True,
        null=True,
        verbose_name=_("Bcc"),
        help_text=_("Bcc"),
    )
    subject = models.CharField(_("Subject"), max_length=989, blank=True)
    message = models.TextField(_("Message"), blank=True)
    html_message = models.TextField(_("HTML Message"), blank=True)
    """
    Emails with 'queued' status will get processed by ``send_queued`` command.
    Status field will then be set to ``failed`` or ``sent`` depending on
    whether it's successfully delivered.
    """
    status = models.PositiveSmallIntegerField(
        _("Status"),
        choices=BackendConstants.STATUS_CHOICES,
        db_index=True,
        default=BackendConstants.STATUS.created,
        blank=True,
        null=True,
    )
    priority = models.PositiveSmallIntegerField(
        _("Priority"), choices=BackendConstants.PRIORITY_CHOICES, blank=True, null=True
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated = models.DateTimeField(db_index=True, auto_now=True)
    scheduled_time = models.DateTimeField(
        _("Scheduled Time"),
        blank=True,
        null=True,
        db_index=True,
        help_text=_("The scheduled sending time"),
    )
    expires_at = models.DateTimeField(
        _("Expires"),
        blank=True,
        null=True,
        help_text=_("Email won't be sent after this timestamp"),
    )
    message_id = models.CharField(
        "Message-ID", null=True, max_length=255, editable=False
    )
    number_of_retries = models.PositiveIntegerField(null=True, blank=True)
    headers = models.JSONField(_("Headers"), blank=True, null=True)
    template = models.ForeignKey(
        "backend_mailer.EmailTemplate",
        blank=True,
        null=True,
        verbose_name=_("Email template"),
        on_delete=models.CASCADE,
    )
    context = context_field_class(_("Context"), blank=True, null=True)
    render_on_delivery = models.BooleanField(default=False)
    message_type = models.PositiveSmallIntegerField(
        _("Message type"),
        choices=BackendConstants.MESSAGE_TYPE_CHOICES,
        default=BackendConstants.MESSAGE_TYPE.text,
    )
    email_backend = models.ForeignKey(
        to="backend_mailer.EmailBackend",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Email backend"),
    )

    class Meta:

        verbose_name = pgettext_lazy("Email address", "Email")
        verbose_name_plural = pgettext_lazy("Email addresses", "Emails")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_email_message = None
        self.connection = None

    def __str__(self):
        return "%s" % self.to

    def create_connection(self):
        try:
            encrypt_config = self.email_backend.config
            backend_config = decrypt_config(value=encrypt_config)

            backend_class = BackendConstants.EMAIL_BACKENDS_CHOICES_DICT.get(
                self.email_backend.backend_type
            )

            data = EmailBackendManager.get_backend_fields(
                backend_type=self.email_backend.backend_type, config=backend_config
            )

            self.connection = get_connection(backend=backend_class, **data)

            logger.info(f"Connection {self.connection}.")
        except Exception as e:
            logger.error(f"Failed to create connection: {e}")
            raise

    def email_message(
        self,
    ):
        """
        Returns Django EmailMessage object for sending.
        """
        if self._cached_email_message:
            return self._cached_email_message

        return self.prepare_email_message()

    def prepare_email_message(self):
        """
        Returns a django ``EmailMessage`` or ``EmailMultiAlternatives`` object,
        depending on whether html_message is empty.
        """
        if get_override_recipients():
            self.to = get_override_recipients()

        if self.template is not None and self.context is not None:
            engine = get_template_engine()
            subject = engine.from_string(self.template.subject).render(self.context)
            plaintext_message = engine.from_string(self.template.content).render(
                self.context
            )
            multipart_template = engine.from_string(self.template.html_content)
            html_message = multipart_template.render(self.context)

        else:
            subject = smart_str(self.subject)
            plaintext_message = self.message
            multipart_template = None
            html_message = self.html_message

        if isinstance(self.headers, dict) or self.expires_at or self.message_id:
            headers = dict(self.headers or {})
            if self.expires_at:
                headers.update(
                    {"Expires": self.expires_at.strftime("%a, %-d %b %H:%M:%S %z")}
                )
            if self.message_id:
                headers.update({"Message-ID": self.message_id})
        else:
            headers = None

        self.create_connection()
        connection = self.connection

        if html_message:
            if plaintext_message:
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=plaintext_message,
                    from_email=self.from_email,
                    to=self.to,
                    bcc=self.bcc,
                    cc=self.cc,
                    headers=headers,
                    connection=connection,
                )
                msg.attach_alternative(html_message, "text/html")
            else:
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=html_message,
                    from_email=self.from_email,
                    to=self.to,
                    bcc=self.bcc,
                    cc=self.cc,
                    headers=headers,
                    connection=connection,
                )
                msg.content_subtype = "html"
            if hasattr(multipart_template, "attach_related"):
                multipart_template.attach_related(msg)

        else:
            msg = EmailMessage(
                subject=subject,
                body=plaintext_message,
                from_email=self.from_email,
                to=self.to,
                bcc=self.bcc,
                cc=self.cc,
                headers=headers,
                connection=connection,
            )

        for attachment in self.attachments.all():
            if attachment.headers:
                mime_part = MIMENonMultipart(*attachment.mimetype.split("/"))
                mime_part.set_payload(attachment.file.read())
                for key, val in attachment.headers.items():
                    try:
                        mime_part.replace_header(key, val)
                    except KeyError:
                        mime_part.add_header(key, val)
                msg.attach(mime_part)
            else:
                msg.attach(
                    attachment.name,
                    attachment.file.read(),
                    mimetype=attachment.mimetype or None,
                )
            attachment.file.close()

        self._cached_email_message = msg
        return msg

    def dispatch(self, log_level=None, disconnect_after_delivery=True, commit=True):
        """
        Sends email and log the result.
        """
        try:
            self.email_message().send()
            status = BackendConstants.STATUS.sent
            message = ""
            exception_type = ""
        except Exception as e:
            status = BackendConstants.STATUS.failed
            message = str(e)
            exception_type = type(e).__name__

            if commit:
                logger.exception("Failed to send email")
            else:
                # If run in a bulk sending mode, re-raise and let the outer
                # layer handle the exception
                raise

        if disconnect_after_delivery:
            self.connection.close()

        if commit:
            self.status = status
            self.save(update_fields=["status"])

            if log_level is None:
                log_level = get_log_level()

            # If log level is 0, log nothing, 1 logs only sending failures
            # and 2 means log both successes and failures
            if log_level == 1:
                if status == BackendConstants.STATUS.failed:
                    self.logs.create(
                        status=status, message=message, exception_type=exception_type
                    )
            elif log_level == 2:
                self.logs.create(
                    status=status, message=message, exception_type=exception_type
                )

        return status

    def clean(self):
        if (
            self.scheduled_time
            and self.expires_at
            and self.scheduled_time > self.expires_at
        ):
            raise ValidationError(
                _("The scheduled time may not be later than the expires time.")
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
