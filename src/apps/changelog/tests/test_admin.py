from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from apps.changelog.admin import ChangeLogAdmin
from apps.changelog.models import ChangeLog
from apps.changelog.tests.factories import ChangeLogFactory
from apps.users.tests.factories import UserFactory
from utils.tests import CustomViewTestCase


class ChangeLogAdminTest(CustomViewTestCase):

    def setUp(self):
        self.site = AdminSite()
        self.admin = ChangeLogAdmin(ChangeLog, self.site)
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.changelog = ChangeLogFactory(user=self.user)

    def test_has_add_permission(self):
        request = self.factory.get("/admin/changelog/changelog/")
        self.assertFalse(self.admin.has_add_permission(request))

    def test_has_change_permission(self):
        request = self.factory.get("/admin/changelog/changelog/")
        self.assertFalse(self.admin.has_change_permission(request, obj=self.changelog))

    def test_has_delete_permission(self):
        request = self.factory.get("/admin/changelog/changelog/")
        self.assertTrue(self.admin.has_delete_permission(request, obj=self.changelog))

    def test_list_display(self):
        self.assertEqual(
            self.admin.list_display,
            ("changed", "model", "user", "record_id", "data", "ipaddress", "action_on_model"),
        )

    def test_readonly_fields(self):
        self.assertEqual(
            self.admin.readonly_fields,
            ("user",),
        )

    def test_list_filter(self):
        self.assertEqual(self.admin.list_filter, ("model", "action_on_model"))
