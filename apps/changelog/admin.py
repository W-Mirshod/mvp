from django.contrib import admin

from apps.changelog.models.models import ChangeLog


@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    list_display = (
        "changed",
        "model",
        "user",
        "record_id",
        "data",
        "ipaddress",
        "action_on_model",
    )
    readonly_fields = ("user",)
    list_filter = (
        "model",
        "action_on_model",
    )

    date_hierarchy = "changed"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True
