from django.test import TestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIRequestFactory



from apps.users.models.users import User
from apps.users.views.v1.views_users import RefreshTokenView


class UserCreationTestCase(TestCase):
    """
    ./manage.py test apps.users.tests.test_models.UserCreationTestCase --settings=_dev.settings_test
    """

    def test_create_user(self):
        email = "user@user.com"
        User.objects.create_user(email=email, password="P@$$w0rd", is_verified=True, is_active=True)
        user = list(User.objects.filter(email=email).all())
        self.assertEqual(len(user), 1)
        self.assertEqual(user[0].email, email)
        self.assertTrue(user[0].is_verified)
        self.assertTrue(user[0].is_active)
        self.assertFalse(user[0].is_superuser)

    def test_create_superuser(self):
        email = "superuser@user.com"
        User.objects.create_superuser(
            email=email, password="P@$$w0rd", is_verified=True, is_active=True
        )
        user = list(User.objects.filter(email=email).all())
        self.assertEqual(len(user), 1)
        self.assertEqual(user[0].email, email)
        self.assertTrue(user[0].is_verified)
        self.assertTrue(user[0].is_active)
        self.assertTrue(user[0].is_superuser)

class RefreshTokenViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpass")
        self.client = APIRequestFactory()
        self.view = RefreshTokenView.as_view({'post': 'refresh'})


    def test_refresh_token_valid(self):
        # create a new token for the user
        refresh = RefreshToken.for_user(self.user)
        data = {"refresh": str(refresh)}

        # make a request to refresh the token
        request = self.client.post("/api/1.0/token_refresh/", data=data)
        response = self.view(request)

        # check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check the response data
        response_data = response.data
        self.assertEqual(response_data["user_id"], self.user.id)
        self.assertIn("refresh", response_data)
        self.assertIn("access", response_data)

    def test_refresh_token_invalid(self):
        # create an invalid token
        data = {"refresh": "invalid_token"}

        # make a request to refresh the token
        request = self.client.post("/api/1.0/token_refresh/", data=data)
        response = self.view(request)

        # check the response status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # check the response data
        response_data = response.data
        self.assertIn("detail", response_data)
        self.assertEqual(response_data["detail"], "Token is invalid or expired")

