from django.test import RequestFactory, TestCase
from rest_framework.exceptions import PermissionDenied
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models.users import User
from utils.permissions import IsOneTimeTokenValid, IsOwner, IsTokenValid


class TestIsOneTimeTokenValid(TestCase):
    """
    python manage.py test tests.test_permissions --config=_dev.settings_test

    """

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass"
        )
        self.factory = APIRequestFactory()
        self.token = RefreshToken.for_user(self.user)
        self.token["one_time"] = True

    def test_valid_one_time_token(self):
        request = self.factory.get("/api/some_endpoint/")
        request.META["HTTP_AUTHORIZATION"] = f"Bearer {self.token}"
        permission = IsOneTimeTokenValid()
        self.assertTrue(permission.has_permission(request, None))

    def test_invalid_one_time_token(self):
        request = self.factory.get("/api/some_endpoint/")
        request.META["HTTP_AUTHORIZATION"] = "Bearer invalid_token"
        permission = IsOneTimeTokenValid()
        with self.assertRaises(PermissionDenied):
            permission.has_permission(request, None)


class TestIsTokenValid(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass"
        )
        self.token = RefreshToken.for_user(self.user)
        self.factory = RequestFactory()

    def test_valid_token(self):
        request = self.factory.get("/api/some_endpoint/")
        request.META["HTTP_AUTHORIZATION"] = f"Bearer {self.token}"
        permission = IsTokenValid()
        self.assertTrue(permission.has_permission(request, None))

    def test_invalid_token(self):
        request = self.factory.get("/api/some_endpoint/")
        request.META["HTTP_AUTHORIZATION"] = "Bearer invalid_token"
        permission = IsTokenValid()
        self.assertFalse(permission.has_permission(request, None))


class TestIsOwner(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com", password="otherpass"
        )
        self.factory = APIRequestFactory()

    def test_is_owner(self):
        obj = self.user
        request = self.factory.get("/api/some_endpoint/")
        request.user = self.user
        permission = IsOwner()
        self.assertTrue(permission.has_object_permission(request, None, obj))

    def test_is_not_owner(self):
        obj = self.other_user
        request = self.factory.get("/api/some_endpoint/")
        request.user = self.user
        permission = IsOwner()
        self.assertFalse(permission.has_object_permission(request, None, obj))
