from django.contrib import admin

from apps.notify.models import Notification
from config.settings import DEBUG


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "id",
        "user",
        "created_at",
    )
    search_fields = ("user__email",)

    def has_delete_permission(self, request, obj=None):
        return DEBUG or request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return DEBUG

    def has_change_permission(self, request, obj=None):
        return DEBUG
