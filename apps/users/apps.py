from django.apps import AppConfig
from health_check.plugins import plugin_dir

from apps.users.health_check.v1.hc_user import UserHealthCheck


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"

    def ready(self):

        plugin_dir.register(UserHealthCheck)
