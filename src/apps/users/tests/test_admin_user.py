from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse, reverse_lazy

from apps.users.tests.factories import UserFactory
from utils.tests import CustomViewTestCase

User = get_user_model()


class TestUserAdmin(CustomViewTestCase):
    """
    ./manage.py test apps.users.tests.test_admin_user.TestUserAdmin --settings=_dev.settings_test
    """

    model = User

    @classmethod
    def setUpTestData(cls):
        cls.user_admin = UserFactory(
            email="adm1n@admin.com",
            is_superuser=True,
            is_staff=True,
            is_active=True,
            is_verified=True,
        )
        cls.password = "adm1n"
        cls.user_admin.set_password(cls.password)

        cls.users = User.objects.bulk_create(
            [
                User(email="user_01@example.com"),
                User(email="user_02@example.com"),
                User(email="user_03@example.com"),
            ]
        )

    def test_list(self):
        self.auth_user(self.user_admin)
        url = reverse_lazy(
            f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist"
        )
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change(self):
        url = reverse_lazy(
            f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
            args=(self.users[0].id,),
        )
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_post(self):
        data = {
            "is_verified": True,
            "is_active": True,
        }
        url = reverse_lazy(
            f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
            args=(self.users[0].id,),
        )
        response = self.client.post(
            url,
            data=data,
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
