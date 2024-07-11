from rest_framework import status
from rest_framework.reverse import reverse_lazy

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

    def test_logout_unauthenticated(self):
        self.user.is_active = False
        self.client.post(reverse_lazy("users_api:logout"))
        response = self.client.post(reverse_lazy("users_api:logout"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
