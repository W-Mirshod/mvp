from django.apps import AppConfig
from health_check.plugins import plugin_dir

from apps.companies.health_check.v1.hl_ch_companies import CompaniesHealthCheck


class CompaniesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.companies"

    def ready(self):

        plugin_dir.register(CompaniesHealthCheck)
