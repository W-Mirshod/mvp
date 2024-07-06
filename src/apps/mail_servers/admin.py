from django.contrib import admin
from .models import SMTPServer, IMAPServer, ProxyServer

admin.site.register(SMTPServer)
admin.site.register(IMAPServer)
admin.site.register(ProxyServer)
