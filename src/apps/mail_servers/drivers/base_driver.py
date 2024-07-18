from django.core.exceptions import ImproperlyConfigured

from apps.mail_servers.models.servers import Server
from apps.mailers.choices import StatusType
from apps.mailers.models import Event
from utils.chunks import chunks


class BaseDriver:
    def __init__(self, server_name):
        self.server_name = server_name
        self.server = Server.objects.get(url=self.server_name)
        self.settings = self.get_server_settings()

    def get_server_settings(self):
        raise ImproperlyConfigured("Subclasses must implement this method")

    def send_mail(self, subject, message, recipient_list):
        raise ImproperlyConfigured("Subclasses must implement this method")

    def add_message_to_queue(self, subject, message, recipient_list):
        Event.create_new_event(
            user=None,
            server=self.server,
            template=message,
            results={"subject": subject, "recipient_list": recipient_list},
        )

    def process_queue(self):
        events = Event.objects.filter(server=self.server, status=StatusType.NEW)
        for event in events:
            self.send_mail(
                subject=event.sent_message.results["subject"],
                message=event.sent_message.template,
                recipient_list=event.sent_message.results["recipient_list"],
            )
            event.status = StatusType.IN_PROCESS
            event.save()

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
