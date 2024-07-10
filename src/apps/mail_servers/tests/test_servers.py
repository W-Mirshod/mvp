from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework_simplejwt.tokens import RefreshToken

from apps.mail_servers.choices import ServerType
from apps.mail_servers.models import (
    IMAPServer,
    MessageTemplate,
    ProxyServer,
    SMTPServer,
)
from apps.users.models import User
from utils.tests import CustomViewTestCase


class ServersViewTests(CustomViewTestCase):
    """
    ./manage.py test apps.mail_servers.tests.test_servers.ServersViewTests --settings=_dev.settings_test      # noqa: E501
    """

    def setUp(self):
        self.user = User.objects.create_superuser(
            email="testuser@example.com", password="Qwerty123", is_verified=True, is_active=True
        )
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(access))

        SMTPServer.objects.create(
            id=1,
            type=ServerType.SMTP,
            url="http://smtp.example.com",
            port=465,
            password="password",
            username="smtp@example.com",
        )

        IMAPServer.objects.create(
            id=2,
            type=ServerType.IMAP,
            url="http://smtp.example.com",
            port=465,
            password="password",
            username="smtp@example.com",
        )

        ProxyServer.objects.create(
            id=3,
            type=ServerType.PROXY,
            url="http://smtp.example.com",
            port=465,
            password="password",
            username="smtp@example.com",
        )

        MessageTemplate.objects.create(
            id=1,
            from_address="template@example.com",
            template="Example template",
            message={"message": "Example message"},
        )

    def test_url_exists_at_desired_location(self):
        smtp_response = self.client.get("/api/1.0/servers/smtp-servers/")
        imap_response = self.client.get("/api/1.0/servers/imap-servers/")
        proxy_response = self.client.get("/api/1.0/servers/proxy-servers/")
        message_response = self.client.get("/api/1.0/servers/message-templates/")

        self.assertEqual(smtp_response.status_code, status.HTTP_200_OK)
        self.assertEqual(imap_response.status_code, status.HTTP_200_OK)
        self.assertEqual(proxy_response.status_code, status.HTTP_200_OK)
        self.assertEqual(message_response.status_code, status.HTTP_200_OK)

    def test_url_accessible_by_name(self):
        smtp_response = self.client.get(reverse_lazy("servers_api:smtp-server_list"))
        imap_response = self.client.get(reverse_lazy("servers_api:imap-server_list"))
        proxy_response = self.client.get(reverse_lazy("servers_api:proxy-server_list"))
        message_response = self.client.get(reverse_lazy("servers_api:message-template_list"))

        self.assertEqual(smtp_response.status_code, status.HTTP_200_OK)
        self.assertEqual(imap_response.status_code, status.HTTP_200_OK)
        self.assertEqual(proxy_response.status_code, status.HTTP_200_OK)
        self.assertEqual(message_response.status_code, status.HTTP_200_OK)

    def test_create_server(self):
        smtp_server = SMTPServer.objects.create(
            id=4,
            type=ServerType.SMTP,
            url="http://smtp.creation.com",
            port=465,
            password="password",
            username="smtp_creation@example.com",
        )

        imap_server = IMAPServer.objects.create(
            id=5,
            type=ServerType.IMAP,
            url="http://imap.creation.com",
            port=465,
            password="password",
            username="imap_creation@example.com",
        )

        proxy_server = ProxyServer.objects.create(
            id=6,
            type=ServerType.PROXY,
            url="http://proxy.creation.com",
            port=465,
            password="password",
            username="proxy_creation@example.com",
        )

        message_template = MessageTemplate.objects.create(
            id=2,
            from_address="template_creation@example.com",
            template="Example template creation",
            message={"message": "Example message"},
        )

        self.assertEqual(smtp_server, SMTPServer.objects.get(url="http://smtp.creation.com"))
        self.assertEqual(imap_server, IMAPServer.objects.get(url="http://imap.creation.com"))
        self.assertEqual(proxy_server, ProxyServer.objects.get(url="http://proxy.creation.com"))
        self.assertEqual(
            message_template,
            MessageTemplate.objects.get(from_address="template_creation@example.com"),
        )

    def test_server_list(self):
        smtp_response = self.client.get(reverse_lazy("servers_api:smtp-server_list")).json()
        imap_response = self.client.get(reverse_lazy("servers_api:imap-server_list")).json()
        proxy_response = self.client.get(reverse_lazy("servers_api:proxy-server_list")).json()
        message_response = self.client.get(reverse_lazy("servers_api:message-template_list")).json()

        self.assertTrue(len(smtp_response) > 0)
        self.assertTrue(len(imap_response) > 0)
        self.assertTrue(len(proxy_response) > 0)
        self.assertTrue(len(message_response) > 0)
        self.assertEqual(smtp_response[0]["type"], ServerType.SMTP)
        self.assertEqual(imap_response[0]["type"], ServerType.IMAP)
        self.assertEqual(proxy_response[0]["type"], ServerType.PROXY)
        self.assertEqual(message_response[0]["from_address"], "template@example.com")

    def test_server_by_id(self):
        smtp_response = self.client.get(
            reverse_lazy("servers_api:smtp-server_by_id", kwargs={"pk": 1})
        )
        imap_response = self.client.get(
            reverse_lazy("servers_api:imap-server_by_id", kwargs={"pk": 2})
        )
        proxy_response = self.client.get(
            reverse_lazy("servers_api:proxy-server_by_id", kwargs={"pk": 3})
        )
        message_response = self.client.get(
            reverse_lazy("servers_api:message-template_by_id", kwargs={"pk": 1})
        )

        self.assertEqual(smtp_response.data["type"], ServerType.SMTP)
        self.assertEqual(imap_response.data["type"], ServerType.IMAP)
        self.assertEqual(proxy_response.data["type"], ServerType.PROXY)
        self.assertEqual(message_response.data["from_address"], "template@example.com")

    def test_wrong_id(self):
        smtp_response = self.client.get(
            reverse_lazy("servers_api:smtp-server_by_id", kwargs={"pk": 10})
        )
        imap_response = self.client.get(
            reverse_lazy("servers_api:imap-server_by_id", kwargs={"pk": 10})
        )
        proxy_response = self.client.get(
            reverse_lazy("servers_api:proxy-server_by_id", kwargs={"pk": 10})
        )
        message_response = self.client.get(
            reverse_lazy("servers_api:message-template_by_id", kwargs={"pk": 10})
        )

        self.assertEqual(smtp_response.data["error"], "No SMTPServer matches the given query.")
        self.assertEqual(imap_response.data["error"], "No IMAPServer matches the given query.")
        self.assertEqual(proxy_response.data["error"], "No ProxyServer matches the given query.")
        self.assertEqual(
            message_response.data["error"], "No MessageTemplate matches the given query."
        )
