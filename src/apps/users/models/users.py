from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken


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


class User(AbstractUser):
    """User`s model"""

    email = models.EmailField(_("e-mail"), unique=True)
    is_verified = models.BooleanField(_("Email verified"), default=False)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_one_time_jwt_created = models.BooleanField(_("One-time JWT created"), default=False)

    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        ordering = ["-id"]

    def create_one_time_jwt(self):
        self.is_one_time_jwt_created = True

        try:
            with transaction.atomic():
                self.save()
                from ..serializers import TokenSerializer

                refresh = TokenSerializer(data={"username_field": self.USERNAME_FIELD}).get_token(
                    self
                )
        except Exception:
            self.is_one_time_jwt_created = False
            self.save()
            return {"error": _("Error with generation JWT")}, status.HTTP_400_BAD_REQUEST
        context = {
            "access": str(refresh.access_token),
        }
        return context, status.HTTP_200_OK
