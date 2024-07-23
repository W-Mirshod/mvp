from django.contrib import admin

from .models import Event, SentMessage
from .models.template import MessageTemplate


@admin.register(SentMessage)
class SentMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "template", "results")
    search_fields = ("user__username", "template")
    list_filter = ("user",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "server", "status", "sent_message", "created_at", "updated_at")
    search_fields = ("server__type", "status", "sent_message__template")
    list_filter = ("status", "server")


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "from_address",
        "is_deleted",
        "created_at",
        "updated_at",
    )
    search_fields = ("from_address",)
    list_filter = (
        "from_address",
        "is_deleted",
    )
