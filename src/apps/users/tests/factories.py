from factory import PostGenerationMethodCall, SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker
from factory.fuzzy import FuzzyText

from src.apps.products.tests.factories import TariffFactory
from src.apps.users.models import UserTariff
from src.apps.users.models.users import User


class UserFactory(DjangoModelFactory):
    """
    User Factory
    """

    email = FuzzyText(length=15, suffix="_a@example.com")
    password = PostGenerationMethodCall("set_password", "adm1n")

    class Meta:
        model = User


class UserTariffFactory(DjangoModelFactory):
    """
    User Tariff Factory
    """

    user = SubFactory(UserFactory)
    tariff = SubFactory(TariffFactory)
    expired_at = Faker("date_time_between", start_date="now", end_date="+30d")

    class Meta:
        model = UserTariff
