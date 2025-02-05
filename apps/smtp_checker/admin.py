from django.contrib import admin
from apps.smtp_checker.models.models import SMTPCheckerSettings, SMTPCheckerTask, SMTPCheckerTaskResult

@admin.register(SMTPCheckerSettings)
class SMTPCheckerSettingsAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "threads_count", "connection_timeout")
    search_fields = ("user",)

@admin.register(SMTPCheckerTask)
class SMTPCheckerTaskAdmin(admin.ModelAdmin):
    list_display = ("user", "settings", "status")
    search_fields = ("user",)

@admin.register(SMTPCheckerTaskResult)
class SMTPCheckerTaskResultAdmin(admin.ModelAdmin):
    list_display = ("task", "server", "result", "response_time")
    search_fields = ("task",)
