from django.utils.translation import gettext_lazy as _


class UserConstance:

    TG_USERNAME_MAX_LENGTH = 255

    """ User roles -> """
    TECH = "tech"
    STAFF = "staff"
    SUPER_STAFF = "super_staff"
    ADMIN = "admin"
    USER = "user"

    USER_ROLES_CHOICES = (
        (TECH, _("Tech")),
        (STAFF, _("Staff")),
        (SUPER_STAFF, _("Super_staff")),
        (ADMIN, _("ADMIN")),
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

    """ <- User roles"""

    """ User positions -> """
    NEW = "new"
    MEMBER = "member"
    SALE = "sale"

    USER_POSITION_CHOICES = (
        (NEW, _("New")),
        (MEMBER, _("Member")),
        (SALE, _("Sale")),
    )

    """ <- User positions"""
