from decimal import Decimal

from rest_framework import status
from rest_framework.reverse import reverse_lazy

from apps.products.models import Product, Tariff
from utils.tests import CustomViewTestCase


class TariffViewTests(CustomViewTestCase):
    """
    ./manage.py test apps.products.tests.test_tariffs.TariffViewTests --settings=_dev.settings_test      # noqa: E501
    """

    def setUp(self):
        Product.objects.create(
            id=1,
            title="Product 1",
            description="Product 1 desc",
        )

        Tariff.objects.create(
            id=1,
            title="Tariff 1",
            rate=199,
            product=Product.objects.get(id=1),
        )

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/api/1.0/tariffs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse_lazy("tariffs_api:tariff_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_tariff(self):
        Tariff.objects.create(
            id=2, title="Tariff 2", rate=999.99, product=Product.objects.get(id=1)
        )
        tariff = list(Tariff.objects.filter(title="Tariff 2").all())
        self.assertEqual(tariff[0].title, "Tariff 2")
        self.assertAlmostEqual(tariff[0].rate, Decimal(999.99), places=2)
        self.assertEqual(tariff[0].product, Product.objects.get(id=1))

    def test_tariff_list(self):
        response = self.client.get(reverse_lazy("tariffs_api:tariff_list")).json()
        self.assertTrue(len(response) > 0)
        self.assertEqual(response[0]["title"], "Tariff 1")

    def test_product_by_id(self):
        response = self.client.get(reverse_lazy("tariffs_api:tariff_by_id", kwargs={"id": 1}))
        self.assertEqual(response.data["title"], "Tariff 1")

    def test_wrong_id(self):
        response = self.client.get(reverse_lazy("tariffs_api:tariff_by_id", kwargs={"id": 3}))
        self.assertEqual(response.data["error"], "Tariff matching query does not exist.")
