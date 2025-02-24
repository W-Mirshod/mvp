from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.utils.translation import gettext_lazy as _

from apps.changelog.mixins import ChangeloggableMixin
from apps.changelog.signals import journal_save_handler, journal_delete_handler
from apps.users.choices import UserConstance


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        if password is None:
            raise TypeError(_("Password should not be none"))

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, **extra_fields)


class User(ChangeloggableMixin, AbstractUser):
    """User`s model"""

    email = models.EmailField(_("e-mail"), unique=True, db_index=True)
    is_verified = models.BooleanField(_("Email verified"), default=False)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_one_time_jwt_created = models.BooleanField(
        _("One-time JWT created"), default=False
    )
    jwt_max_out = models.DateTimeField(blank=True, null=True)

    role = models.CharField(
        max_length=55,
        choices=UserConstance.USER_ROLES_CHOICES,
        default=UserConstance.USER,
    )

    telegram_id = models.BigIntegerField(
        _("Telegram ID"), unique=True, blank=True, null=True
    )

    telegram_username = models.CharField(
        max_length=UserConstance.TG_USERNAME_MAX_LENGTH, blank=True, null=True
    )
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(
        null=True,
        upload_to="users",
        validators=[FileExtensionValidator(allowed_extensions=["jpeg", "jpg", "png"])],
    )
    position = models.CharField(
        max_length=35,
        choices=UserConstance.USER_POSITION_CHOICES,
        default=UserConstance.NEW,
    )
    mailing_experience = models.CharField(
        max_length=55,
        choices=UserConstance.MAILING_EXPERIENCE_CHOICES,
        default=UserConstance.NO_EXPERIENCE,
    )
    working_area = models.CharField(
        max_length=55,
        choices=UserConstance.WORKING_AREA_CHOICES,
        default=UserConstance.REMOTE,
    )
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta(AbstractUser.Meta):

        ordering = ("-id",)

    def restore_password(self, new_password: str):
        self.set_password(new_password)


post_save.connect(journal_save_handler, sender=User)
post_delete.connect(journal_delete_handler, sender=User)
