import json
from datetime import timedelta, timezone as dt_timezone

from django.conf import settings
from django.contrib.auth import get_user, get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse, reverse_lazy

from utils.tests import CustomViewTestCase

from .factories import UserFactory

User = get_user_model()


class EmailVerificationViewTests(CustomViewTestCase):
    """
    ./manage.py test apps.users.tests.test_email_verify.EmailVerificationViewTests --settings=_dev.settings_test
    """

    def setUp(self):
        self.user = User.objects.create_user(
            email="user_unverified@example.com",
            password="testpassword",
            is_active=True,
            is_verified=True,
        )

    def test_missing_token(self):
        response = self.client.post(reverse_lazy("users_api:email_verify"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Missing token")

    def test_invalid_token(self):
        response = self.client.post(reverse_lazy("users_api:email_verify") + "?token=invalid_token")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Invalid token")

    def test_succesful_verification(self):
        data = {
            "email": "user_unverified@example.com",
            "password": "testpassword",
        }
        login = self.client.post(reverse_lazy("users_api:token_obtain_pair"), data)
        access_token = login.data["access"]
        response = self.client.post(
            reverse_lazy("users_api:email_verify") + f"?token={access_token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Email verified")
