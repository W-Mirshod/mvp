from django.db import models


class MailServer(models.Model):
    url = models.URLField()
    port = models.IntegerField()
    password = models.CharField(max_length=255)

    class Meta:
        abstract = True


class SMTPServer(MailServer):
    pass


class IMAPServer(MailServer):
    pass


class ProxyServer(MailServer):
    pass


class MessageTemplate(models.Model):
    is_deleted = models.BooleanField(default=False)
    from_address = models.CharField(max_length=255, blank=True, null=True)
    template = models.TextField(blank=True, null=True)
    message = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
