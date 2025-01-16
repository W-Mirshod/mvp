# from constance.test import override_config
# from django.core.exceptions import ImproperlyConfigured
# from django.test import TestCase
#
# from apps.mail_servers.choices import ServerType
# from apps.mail_servers.drivers import IMAPDriver, ProxyDriver, SMTPDriver
# from apps.mail_servers.models import IMAPServer, ProxyServer, Server, SMTPServer
# from apps.mailers.models import Event
#
#
# class DriverTestCase(TestCase):
#     def setUp(self):
#         self.server_smtp = Server.objects.create(
#             url="smtp.example.com",
#             port=587,
#             username="user@example.com",
#             password="password",
#             email_use_tls=True,
#             is_active=True,
#             type=ServerType.SMTP,
#         )
#         self.smtp_server = SMTPServer.objects.get(id=self.server_smtp.id)
#
#         self.server_imap = Server.objects.create(
#             url="imap.example.com",
#             port=993,
#             username="user@example.com",
#             password="password",
#             email_use_tls=True,
#             is_active=True,
#             type=ServerType.IMAP,
#         )
#         self.imap_server = IMAPServer.objects.get(id=self.server_imap.id)
#
#         self.server_proxy = Server.objects.create(
#             url="proxy.example.com",
#             port=993,
#             username="user@example.com",
#             password="password",
#             email_use_tls=True,
#             is_active=True,
#             type=ServerType.PROXY,
#         )
#         self.proxy_server = ProxyServer.objects.get(id=self.server_proxy.id)
#
#     def test_smtp_send_mail(self):
#         driver = SMTPDriver(server_name=self.smtp_server.url)
#         driver.add_message_to_queue(
#             subject="Test Subject",
#             message="This is a test message.",
#             recipient_list=["recipient@example.com"],
#         )
#         self.assertEqual(Event.objects.count(), 1)
#         event = Event.objects.first()
#         self.assertEqual(event.sent_message.results["subject"], "Test Subject")
#
#         with self.assertRaises(ImproperlyConfigured):
#             driver.process_queue()
#
#     @override_config(ENABLE_IMAP_SENDING=True)
#     def test_imap_send_mail(self):
#         driver = IMAPDriver(server_name=self.imap_server.url)
#         driver.add_message_to_queue(
#             subject="Test Subject",
#             message="This is a test message.",
#             recipient_list=["recipient@example.com"],
#         )
#         self.assertEqual(Event.objects.count(), 1)
#         event = Event.objects.first()
#         self.assertEqual(event.sent_message.results["subject"], "Test Subject")
#
#         with self.assertRaises(ImproperlyConfigured):
#             driver.process_queue()
#
#     def test_proxy_send_mail(self):
#         driver = ProxyDriver(server_name=self.proxy_server.url)
#         driver.add_message_to_queue(
#             subject="Test Subject",
#             message="This is a test message.",
#             recipient_list=["recipient@example.com"],
#         )
#         self.assertEqual(Event.objects.count(), 1)
#         event = Event.objects.first()
#         self.assertEqual(event.sent_message.results["subject"], "Test Subject")
#
#         with self.assertRaises(ImproperlyConfigured):
#             driver.process_queue()
