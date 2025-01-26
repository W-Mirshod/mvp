from threading import local
from typing import Dict

from django.core.mail import get_connection
from django.core.mail.backends.base import BaseEmailBackend

from apps.backend_mailer.settings import get_backend


# Copied from Django 1.8's django.core.cache.CacheHandler
class ConnectionHandler:
    """
    A Cache Handler to manage access to Cache instances.

    Ensures only one instance of each alias exists per thread.
    """

    def __init__(self):
        self._connections = local()

    def __getitem__(self, alias):
        try:
            return self._connections.connections[alias]
        except AttributeError:
            self._connections.connections = {}
        except KeyError:
            pass

        try:
            backend = get_backend(alias)
        except KeyError:
            raise KeyError("%s is not a valid backend alias" % alias)

        connection = get_connection(backend)
        connection.open()
        self._connections.connections[alias] = connection
        return connection

    def all(self):
        return getattr(self._connections, "connections", {}).values()

    def close(self):
        for connection in self.all():
            connection.close()


def dynamic_backend(backend_type: str, data: Dict) -> BaseEmailBackend:

    backend_type_dict = {
        "default": "django.core.mail.backends.smtp.EmailBackend",
        "aws_backend": "django_ses.SESBackend",
        "smtp": "django.core.mail.backends.smtp.EmailBackend",
    }

    backend_class = backend_type_dict.get(
        backend_type, "django.core.mail.backends.smtp.EmailBackend"
    )

    connection = get_connection(backend_class, **data)

    return connection


connections = ConnectionHandler()
