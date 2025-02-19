import logging

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.forms import UserCreationForm
from apps.users.models.tariffs import UserTariff
from apps.users.models.users import User

logger = logging.getLogger(__name__)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
        "role",
        "is_active",
        "is_verified",
        "jwt_max_out",
        "is_one_time_jwt_created",
        "telegram_username",
        "gender",
        "birth_date",
        "bio",
        "avatar",
    )
    search_fields = ("email",)
    list_per_page = 25
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "role",
                    "telegram_username",
                    "gender",
                    "birth_date",
                    "bio",
                    "avatar",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
        (
            _("JWT"),
            {
                "fields": (
                    "is_one_time_jwt_created",
                    "jwt_max_out",
                )
            },
        ),
        (
            _("Important dates"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )
    readonly_fields = (
        "last_login",
        "date_joined",
    )
    add_form = UserCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display_links = (
        "email",
        "id",
    )
    list_filter = (
        "is_active",
        "is_verified",
    )
    ordering = ("email",)


@admin.register(UserTariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ("user", "tariff", "expired_at")
