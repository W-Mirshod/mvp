from django.test import TestCase
from apps.mailers.models import SentMessage, Event
from apps.users.models import User
from apps.mail_servers.models.models_servers import Server
from apps.mailers.choices import StatusType


class EventModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com', password='password')
        self.server = Server.objects.create(
            type='SMTP',
            url='smtp.example.com',
            port=587,
            password='password',
            username='user@example.com',
            email_use_tls=True,
            is_active=True
        )

    def test_create_new_event(self):
        event = Event.create_new_event(user=self.user, server=self.server, template='Test Template',
                                       results={'key': 'value'})
        self.assertIsNotNone(event)
        self.assertEqual(event.server, self.server)
        self.assertEqual(event.status, StatusType.NEW)
        self.assertIsNotNone(event.sent_message)
        self.assertEqual(event.sent_message.user, self.user)
        self.assertEqual(event.sent_message.template, 'Test Template')
        self.assertEqual(event.sent_message.results, {'key': 'value'})
        self.assertEqual(event.sent_message.event_set.first(), event)
