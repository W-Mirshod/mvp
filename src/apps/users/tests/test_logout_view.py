from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from apps.users.forms import User
from apps.users.tests.factories import UserFactory
from utils.tests import CustomViewTestCase


class LogoutViewTests(CustomViewTestCase):

    def setUp(self):
        self.user = UserFactory(
            email="user_verified@example.com",
            password="testpassword",
            is_active=True,
            is_verified=True,
        )

    def test_successful_logout(self):
        data = {
            "email": "user_verified@example.com",
            "password": "testpassword",
        }
        response = self.client.post(reverse_lazy("users_api:token_obtain_pair"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            "refresh": response.data["refresh"],
        }
        headers = {
            "Authorization": f'Bearer {response.data["access"]}',
        }
        response_logout = self.client.post(reverse_lazy("users_api:logout"), data, headers=headers)
        self.assertEqual(response_logout.status_code, status.HTTP_200_OK)

    def test_successful_logout_token_in_blacklist(self):
        data = {"email": "testuser@example.com", "password": "testpassword"}
        user = User.objects.get(email=data["email"])
        self.auth_user(User, user, data["password"])
        num_blacklisted_tokens_before = OutstandingToken.objects.count()
        self.client.post(reverse_lazy("users_api:logout"), data)
        num_blacklisted_tokens_after = OutstandingToken.objects.count()
        self.assertEqual(
            num_blacklisted_tokens_after, num_blacklisted_tokens_before + 1
        )

    def test_logout_unauthenticated(self):
        self.user.is_active = False
        self.client.post(reverse_lazy("users_api:logout"))
        response = self.client.post(reverse_lazy("users_api:logout"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
