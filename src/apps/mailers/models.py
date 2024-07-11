from django.db import models
from apps.users.models import User
from .choices import StatusType
from apps.mail_servers.models.models_servers import Server
from utils.models import DateModelMixin, DeleteModelMixin


class SentMessage(DeleteModelMixin, DateModelMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    template = models.TextField(blank=True, null=True)
    results = models.JSONField(blank=True, null=True)


class Event(DeleteModelMixin, DateModelMixin, models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=StatusType.CHOICES, default=StatusType.NEW)
    sent_message = models.ForeignKey(SentMessage, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
