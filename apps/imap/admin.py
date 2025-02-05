from django.contrib import admin
from .models import IMAPAccount

@admin.register(IMAPAccount)
class IMAPAccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'imap_server', 'created_at')
    search_fields = ('email', 'imap_server')
    list_filter = ('use_ssl', 'created_at')