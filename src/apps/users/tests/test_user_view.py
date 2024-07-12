from apps.users.tests.factories import UserFactory, UserTariffFactory
from utils.tests import CustomViewTestCase


class UserViewTest(CustomViewTestCase):
    """
    ./manage.py test apps.users.tests.test_user_view.UserViewTest --settings=_dev.settings_test
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

    def test_list_01_url_exists_at_desired_location(self):
        response = self.client.get(f"/api/1.0/users/{self.user_admin.id}/")
        self.assertEqual(response.status_code, 200)

    def test_detail_01(self):
        self.auth_user(user=self.user_admin)
        self._test_detail("users_api:manage", self.user_admin)
