from django.db import models


class MailServer(models.Model):
    url = models.URLField()
    port = models.IntegerField()
    password = models.CharField(max_length=255)

    class Meta:
        abstract = True


class SMTPServer(MailServer):
    username = models.EmailField(default='default_smtp@example.com')
    email_use_tls = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)


class IMAPServer(MailServer):
    username = models.EmailField(default='default_imap@example.com')
    email_use_tls = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)


class ProxyServer(MailServer):
    username = models.EmailField(default='default_proxy@example.com')
    email_use_tls = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)


class MessageTemplate(models.Model):
    is_deleted = models.BooleanField(default=False)
    from_address = models.CharField(max_length=255, blank=True, null=True)
    template = models.TextField(blank=True, null=True)
    message = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)