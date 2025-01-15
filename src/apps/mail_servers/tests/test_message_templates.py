from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework_simplejwt.tokens import RefreshToken

from src.apps.mail_servers.models import MessageTemplate
from src.apps.mail_servers.tests.factories import MessageTemplateFactory
from src.apps.users.tests.factories import UserFactory
from src.utils.tests import CustomViewTestCase


class MessageTemplateViewTests(CustomViewTestCase):
    """
    ./manage.py test apps.mail_servers.tests.test_message_templates.MessageTemplateViewTests --settings=_dev.settings_test      # noqa: E501
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

        MessageTemplateFactory(
            id=1,
            from_address="template@example.com",
            template="Example template",
            message={"message": "Example message"},
        )

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/api/1.0/servers/message-templates/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse_lazy("servers_api:message-template_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_template(self):
        template = MessageTemplateFactory(
            id=2,
            from_address="template_creation@example.com",
            template="Example template creation",
            message={"message": "Example message"},
        )

        self.assertEqual(template, MessageTemplate.objects.get(id=2))

    def test_template_list(self):
        response = self.client.get(
            reverse_lazy("servers_api:message-template_list")
        ).json()

        self.assertTrue(len(response) > 0)
        self.assertEqual(response[0]["from_address"], "template@example.com")

    def test_template_by_id(self):
        response = self.client.get(
            reverse_lazy("servers_api:message-template_by_id", kwargs={"pk": 1})
        )

        self.assertEqual(response.data["from_address"], "template@example.com")

    def test_wrong_id(self):
        response = self.client.get(
            reverse_lazy("servers_api:message-template_by_id", kwargs={"pk": 10})
        )

        self.assertEqual(
            response.data["detail"], "No MessageTemplate matches the given query."
        )
