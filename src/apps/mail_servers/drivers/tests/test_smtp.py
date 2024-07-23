import unittest
from unittest.mock import patch, MagicMock

from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework_simplejwt.tokens import RefreshToken

from apps.mail_servers.choices import ServerType
from apps.mail_servers.models.servers import SMTPServer
from apps.mail_servers.tests.factories import SMTPServerFactory
from apps.users.tests.factories import UserFactory
from utils.tests import CustomViewTestCase

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from apps.mail_servers.drivers.driver_smtp import SMTPDriver
from constance import config


class SMTPDriverTests(unittest.TestCase):

    def setUp(self):
        self.driver = SMTPDriver(server_name='http://smtp.example.com')
        self.driver.server_name = 'http://smtp.example.com'
        config.ENABLE_SMTP_SENDING = True

    def tearDown(self):
        config.ENABLE_SMTP_SENDING = False

    @patch('apps.mail_servers.models.SMTPServer.objects.get')
    def test_get_server_settings(self, mock_get):
        mock_get.return_value = SMTPServerFactory.build()
        settings = self.driver.get_server_settings()
        self.assertIsNotNone(settings)
        self.assertEqual(settings.url, mock_get.return_value.url)

    @patch('apps.mail_servers.models.SMTPServer.objects.get')
    def test_get_server_settings_raises_exception(self, mock_get):
        mock_get.side_effect = SMTPServer.DoesNotExist
        with self.assertRaises(ObjectDoesNotExist):
            self.driver.get_server_settings()

    @patch('apps.mail_servers.drivers.driver_smtp.get_connection', autospec=True)
    @patch('apps.mail_servers.models.SMTPServer.objects.get')
    def test_send_mail(self, mock_get, mock_get_connection):
        mock_get.return_value = SMTPServerFactory.build()
        self.driver.settings = mock_get.return_value
        mock_connection = MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_connection

        with patch.object(EmailMessage, 'send') as mock_send:
            self.driver.send_mail('Test Subject', 'Test Message', ['recipient@test.com'])
            mock_send.assert_called_once()

    @patch('apps.mail_servers.models.SMTPServer.objects.get')
    def test_check_connection_success(self, mock_get):
        mock_get.return_value = SMTPServerFactory.build()
        self.driver.settings = mock_get.return_value
        with patch('smtplib.SMTP_SSL') as mock_smtp:
            mock_client = MagicMock()
            mock_client.login.return_value = ('OK', [])
            mock_smtp.return_value = mock_client
            self.assertTrue(self.driver.check_connection())

    @patch('apps.mail_servers.models.SMTPServer.objects.get')
    def test_check_connection_failure(self, mock_get):
        mock_get.return_value = SMTPServerFactory.build()
        self.driver.settings = mock_get.return_value
        with patch('smtplib.SMTP_SSL') as mock_smtp:
            mock_client = MagicMock()
            mock_client.login.side_effect = smtplib.SMTPAuthenticationError(535, 'authentication failed')
            mock_smtp.return_value = mock_client
            self.assertFalse(self.driver.check_connection())

    @patch('apps.mail_servers.models.SMTPServer.objects.get')
    def test_login(self, mock_get):
        mock_get.return_value = SMTPServerFactory.build()
        self.driver.settings = mock_get.return_value
        with patch('smtplib.SMTP_SSL') as mock_smtp:
            mock_client = MagicMock()
            mock_client.login.return_value = ('OK', [])
            mock_smtp.return_value = mock_client
            self.assertTrue(self.driver.login())

    @patch('apps.mail_servers.models.SMTPServer.objects.get')
    def test_logout(self, mock_get):
        mock_get.return_value = SMTPServerFactory.build()
        self.driver.settings = mock_get.return_value
        with patch('smtplib.SMTP_SSL') as mock_smtp:
            mock_client = MagicMock()
            mock_client.quit.return_value = ('BYE', [])
            mock_smtp.return_value = mock_client
            self.assertTrue(self.driver.logout())

    @patch('apps.mail_servers.models.SMTPServer.objects.get')
    @patch.object(SMTPDriver, 'send_mail')
    def test_send_message(self, mock_send_mail, mock_get):
        mock_get.return_value = SMTPServerFactory.build()
        self.driver.settings = mock_get.return_value
        self.driver.send_message('Test Subject', 'Test Message', 'recipient@test.com')
        mock_send_mail.assert_called_once_with(
            'Test Subject', 'Test Message', ['recipient@test.com']
        )


class SMTPServerViewTests(CustomViewTestCase):
    """
    ./manage.py test apps.mail_servers.tests.test_smtp.SMTPServerViewTests --settings=_dev.settings_test      # noqa: E501
    """

    def setUp(self):
        self.user = UserFactory(
            email="testuser@example.com", password="Qwerty123", is_verified=True, is_active=True
        )
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(access))

        SMTPServerFactory(
            id=1,
            type=ServerType.SMTP,
            url="http://smtp.example.com",
            port=465,
            password="password",
            username="smtp@example.com",
        )

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/api/1.0/servers/smtp-servers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse_lazy("servers_api:smtp-server_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_server(self):
        smtp_server = SMTPServerFactory(
            id=2,
            type=ServerType.SMTP,
            url="http://smtp.creation.com",
            port=465,
            password="password",
            username="smtp_creation@example.com",
        )

        self.assertEqual(smtp_server, SMTPServer.objects.get(id=2))

    def test_server_list(self):
        response = self.client.get(reverse_lazy("servers_api:smtp-server_list")).json()

        self.assertTrue(len(response) > 0)
        self.assertEqual(response[0]["type"], ServerType.SMTP)

    def test_server_by_id(self):
        response = self.client.get(
            reverse_lazy("servers_api:smtp-server_by_id", kwargs={"pk": 1}))

        self.assertEqual(response.data["type"], ServerType.SMTP)

    def test_wrong_id(self):
        response = self.client.get(
            reverse_lazy("servers_api:smtp-server_by_id", kwargs={"pk": 10}))

        self.assertEqual(response.data["detail"], "No SMTPServer matches the given query.")
