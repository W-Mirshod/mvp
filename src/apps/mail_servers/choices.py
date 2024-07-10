from django.utils.translation import gettext_lazy as _


class ServerType:
    """
    Type of the server
    """

    SMTP = "smpt"
    IMAP = "imap"
    PROXY = "proxy"

    ITEMS = [SMTP, IMAP, PROXY]

    CHOICES = (
        (SMTP, _("SMTP")),
        (IMAP, _("IMAP")),
        (PROXY, _("PROXY")),
    )
