import json

from django.db.models import Model
from django.test import override_settings
from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from apps.users.models.users import User


@override_settings(SQL_DEBUG=False)
class TestCaseBase(APITestCase):
    """
    Base (without authorisation)
    """

    CONTENT_TYPE_JSON = "application/json"

    def check_status(self, response, status):
        self.assertEqual(response.status_code, status, response.data)


class WithLoginTestCase(TestCaseBase):
    """
    Base (with authorisation)
    """

    admin_email = "admin@admin.com"
    admin_password = "admin"
    admin_token = ""
    admin_refresh = ""

    jwt_body = {}

    login_url = reverse_lazy("users_api:token_obtain_pair")
    refresh_token_url = reverse_lazy("users_api:token_refresh")
    logout_url = reverse_lazy("users_api:logout")

    def _login(self, user: User = None, email: str = None, password: str = None):
        user = user if user else self.user
        data = {
            "email": email if email else self.admin_email,
            "password": password if password else self.admin_password,
        }
        r = self.client.post(self.login_url, data)
        self.jwt_body = r.json()
        if "access" in self.jwt_body:
            self.client.credentials(
                HTTP_AUTHORIZATION=f"Bearer {self.jwt_body['access']}"
            )
        return r.status_code, self.jwt_body

    @classmethod
    def setUpClass(cls):
        user, is_create = User.objects.get_or_create(email=cls.admin_email)
        if is_create:
            user.set_password(cls.admin_password)
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.is_verified = True
            user.save()
        cls.user = user
        super().setUpClass()

    def setUp(self) -> None:
        self.auth_user(self.user)
        super().setUp()

    def auth_user(self, user: User, email: str = None, password: str = None):
        """
        Авторизация
        """
        _, body = self._login(user, email, password)
        self.admin_token = body["access"]
        self.admin_refresh = body["refresh"]


class CustomViewTestCase(WithLoginTestCase):

    def _test_list(self, url, object):
        if ":" in url:
            url = reverse_lazy(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        rows = response.data["results"]
        self.assertEqual(
            [row["id"] for row in rows if row["id"] == object.pk], [object.pk]
        )

    def _test_create(self, url_name, model, check_field, status_code=201):
        url = reverse_lazy(url_name)
        data = self._generate_data()
        response = self.client.post(
            url,
            data=json.dumps(data, indent=4, sort_keys=True, default=str),
            content_type=self.CONTENT_TYPE_JSON,
        )
        self.assertEqual(response.status_code, status_code, response.data)
        object = model.objects.filter(pk=response.data["id"]).first()
        self.assertEqual(getattr(object, check_field), data[check_field])
        return object

    def _test_detail(self, url_name: str, object: "Model", check_field: str = "id"):
        url = reverse_lazy(url_name, kwargs=dict(pk=object.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(getattr(object, check_field), response.data[check_field])

    def _test_edit(
        self, url_name: str, object: "Model", check_field: str = None, data=None
    ):
        url = reverse_lazy(url_name, kwargs=dict(pk=object.pk))
        if data is None:
            data = self._generate_data()
        response = self.client.put(
            url, data=json.dumps(data), content_type=self.CONTENT_TYPE_JSON
        )
        self.assertEqual(response.status_code, 200, response.data)
        object = type(object).objects.filter(pk=response.data["id"]).first()
        if check_field:
            self.assertEqual(getattr(object, check_field), data[check_field])
        return object

    def _test_delete(self, url_name, object):
        url = reverse_lazy(url_name, kwargs=dict(pk=object.pk))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204, response.data)
        qs = type(object).objects.filter(pk=object.pk, is_deleted=False)
        self.assertIsNone(qs.first())

    def _generate_data(self):
        pass
