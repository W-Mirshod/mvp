from django.contrib import admin
from .models import ChangeLog


@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'model_name', 'user', 'object_id', 'data_changes', 'url', 'action')
    readonly_fields = ('datetime', 'model_name', 'user', 'object_id', 'data_changes', 'url', 'action')
    list_filter = ('model_name', 'action')
    search_fields = ('model_name', 'user__username', 'object_id', 'action')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True
