from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from utils.tests import CustomViewTestCase

User = get_user_model()


class RegistrationViewSetTests(CustomViewTestCase):
    """
    ./manage.py test apps.users.tests.test_test_login_view.LoginTokenViewTests --settings=_dev.settings_test
    """

    def setUp(self):
        self.url = reverse_lazy("users_api:registration")

    def test_successful_registration(self):
        data = {
            "email": "new_user@example.com",
            "password": "New_Pa$$w0rd",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        users = User.objects.filter(email=data["email"]).all()
        self.assertEqual(len(users), 1)

        user = users[0]
        user.is_active = True
        user.is_verified = True
        user.save(update_fields=("is_active", "is_verified"))

        response = self.client.post(reverse_lazy("users_api:token_obtain_pair"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_missing_password(self):
        data = {
            "email": "newuser@example.com",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_email(self):
        data = {
            "password": "newpassword",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_existing_user(self):
        User.objects.create_user(email="existinguser@example.com", password="password")
        data = {
            "email": "existinguser@example.com",
            "password": "newpassword",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email(self):
        data = {
            "email": "invalid-email",
            "password": "newpassword",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_password(self):
        data = {
            "email": "newuser@example.com",
            "password": "short",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
