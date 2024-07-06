from rest_framework import status
from rest_framework.reverse import reverse_lazy

from apps.users.forms import User
from utils.tests import CustomViewTestCase


class LogoutViewTests(CustomViewTestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            is_active=True,
            is_verified=True,
        )

    def test_successful_logout(self):
        data = {"email": "testuser@example.com", "password": "testpassword"}
        user = User.objects.get(email=data["email"])
        self.auth_user(User, user, data["password"])
        response_logout = self.client.post(reverse_lazy("users_api:logout"), data)
        self.assertEqual(response_logout.status_code, status.HTTP_200_OK)

    def test_logout_unauthenticated(self):
        self.user.is_active = False
        self.client.post(reverse_lazy("users_api:logout"))
        response = self.client.post(reverse_lazy("users_api:logout"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
