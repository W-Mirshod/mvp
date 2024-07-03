from factory import PostGenerationMethodCall
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from apps.users.models import User


class UserFactory(DjangoModelFactory):
    """
    User Factory
    """

    email = FuzzyText(length=15, suffix="_a@example.com")
    password = PostGenerationMethodCall("set_password", "adm1n")

    class Meta:
        model = User
