from django.db import models
from django.utils.translation import gettext_lazy as _

from .users import User


class BlackListedAccessToken(models.Model):
    jti = models.CharField(unique=True, max_length=255)
    jti_refresh = models.CharField(unique=True, max_length=255)
    token = models.TextField()
    user = models.ForeignKey(
        User, related_name="blacklisted_access_token_users", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("BlackListed access token")
        verbose_name_plural = _("BlackListed access tokens")
        unique_together = ("token", "user")
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"Blacklisted access token for {self.user} ({self.jti})"
