from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework_simplejwt.tokens import RefreshToken

from apps.mail_servers.choices import ServerType
from apps.mail_servers.models import ProxyServer
from apps.mail_servers.tests.factories import ProxyServerFactory
from apps.users.tests.factories import UserFactory
from utils.tests import CustomViewTestCase


class ProxyServerViewTests(CustomViewTestCase):
    """
    ./manage.py test apps.mail_servers.tests.test_proxy.ProxyServerViewTests --settings=_dev.settings_test      # noqa: E501
    """

    def setUp(self):
        self.user = UserFactory(
            email="testuser@example.com", password="Qwerty123", is_verified=True, is_active=True
        )
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(access))

        ProxyServerFactory(
            id=1,
            type=ServerType.PROXY,
            url="http://proxy.example.com",
            port=465,
            password="password",
            username="proxy@example.com",
        )

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/api/1.0/servers/proxy-servers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse_lazy("servers_api:proxy-server_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_server(self):
        proxy_server = ProxyServerFactory(
            id=2,
            type=ServerType.PROXY,
            url="http://proxy.creation.com",
            port=465,
            password="password",
            username="proxy_creation@example.com",
        )

        self.assertEqual(proxy_server, ProxyServer.objects.get(id=2))

    def test_server_list(self):
        response = self.client.get(reverse_lazy("servers_api:proxy-server_list")).json()

        self.assertTrue(len(response) > 0)
        self.assertEqual(response[0]["type"], ServerType.PROXY)

    def test_server_by_id(self):
        response = self.client.get(reverse_lazy("servers_api:proxy-server_by_id", kwargs={"pk": 1}))

        self.assertEqual(response.data["type"], ServerType.PROXY)

    def test_wrong_id(self):
        response = self.client.get(
            reverse_lazy("servers_api:proxy-server_by_id", kwargs={"pk": 10})
        )

        self.assertEqual(response.data["detail"], "No ProxyServer matches the given query.")
