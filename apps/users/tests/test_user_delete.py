from apps.users.tests.factories import UserFactory, UserTariffFactory
from utils.tests import CustomViewTestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


class UserDeleteTest(CustomViewTestCase):
    """
    ./manage.py test apps.users.tests.test_user_delete.UserViewTest --config=_dev.settings_test
    """

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
        cls.user_tariff = UserTariffFactory(
            user=cls.user_admin,
        )
        cls.password = "adm1n"
        cls.user_admin.set_password(cls.password)

    def test_check_status_code_delete_user(self):

        response = self.client.delete(f"/api/1.0/users/{self.user_admin.id}/")
        self.assertEqual(response.status_code, 204)

    def test_user_delete_existing(self):
        user_model = get_user_model()
        self.assertTrue(user_model.objects.filter(id=self.user_admin.id).exists())

        self.client.delete(f"/api/1.0/users/{self.user_admin.id}/")
        with self.assertRaises(ObjectDoesNotExist):
            user_model.objects.get(id=self.user_admin.id)
