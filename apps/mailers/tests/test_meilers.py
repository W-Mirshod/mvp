from django.test import TestCase

from apps.mail_servers.models.servers import Server
from apps.mailers.choices import StatusType
from apps.mailers.models import MessageTemplate
from apps.mailers.models.event import Event
from apps.mailers.models.message import SentMessage
from apps.users.models import User


class EventModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="testuser@example.com", password="password"
        )
        self.server = Server.objects.create(
            type="SMTP",
            url="smtp.example.com",
            port=587,
            password="password",
            username="user@example.com",
            email_use_tls=True,
            is_active=True,
        )
        self.message = MessageTemplate.objects.create(
            from_address="user@example.com",
            template="Test Template",
            message="Test Template"
        )
    def test_create_new_event(self):
        event = Event.create_new_event(
            user=self.user,
            server=self.server,
            template=self.message,
            results={"key": "value"},
        )
        self.assertIsNotNone(event)
        self.assertEqual(event.server, self.server)
        self.assertEqual(event.status, StatusType.NEW)
        self.assertIsNotNone(event.sent_message)
        self.assertEqual(event.sent_message.user, self.user)
        self.assertEqual(event.sent_message.template.template, "Test Template")
        self.assertEqual(event.sent_message.results, {"key": "value"})
        self.assertEqual(event.sent_message.event_set.first(), event)
        sent_message = SentMessage.objects.get(id=event.sent_message.id)
        self.assertIsNotNone(sent_message)
        self.assertEqual(sent_message.user, self.user)
        self.assertEqual(sent_message.template.template, "Test Template")
        self.assertEqual(sent_message.results, {"key": "value"})
