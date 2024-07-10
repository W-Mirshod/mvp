from django.contrib import admin

from .models import IMAPServer, MessageTemplate, ProxyServer, SMTPServer

admin.site.register(SMTPServer)
admin.site.register(IMAPServer)
admin.site.register(ProxyServer)
admin.site.register(MessageTemplate)
