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


class UserViewTest(TestCase):
    """
    ./manage.py test apps.users.tests.test_view.UserViewTest --settings=_dev.settings_test
    """

    CONTENT_TYPE_JSON = "application/json"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_admin = UserFactory(
            email="adm1n@admin.com",
            is_superuser=True,
            is_staff=True,
            is_active=True,
            is_verified=True,
        )
        cls.password = "adm1n"
        cls.user_admin.set_password(cls.password)

    def test_login(self):
        self.assertFalse(get_user(self.client).is_authenticated)
        self.client.login(email="adm1n@admin.com", password=self.password)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_login_wrong(self):
        self.assertFalse(get_user(self.client).is_authenticated)
        self.client.login(email="adm1n@admin.com", password="wrong")
        self.assertFalse(get_user(self.client).is_authenticated)


class LoginTokenViewTests(CustomViewTestCase):
    """
    ./manage.py test apps.users.tests.test_view.LoginTokenViewTests --settings=_dev.settings_test
    """

    def setUp(self):
        self.user = User.objects.create_user(
            email="user_verified@example.com",
            password="testpassword",
            is_active=True,
            is_verified=True,
        )

    def test_successful_login(self):
        data = {"email": "user_verified@example.com", "password": "testpassword"}
        response = self.client.post(reverse_lazy("users_api:token_obtain_pair"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)
        self.assertIn("user_id", response.data)

    def test_invalid_credentials(self):
        data = {"email": "user_verified@example.com", "password": "wrongpassword"}
        response = self.client.post(reverse_lazy("users_api:token_obtain_pair"), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_password(self):
        data = {
            "email": "testuser@example.com",
        }
        response = self.client.post(reverse_lazy("users_api:token_obtain_pair"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_email(self):
        data = {
            "password": "testpassword",
        }
        response = self.client.post(reverse_lazy("users_api:token_obtain_pair"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        data = {"email": "testuser@example.com", "password": "testpassword"}
        response = self.client.post(reverse_lazy("users_api:token_obtain_pair"), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
