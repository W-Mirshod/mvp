from django.db import models
from apps.users.models import User
from django.utils.translation import gettext_lazy as _
from .choices import ActionType


class ChangeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    url = models.URLField(null=True, blank=True)
    model_name = models.CharField(max_length=255)
    object_id = models.IntegerField()
    data = models.JSONField(verbose_name=_("Modifiable model data"), default=dict)
    action = models.CharField(max_length=50, choices=ActionType.choices())

    def __str__(self):
        return f'{self.model_name} {self.object_id} {self.action} by {self.user}'
