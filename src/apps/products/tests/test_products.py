from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework_simplejwt.tokens import RefreshToken

from src.apps.products.tests.factories import ProductFactory
from src.apps.users.tests.factories import UserFactory
from src.utils.tests import CustomViewTestCase


class ProductViewTests(CustomViewTestCase):
    """
    ./manage.py test apps.products.tests.test_products.ProductViewTests --settings=_dev.settings_test      # noqa: E501
    """

    def setUp(self):
        self.user = UserFactory(is_verified=True, is_active=True)
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(access))

        ProductFactory(
            id=1,
            title="Product 1",
            description="Product 1 desc",
        )

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/api/1.0/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse_lazy("products_api:product_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_list(self):
        response = self.client.get(reverse_lazy("products_api:product_list")).json()
        self.assertEqual(response[0]["title"], "Product 1")

    def test_product_by_id(self):
        response = self.client.get(
            reverse_lazy("products_api:product_by_id", kwargs={"pk": 1})
        )
        self.assertEqual(response.data["title"], "Product 1")

    def test_wrong_id(self):
        response = self.client.get(
            reverse_lazy("products_api:product_by_id", kwargs={"pk": 3})
        )
        self.assertEqual(response.data["detail"], "No Product matches the given query.")
