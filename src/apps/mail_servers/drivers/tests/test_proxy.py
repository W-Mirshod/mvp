import unittest
import imaplib
from unittest.mock import patch, MagicMock

from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework_simplejwt.tokens import RefreshToken

from src.apps.mail_servers.choices import ServerType
from src.apps.mail_servers.models import ProxyServer
from src.apps.mail_servers.tests.factories import ProxyServerFactory
from src.apps.users.tests.factories import UserFactory
from src.utils.tests import CustomViewTestCase

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from src.apps.mail_servers.drivers.driver_proxy import ProxyDriver
from constance import config


class ProxyDriverTests(unittest.TestCase):

    def setUp(self):
        self.driver = ProxyDriver(server_name="http://proxy.example.com")
        self.driver.server_name = "http://proxy.example.com"
        config.ENABLE_PROXY_SENDING = True

    def tearDown(self):
        config.ENABLE_PROXY_SENDING = False

    @patch("apps.mail_servers.models.ProxyServer.objects.get")
    def test_get_server_settings(self, mock_get):
        mock_get.return_value = ProxyServerFactory.build()
        settings = self.driver.get_server_settings()
        self.assertIsNotNone(settings)
        self.assertEqual(settings.url, mock_get.return_value.url)

    @patch("apps.mail_servers.models.ProxyServer.objects.get")
    def test_get_server_settings_raises_exception(self, mock_get):
        mock_get.side_effect = ProxyServer.DoesNotExist
        with self.assertRaises(ObjectDoesNotExist):
            self.driver.get_server_settings()

    @patch("apps.mail_servers.drivers.driver_proxy.get_connection", autospec=True)
    @patch("apps.mail_servers.models.ProxyServer.objects.get")
    def test_send_mail(self, mock_get, mock_get_connection):
        mock_get.return_value = ProxyServerFactory.build()
        self.driver.settings = mock_get.return_value
        mock_connection = MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_connection

        with patch.object(EmailMessage, "send") as mock_send:
            self.driver.send_mail(
                "Test Subject", "Test Message", ["recipient@test.com"]
            )
            mock_send.assert_called_once()

    @patch("apps.mail_servers.models.ProxyServer.objects.get")
    def test_check_connection_success(self, mock_get):
        mock_get.return_value = ProxyServerFactory.build()
        self.driver.settings = mock_get.return_value
        with patch("imaplib.IMAP4_SSL") as mock_imap:
            mock_client = MagicMock()
            mock_client.login.return_value = ("OK", [])
            mock_imap.return_value = mock_client
            self.assertTrue(self.driver.check_connection())

    @patch("apps.mail_servers.models.ProxyServer.objects.get")
    def test_check_connection_failure(self, mock_get):
        mock_get.return_value = ProxyServerFactory.build()
        self.driver.settings = mock_get.return_value
        with patch("imaplib.IMAP4_SSL") as mock_imap:
            mock_client = MagicMock()
            mock_client.login.side_effect = imaplib.IMAP4.error("login failed")
            mock_imap.return_value = mock_client
            self.assertFalse(self.driver.check_connection())

    @patch("apps.mail_servers.models.ProxyServer.objects.get")
    def test_login(self, mock_get):
        mock_get.return_value = ProxyServerFactory.build()
        self.driver.settings = mock_get.return_value
        with patch("imaplib.IMAP4_SSL") as mock_imap:
            mock_client = MagicMock()
            mock_client.login.return_value = ("OK", [])
            mock_imap.return_value = mock_client
            self.assertTrue(self.driver.login())

    @patch("apps.mail_servers.models.ProxyServer.objects.get")
    def test_logout(self, mock_get):
        mock_get.return_value = ProxyServerFactory.build()
        self.driver.settings = mock_get.return_value
        with patch("imaplib.IMAP4_SSL") as mock_imap:
            mock_client = MagicMock()
            mock_client.logout.return_value = ("BYE", [])
            mock_imap.return_value = mock_client
            self.assertTrue(self.driver.logout())

    @patch("apps.mail_servers.models.ProxyServer.objects.get")
    @patch.object(ProxyDriver, "send_mail")
    def test_send_message(self, mock_send_mail, mock_get):
        mock_get.return_value = ProxyServerFactory.build()
        self.driver.settings = mock_get.return_value
        self.driver.send_message("Test Subject", "Test Message", "recipient@test.com")
        mock_send_mail.assert_called_once_with(
            "Test Subject", "Test Message", ["recipient@test.com"]
        )


class ProxyServerViewTests(CustomViewTestCase):
    """
    ./manage.py test apps.mail_servers.tests.test_proxy.ProxyServerViewTests --settings=_dev.settings_test      # noqa: E501
    """

    def setUp(self):
        self.user = UserFactory(
            email="testuser@example.com",
            password="Qwerty123",
            is_verified=True,
            is_active=True,
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
        response = self.client.get(
            reverse_lazy("servers_api:proxy-server_by_id", kwargs={"pk": 1})
        )

        self.assertEqual(response.data["type"], ServerType.PROXY)

    def test_wrong_id(self):
        response = self.client.get(
            reverse_lazy("servers_api:proxy-server_by_id", kwargs={"pk": 10})
        )

        self.assertEqual(
            response.data["detail"], "No ProxyServer matches the given query."
        )
