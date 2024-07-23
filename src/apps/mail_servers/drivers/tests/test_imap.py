import unittest
import imaplib
from unittest.mock import patch, MagicMock

from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework_simplejwt.tokens import RefreshToken

from apps.mail_servers.choices import ServerType
from apps.mail_servers.models.servers import IMAPServer
from apps.mail_servers.tests.factories import IMAPServerFactory
from apps.users.tests.factories import UserFactory
from utils.tests import CustomViewTestCase

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from apps.mail_servers.drivers.driver_imap import IMAPDriver
from constance import config


class IMAPDriverTests(unittest.TestCase):

    def setUp(self):
        self.driver = IMAPDriver(server_name='http://imap.example.com')
        self.driver.server_name = 'http://imap.example.com'
        config.ENABLE_IMAP_SENDING = True

    def tearDown(self):
        config.ENABLE_IMAP_SENDING = False

    @patch('apps.mail_servers.models.IMAPServer.objects.get')
    def test_get_server_settings(self, mock_get):
        mock_get.return_value = IMAPServerFactory.build()
        settings = self.driver.get_server_settings()
        self.assertIsNotNone(settings)
        self.assertEqual(settings.url, mock_get.return_value.url)

    @patch('apps.mail_servers.models.IMAPServer.objects.get')
    def test_get_server_settings_raises_exception(self, mock_get):
        mock_get.side_effect = IMAPServer.DoesNotExist
        with self.assertRaises(ObjectDoesNotExist):
            self.driver.get_server_settings()

    @patch('apps.mail_servers.drivers.driver_imap.get_connection', autospec=True)
    @patch('apps.mail_servers.models.IMAPServer.objects.get')
    def test_send_mail(self, mock_get, mock_get_connection):
        mock_get.return_value = IMAPServerFactory.build()
        self.driver.settings = mock_get.return_value
        mock_connection = MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_connection

        with patch.object(EmailMessage, 'send') as mock_send:
            self.driver.send_mail('Test Subject', 'Test Message', ['recipient@test.com'])
            mock_send.assert_called_once()

    @patch('apps.mail_servers.models.IMAPServer.objects.get')
    def test_check_connection_success(self, mock_get):
        mock_get.return_value = IMAPServerFactory.build()
        self.driver.settings = mock_get.return_value
        with patch('imaplib.IMAP4_SSL') as mock_imap:
            mock_client = MagicMock()
            mock_client.login.return_value = ('OK', [])
            mock_imap.return_value = mock_client
            self.assertTrue(self.driver.check_connection())

    @patch('apps.mail_servers.models.IMAPServer.objects.get')
    def test_check_connection_failure(self, mock_get):
        mock_get.return_value = IMAPServerFactory.build()
        self.driver.settings = mock_get.return_value
        with patch('imaplib.IMAP4_SSL') as mock_imap:
            mock_client = MagicMock()
            mock_client.login.side_effect = imaplib.IMAP4.error('login failed')
            mock_imap.return_value = mock_client
            self.assertFalse(self.driver.check_connection())

    @patch('apps.mail_servers.models.IMAPServer.objects.get')
    def test_login(self, mock_get):
        mock_get.return_value = IMAPServerFactory.build()
        self.driver.settings = mock_get.return_value
        with patch('imaplib.IMAP4_SSL') as mock_imap:
            mock_client = MagicMock()
            mock_client.login.return_value = ('OK', [])
            mock_imap.return_value = mock_client
            self.assertTrue(self.driver.login())

    @patch('apps.mail_servers.models.IMAPServer.objects.get')
    def test_logout(self, mock_get):
        mock_get.return_value = IMAPServerFactory.build()
        self.driver.settings = mock_get.return_value
        with patch('imaplib.IMAP4_SSL') as mock_imap:
            mock_client = MagicMock()
            mock_client.logout.return_value = ('BYE', [])
            mock_imap.return_value = mock_client
            self.assertTrue(self.driver.logout())

    @patch('apps.mail_servers.models.IMAPServer.objects.get')
    @patch.object(IMAPDriver, 'send_mail')
    def test_send_message(self, mock_send_mail, mock_get):
        mock_get.return_value = IMAPServerFactory.build()
        self.driver.settings = mock_get.return_value
        self.driver.send_message('Test Subject', 'Test Message', 'recipient@test.com')
        mock_send_mail.assert_called_once_with(
            'Test Subject', 'Test Message', ['recipient@test.com']
        )


class IMAPServerViewTests(CustomViewTestCase):
    """
    ./manage.py test apps.mail_servers.tests.test_imap.IMAPServerViewTests --settings=_dev.settings_test      # noqa: E501
    """

    def setUp(self):
        self.user = UserFactory(
            email="testuser@example.com", password="Qwerty123", is_verified=True, is_active=True
        )
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(access))

        IMAPServerFactory(
            id=1,
            type=ServerType.IMAP,
            url="http://imap.example.com",
            port=465,
            password="password",
            username="imap@example.com",
        )

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/api/1.0/servers/imap-servers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse_lazy("servers_api:imap-server_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_server(self):
        imap_server = IMAPServerFactory(
            id=2,
            type=ServerType.IMAP,
            url="http://imap.creation.com",
            port=465,
            password="password",
            username="imap_creation@example.com",
        )

        self.assertEqual(imap_server, IMAPServer.objects.get(id=2))

    def test_server_list(self):
        response = self.client.get(reverse_lazy("servers_api:imap-server_list")).json()

        self.assertTrue(len(response) > 0)
        self.assertEqual(response[0]["type"], ServerType.IMAP)

    def test_server_by_id(self):
        response = self.client.get(
            reverse_lazy("servers_api:imap-server_by_id", kwargs={"pk": 1}))

        self.assertEqual(response.data["type"], ServerType.IMAP)

    def test_wrong_id(self):
        response = self.client.get(
            reverse_lazy("servers_api:imap-server_by_id", kwargs={"pk": 10}))

        self.assertEqual(response.data["detail"], "No IMAPServer matches the given query.")
