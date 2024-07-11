from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework_simplejwt.tokens import RefreshToken

from apps.products.models import Tariff
from apps.products.tests.factories import TariffFactory
from apps.users.tests.factories import UserFactory
from utils.tests import CustomViewTestCase


class TariffViewTests(CustomViewTestCase):
    """
    ./manage.py test apps.products.tests.test_tariffs.TariffViewTests --settings=_dev.settings_test      # noqa: E501
    """

    def setUp(self):
        self.user = UserFactory(is_verified=True, is_active=True)
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(access))

        TariffFactory(
            id=1,
            title="Tariff 1",
            rate=199,
        )

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/api/1.0/tariffs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse_lazy("tariffs_api:tariff_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_tariff(self):
        tariff = TariffFactory(id=2, title="Tariff 2", rate=999.99)
        self.assertEqual(tariff, Tariff.objects.get(id=2))

    def test_tariff_list(self):
        response = self.client.get(reverse_lazy("tariffs_api:tariff_list")).json()
        self.assertTrue(len(response) > 0)
        self.assertEqual(response[0]["title"], "Tariff 1")

    def test_product_by_id(self):
        response = self.client.get(reverse_lazy("tariffs_api:tariff_by_id", kwargs={"pk": 1}))
        self.assertEqual(response.data["title"], "Tariff 1")

    def test_wrong_id(self):
        response = self.client.get(reverse_lazy("tariffs_api:tariff_by_id", kwargs={"pk": 3}))
        self.assertEqual(response.data["detail"], "No Tariff matches the given query.")
