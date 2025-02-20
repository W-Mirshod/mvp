from django.utils.translation import gettext_lazy as _


class UserConstance:

    TG_USERNAME_MAX_LENGTH = 255

    """ User roles -> """
    STUFF = "stuff"
    ADMIN = "admin"
    USER = "user"
    OWNER_COMPANY = "owner_company"
    SUPPORT = "support"

    ITEMS = [STUFF, ADMIN, USER, OWNER_COMPANY, SUPPORT]

    USER_ROLES_CHOICES = (
        (STUFF, _("STUFF")),
        (ADMIN, _("ADMIN")),
        (USER, _("USER")),
        (OWNER_COMPANY, _("OWNER_COMPANY")),
        (SUPPORT, _("SUPPORT")),
    )

    """ <- User roles"""

    """ User gender -> """
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    NON_BINARY = "non-binary"

    USER_GENDER_CHOICES = (
        (MALE, _("Male")),
        (FEMALE, _("Female")),
        (OTHER, _("Other")),
        (NON_BINARY, _("binary")),
    )

    """ <- User gender"""
