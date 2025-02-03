from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_delete

from apps.changelog.mixins import ChangeloggableMixin
from apps.changelog.signals import journal_save_handler, journal_delete_handler
from apps.proxies.models.countries import Country
from apps.proxies.models.judges import Judge

from utils.models import DateModelMixin, DeleteModelMixin


class ProxyConfig(ChangeloggableMixin, DateModelMixin, DeleteModelMixin):
    ANONYMITY_CHOICES = (
        ("TRANSPARENT", "Transparent"),
        ("ELITE", "Elite"),
        ("ANONYMOUS", "Anonymous")
    )

    author = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proxy_config')
    judge = models.ManyToManyField(Judge)
    timeout = models.PositiveSmallIntegerField()
    countries = models.ManyToManyField(Country)
    anonymity = models.CharField(max_length=20, choices=ANONYMITY_CHOICES)

post_save.connect(journal_save_handler, sender=ProxyConfig)
post_delete.connect(journal_delete_handler, sender=ProxyConfig)
