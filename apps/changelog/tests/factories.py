from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

from apps.changelog.models.models import ChangeLog
from apps.users.tests.factories import UserFactory


class ChangeLogFactory(DjangoModelFactory):
    class Meta:
        model = ChangeLog

    user = SubFactory(UserFactory)
    model = "TestModel"
    record_id = Sequence(lambda n: n)
    action_on_model = "create"
    data = {}
    ipaddress = "127.0.0.1"
