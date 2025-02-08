from django.contrib import admin

from apps.proxies.models.proxies import Proxy


@admin.register(Proxy)
class ProxyAdmin(admin.ModelAdmin):
    list_display = (
        "host",
        "port",
        "is_active",
        "country_code",
        "anonymity",
        "timeout",
        "username",
        "password",
        "author",
    )
    list_filter = (
        "is_active",
        "timeout",
    )
    search_fields = (
        "is_active",
        "author",
        "anonymity",
    )
    ordering = ("-id",)
    filter_horizontal = ("countries",)
