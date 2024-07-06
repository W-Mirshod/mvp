from django.apps import AppConfig


class ChangelogConfig(AppConfig):
    name = 'apps.changelog'

    def ready(self):
        import apps.changelog.signals
