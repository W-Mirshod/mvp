# from rest_framework import status
# from rest_framework.reverse import reverse_lazy
# from rest_framework_simplejwt.tokens import RefreshToken
#
# from apps.mail_servers.choices import ServerType
# from apps.mail_servers.models import SMTPServer
# from apps.mail_servers.tests.factories import SMTPServerFactory
# from apps.users.tests.factories import UserFactory
# from utils.tests import CustomViewTestCase
#
#
# class SMTPServerViewTests(CustomViewTestCase):
#     """
#     ./manage.py test apps.mail_servers.tests.test_smtp.SMTPServerViewTests --settings=_dev.settings_test      # noqa: E501
#     """
#
#     def setUp(self):
#         self.user = UserFactory(is_verified=True, is_active=True)
#         refresh = RefreshToken.for_user(self.user)
#         access = refresh.access_token
#         self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(access))
#
#         SMTPServerFactory(
#             id=1,
#             type=ServerType.SMTP,
#             url="http://smtp.example.com",
#             port=465,
#             password="password",
#             username="smtp@example.com",
#         )
#
#     def test_url_exists_at_desired_location(self):
#         response = self.client.get("/api/1.0/servers/smtp-servers/")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_url_accessible_by_name(self):
#         response = self.client.get(reverse_lazy("servers_api:smtp-server_list"))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_create_server(self):
#         smtp_server = SMTPServerFactory(
#             id=2,
#             type=ServerType.SMTP,
#             url="http://smtp.creation.com",
#             port=465,
#             password="password",
#             username="smtp_creation@example.com",
#         )
#
#         self.assertEqual(smtp_server, SMTPServer.objects.get(id=2))
#
#     def test_server_list(self):
#         response = self.client.get(reverse_lazy("servers_api:smtp-server_list")).json()
#
#         self.assertTrue(len(response) > 0)
#         self.assertEqual(response[0]["type"], ServerType.SMTP)
#
#     def test_server_by_id(self):
#         response = self.client.get(reverse_lazy("servers_api:smtp-server_by_id", kwargs={"pk": 1}))
#
#         self.assertEqual(response.data["type"], ServerType.SMTP)
#
#     def test_wrong_id(self):
#         response = self.client.get(reverse_lazy("servers_api:smtp-server_by_id", kwargs={"pk": 10}))
#
#         self.assertEqual(response.data["detail"], "No SMTPServer matches the given query.")
