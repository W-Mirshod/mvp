from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from apps.changelog.admin import ChangeLogAdmin
from apps.changelog.models import ChangeLog
from apps.users.models import User


class ChangeLogAdminTest(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.admin = ChangeLogAdmin(ChangeLog, self.site)
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email="testuser@example.com", password="admin123")
        self.changelog = ChangeLog.objects.create(
            datetime="2023-07-05T18:00:00Z",
            model_name="TestModel",
            user=self.user,
            object_id=1,
            data="{}",
            url="http://example.com",
            action="create",
        )

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
            ("datetime", "model_name", "user", "object_id", "data", "url", "action"),
        )

    def test_readonly_fields(self):
        self.assertEqual(
            self.admin.readonly_fields,
            ("datetime", "model_name", "user", "object_id", "data", "url", "action"),
        )

    def test_list_filter(self):
        self.assertEqual(self.admin.list_filter, ("model_name", "action"))

    def test_search_fields(self):
        self.assertEqual(
            self.admin.search_fields,
            ("model_name", "user__email", "object_id", "action"),
        )
