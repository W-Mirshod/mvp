import logging
from django.core.exceptions import ImproperlyConfigured
from apps.mail_servers.drivers.utils import chunks
from apps.mail_servers.models.servers import Server
from apps.backend_mailer.models import EmailBackend

logger = logging.getLogger(__name__)


class BaseDriver:
    def __init__(self, server_name):
        if not self.enable:
            return None
        self.server_name = server_name
        self.server = Server.objects.get(url=self.server_name, is_deleted=False)
        self.settings = self.get_server_settings()

    def get_server_settings(self):
        raise ImproperlyConfigured("Subclasses must implement this method")

    def send_mail(self, subject, message, recipient_list):
        raise ImproperlyConfigured("Subclasses must implement this method")

    def process_queue(self, status: str, server: Server, email_backend: EmailBackend ):
        raise ImproperlyConfigured("Subclasses must implement this method")

    def get_driver(self, driver_type):
        raise ImproperlyConfigured("Subclasses must implement this method")

    def login(self):
        raise ImproperlyConfigured("Subclasses must implement this method")

    def plural_login(self, user_list, chunk_size):
        for chunk in chunks(user_list, chunk_size):
            self.login_chunk(chunk)

    def send_message(self):
        raise ImproperlyConfigured("Subclasses must implement this method")

    def send_messages(self, messages, chunk_size):
        for chunk in chunks(messages, chunk_size):
            self.send_messages_chunk(chunk)

    def logout(self):
        raise ImproperlyConfigured("Subclasses must implement this method")

    def check_connection(self):
        raise ImproperlyConfigured("Subclasses must implement this method")

    @property
    def _settings(self):
        raise ImproperlyConfigured("Subclasses must implement this property")

    @property
    def enable(self):
        raise ImproperlyConfigured("Subclasses must implement this property")
