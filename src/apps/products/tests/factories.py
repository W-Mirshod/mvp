from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyFloat, FuzzyText

from apps.products.models import Product, Tariff


class ProductFactory(DjangoModelFactory):
    """
    Product Factory
    """

    title = FuzzyText(length=10, prefix="title_")
    description = FuzzyText(length=10, prefix="description_")

    class Meta:
        model = Product


class TariffFactory(DjangoModelFactory):
    """
    Tariff Factory
    """

    title = FuzzyText(length=10, prefix="title_")
    rate = FuzzyFloat(low=0.01, high=999.99)
    product = SubFactory(ProductFactory)

    class Meta:
        model = Tariff
