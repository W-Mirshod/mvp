from django.utils.translation import gettext_lazy as _


class UserRoles:
    """
    User roles
    """

    STUFF = "stuff"
    ADMIN = "admin"
    USER = "user"
    OWNER_COMPANY = "owner_company"

    ITEMS = [STUFF, ADMIN, USER, OWNER_COMPANY]

    CHOICES = (
        (STUFF, _("STUFF")),
        (ADMIN, _("ADMIN")),
        (USER, _("USER")),
        (OWNER_COMPANY, _("OWNER_COMPANY")),
    )
