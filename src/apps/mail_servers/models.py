from django.db import models

class MailServer(models.Model):
    url = models.URLField()
    port = models.IntegerField()
    password = models.CharField(max_length=255)
    queries_per_sec = models.IntegerField()

    class Meta:
        abstract = True

class SMTPServer(MailServer):
    pass

class IMAPServer(MailServer):
    pass

class ProxyServer(MailServer):
    pass
