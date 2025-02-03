from django.contrib import admin

from .models.proxies import Proxy


@admin.register(Proxy)
class ProxyAdmin(admin.ModelAdmin):
    list_display = (
        "host",
        "port",
        "is_active",
        "country",
        "country_code",
        "anonymity",
        "timeout",
        "username",
        "password",
        "author",
    )
    list_filter = (
        "is_active",
        "country",
        "timeout",
    )
    search_fields = (
        "is_active",
        "author",
        "anonymity",
    )
    ordering = ("-id",)
