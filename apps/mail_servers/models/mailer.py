from django.db import models


class Session(models.Model):
    name = models.CharField(max_length=255, null=True)


class Base(models.Model):
    first = models.CharField(max_length=255, null=True)
    last = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    session = models.ForeignKey(
        to=Session,
        on_delete=models.SET_NULL,
        related_name="session_to_base",
        null=True,
        blank=True,
    )

    status = models.CharField(max_length=255, null=True, default="new")

    class Meta:
        db_table = "bases"
        indexes = [
            models.Index(fields=["session", "email"]),
            models.Index(fields=["status"]),
        ]


class Domain(models.Model):
    url = models.TextField(null=True)
    status = models.CharField(max_length=255, null=True)
    session = models.ForeignKey(
        to=Session,
        on_delete=models.SET_NULL,
        related_name="session_to_domain",
        null=True,
        blank=True,
    )
    tempName = models.CharField(max_length=255, null=True)
    template = models.ForeignKey("Template", on_delete=models.SET_NULL, null=True)


class Manifest(models.Model):
    name = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)


class Material(models.Model):
    manifest = models.CharField(max_length=255, null=True)
    data = models.TextField(null=True)


class Proxy(models.Model):
    ip = models.CharField(max_length=255, null=True)
    port = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True, default="new")
    session = models.ForeignKey(
        to=Session,
        on_delete=models.SET_NULL,
        related_name="session_to_proxy",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "proxy"
        indexes = [
            models.Index(fields=["session", "ip"]),
            models.Index(fields=["status"]),
        ]


class SMTP(models.Model):
    server = models.CharField(max_length=255, null=True)
    port = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True, default="new")
    session = models.ForeignKey(
        to=Session,
        on_delete=models.SET_NULL,
        related_name="session_to_smtp",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "smtp"

    def __str__(self):
        return f"{self.server} ({self.email})"


class Template(models.Model):
    maintmp = models.IntegerField(null=True)
    template = models.TextField(null=True)
    froms = models.TextField(null=True)
    subject = models.TextField(null=True)
    status = models.CharField(max_length=255, null=True)
    session = models.ForeignKey(
        to=Session,
        on_delete=models.SET_NULL,
        related_name="session_to_template",
        null=True,
        blank=True,
    )
    htmlbodies = models.TextField(null=True)


class Temp(models.Model):
    tempName = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    session = models.ForeignKey(
        to=Session,
        on_delete=models.SET_NULL,
        related_name="session_to_temp",
        null=True,
        blank=True,
    )


class Log(models.Model):
    text = models.TextField(null=True)
    type = models.CharField(max_length=255, null=True)
    session = models.ForeignKey(
        to=Session,
        on_delete=models.SET_NULL,
        related_name="session_to_log",
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class IMAP(models.Model):
    server = models.CharField(max_length=255, null=True)
    port = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    session = models.ForeignKey(
        to=Session,
        on_delete=models.SET_NULL,
        related_name="session_to_imap",
        null=True,
        blank=True,
    )


class Setting(models.Model):
    session = models.ForeignKey(
        to=Session,
        on_delete=models.CASCADE,
        related_name="session_to_setting",
    )
    type = models.CharField(max_length=255)
    data = models.IntegerField(null=True)

    class Meta:
        unique_together = ("session", "type")


class IPBlacklist(models.Model):
    ip = models.CharField(max_length=45, unique=True)
    reason = models.TextField()
    attempts = models.IntegerField(default=0)
    blocked_until = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ip_blacklist"
        verbose_name = "IP Blacklist"
        verbose_name_plural = "IP Blacklist"

    def __str__(self):
        return f"{self.ip} ({self.reason})"

