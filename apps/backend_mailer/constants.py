from collections import namedtuple
from django.utils.translation import gettext_lazy as _


class BackendConstants:
    """EMAIL PRIORITY ->"""

    PRIORITY = namedtuple("PRIORITY", "low medium high now")._make(range(4))

    PRIORITY_CHOICES = [
        (PRIORITY.low, _("low")),
        (PRIORITY.medium, _("medium")),
        (PRIORITY.high, _("high")),
        (PRIORITY.now, _("now")),
    ]
    """<- EMAIL PRIORITY"""

    """ EMAIL STATUS -> """
    STATUS = namedtuple("STATUS", "sent failed queued requeued created")._make(range(5))

    STATUS_CHOICES = [
        (STATUS.created, _("created")),
        (STATUS.sent, _("sent")),
        (STATUS.failed, _("failed")),
        (STATUS.queued, _("queued")),
        (STATUS.requeued, _("requeued")),
    ]
    """<- EMAIL STATUS"""
    """ MESSAGE TYPE ->"""
    MESSAGE_TYPE = namedtuple("MESSAGE_TYPE", "text html")._make(range(2))

    MESSAGE_TYPE_CHOICES = [
        (MESSAGE_TYPE.text, _("text")),
        (MESSAGE_TYPE.html, _("html")),
    ]

    """ <-MESSAGE TYPE"""
    """ LOG STATUS ->"""
    LOG_STATUS_CHOICES = [(STATUS.sent, _("sent")), (STATUS.failed, _("failed"))]

    """<- LOG STATUS"""

    """MAILING TYPE  ->"""

    DEFAULT_MAILING_TYPE = 1
    SES_MAILING_TYPE = 2
    ANY_MAIL_MAILING_TYPE = 3
    SMTP_MAILING_TYPE = 4
    GMAIL_MAILING_TYPE = 5

    MAILING_TYPE_CHOICES = (
        (DEFAULT_MAILING_TYPE, "Default"),
        (SES_MAILING_TYPE, "SES"),
        (ANY_MAIL_MAILING_TYPE, "AnyMail 3"),
        (SMTP_MAILING_TYPE, "SMTP"),
        (GMAIL_MAILING_TYPE, "G-Mail 5"),
    )

    MAILING_TYPE_IDS = [i[0] for i in MAILING_TYPE_CHOICES]
    """< - MAILING TYPE """

    """ EMAIL BACKENDS ->"""

    DEFAULT_EMAIL_BACKEND = 1
    SES_EMAIL_BACKEND = 2
    SMTP_EMAIL_BACKEND = 3
    ANYMAIL_EMAIL_BACKEND = 4

    EMAIL_BACKENDS_CHOICES = (
        (DEFAULT_EMAIL_BACKEND, "django.core.mail.backends.smtp.EmailBackend"),
        (SES_EMAIL_BACKEND, "django_ses.SESBackend"),
        (SMTP_EMAIL_BACKEND, "django.core.mail.backends.smtp.EmailBackend"),
        (ANYMAIL_EMAIL_BACKEND, "anymail.backends.amazon_ses.EmailBackend"),
    )

    EMAIL_BACKENDS_IDS = [i[0] for i in EMAIL_BACKENDS_CHOICES]
    EMAIL_BACKENDS_CHOICES_DICT = dict(EMAIL_BACKENDS_CHOICES)

    BACKEND_FIELDS = {
        EMAIL_BACKENDS_CHOICES_DICT.get(DEFAULT_EMAIL_BACKEND): [
            "host",
            "port",
            "username",
            "password",
            "use_tls",
        ],
        EMAIL_BACKENDS_CHOICES_DICT.get(SMTP_EMAIL_BACKEND): [
            "host",
            "port",
            "username",
            "password",
            "use_tls",
        ],
        EMAIL_BACKENDS_CHOICES_DICT.get(SES_EMAIL_BACKEND): [
            "aws_access_key_id",
            "aws_secret_access_key",
            "region",
        ],
        EMAIL_BACKENDS_CHOICES_DICT.get(ANYMAIL_EMAIL_BACKEND): [
            "aws_access_key_id",
            "aws_secret_access_key",
            "region",
            "session_token",
        ],
    }

    """<- EMAIL BACKENDS"""
