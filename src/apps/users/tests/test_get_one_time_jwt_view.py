from unittest import mock

from django.contrib.auth import get_user_model
from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from apps.users.tests.factories import UserFactory
from utils.tests import CustomViewTestCase

User = get_user_model()


class TestGetOneTimeJWT(CustomViewTestCase):
    """
    ./manage.py test apps.users.tests.test_get_one_time_jwt_view.TestGetOneTimeJWT --settings=_dev.settings_test        # noqa: E501
    """

    def setUp(self):
        self.url = reverse_lazy("users_api:get_one_time_jwt")

    @override_settings(CELERY_BROKER_URL=None)
    @mock.patch("apps.users.tasks.send_mail")
    def test_successful_jwt_generation(self, fake_send_mail_fct):
        user = UserFactory(
            email="user_verified@example.com",
            password="testpassword",
            is_active=True,
            is_verified=True,
        )
        response = self.client.post(self.url, {"email": user.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(fake_send_mail_fct.call_count, 1)
        self.assertIn("Successfully regenerated the new JWT.", response.data)

    def test_invalid_email(self, *args, **kwargs):
        response = self.client.post(self.url, {"email": "invalid@example.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid email.", response.data["error"])
