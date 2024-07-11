from django.contrib import admin

from .models import IMAPServer, ProxyServer, SMTPServer


@admin.register(SMTPServer)
class SMTPServerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "url",
        "port",
        "username",
        "password",
        "email_use_tls",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "port",
        "is_active",
        "url",
    )
    search_fields = (
        "url",
        "username",
        "port",
    )
    ordering = ("-id",)


@admin.register(IMAPServer)
class IMAPServerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "url",
        "port",
        "username",
        "password",
        "email_use_tls",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "port",
        "is_active",
        "url",
    )
    search_fields = (
        "url",
        "username",
        "port",
    )
    ordering = ("-id",)


@admin.register(ProxyServer)
class ProxyServerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "url",
        "port",
        "username",
        "password",
        "email_use_tls",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "port",
        "is_active",
        "url",
    )
    search_fields = (
        "url",
        "username",
        "port",
    )
    ordering = ("-id",)
