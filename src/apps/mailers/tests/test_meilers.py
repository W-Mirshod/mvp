from django.test import TestCase

from src.apps.mail_servers.models.servers import Server
from src.apps.mailers.choices import StatusType
from src.apps.mailers.models import Event, SentMessage
from src.apps.users.models.users import User


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

    def test_create_new_event(self):
        event = Event.create_new_event(
            user=self.user,
            server=self.server,
            template="Test Template",
            results={"key": "value"},
        )
        self.assertIsNotNone(event)
        self.assertEqual(event.server, self.server)
        self.assertEqual(event.status, StatusType.NEW)
        self.assertIsNotNone(event.sent_message)
        self.assertEqual(event.sent_message.user, self.user)
        self.assertEqual(event.sent_message.template, "Test Template")
        self.assertEqual(event.sent_message.results, {"key": "value"})
        self.assertEqual(event.sent_message.event_set.first(), event)
        sent_message = SentMessage.objects.get(id=event.sent_message.id)
        self.assertIsNotNone(sent_message)
        self.assertEqual(sent_message.user, self.user)
        self.assertEqual(sent_message.template, "Test Template")
        self.assertEqual(sent_message.results, {"key": "value"})
