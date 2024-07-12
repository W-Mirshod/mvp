from django.contrib import admin
from .models import SentMessage, Event


class SentMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'template', 'results')
    search_fields = ('user__username', 'template')
    list_filter = ('user',)


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'server', 'status', 'sent_message', 'created_at', 'updated_at')
    search_fields = ('server__type', 'status', 'sent_message__template')
    list_filter = ('status', 'server')


admin.site.register(SentMessage, SentMessageAdmin)
admin.site.register(Event, EventAdmin)
