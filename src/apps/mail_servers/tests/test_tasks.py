from django.test import TestCase
from apps.mail_servers.tasks import test_periodic_task


class TestPeriodicTask(TestCase):
    def test_periodic_task(self):
        result = test_periodic_task.delay()
        self.assertEqual(result.get(), "Periodic task executed")

