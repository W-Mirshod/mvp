from django.apps import AppConfig
from health_check.plugins import plugin_dir

from apps.mailers.health_check.v1.hс_sent_message import SentMessagesHealthCheck
from apps.mailers.health_check.v1.hс_message_template import MessageTemplateHealthCheck


class MailersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.mailers"

    def ready(self):

        plugin_dir.register(SentMessagesHealthCheck)
        plugin_dir.register(MessageTemplateHealthCheck)
