from django.db import models

from apps.mail_servers.models.servers import Server
from apps.mailers.choices import StatusType
from apps.mailers.models.message import SentMessage

from utils.models import DateModelMixin, DeleteModelMixin




class Event(DeleteModelMixin, DateModelMixin, models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=StatusType.CHOICES, default=StatusType.NEW
    )
    sent_message = models.ForeignKey(SentMessage, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create_new_event(cls, user, server, template="", results=None):
        if results is None:
            results = {}
        sent_message = SentMessage.objects.create(
            user=user, template=template, results=results
        )
        event = cls.objects.create(
            server=server, status=StatusType.NEW, sent_message=sent_message
        )
        return event
