from rest_framework import status
from rest_framework.reverse import reverse_lazy

from apps.products.models import Product
from utils.tests import CustomViewTestCase


class ProductViewTests(CustomViewTestCase):
    """
    ./manage.py test apps.products.tests.test_products.ProductViewTests --settings=_dev.settings_test      # noqa: E501
    """

    def setUp(self):
        Product.objects.create(
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

    def test_create_product(self):
        Product.objects.create(id=2, title="Product 2", description="Product 2 desc")
        product = list(Product.objects.filter(title="Product 2").all())
        self.assertEqual(product[0].title, "Product 2")
        self.assertEqual(product[0].description, "Product 2 desc")

    def test_product_list(self):
        response = self.client.get(reverse_lazy("products_api:product_list")).json()
        self.assertEqual(response[0]["title"], "Product 1")

    def test_product_by_id(self):
        response = self.client.get(reverse_lazy("products_api:product_by_id", kwargs={"id": 1}))
        self.assertEqual(response.data["title"], "Product 1")

    def test_wrong_id(self):
        response = self.client.get(reverse_lazy("products_api:product_by_id", kwargs={"id": 3}))
        self.assertEqual(response.data["error"], "Product matching query does not exist.")
