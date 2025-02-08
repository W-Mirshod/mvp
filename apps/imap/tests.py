from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from .models import EmailAccount
from .services import IMAPService

User = get_user_model()

class EmailViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='password'
        )
        self.email_account = EmailAccount.objects.create(
            email='test@example.com',
            password='password',
            is_active=True
        )
        self.client.force_authenticate(user=self.user)
        self.imap_patcher = patch('imaplib.IMAP4_SSL')
        self.mock_imap = self.imap_patcher.start()
        self.mock_connection = MagicMock()
        self.mock_imap.return_value = self.mock_connection
        self.mock_connection.search.return_value = ('OK', [b'1 2 3 4 5'])
        self.mock_connection.fetch.return_value = ('OK', [(b'1', b'From: test@example.com\r\nSubject: Test Email\r\nDate: Tue, 15 Nov 2023 14:30:00 -0500\r\n\r\nTest content')])

    def tearDown(self):
        self.imap_patcher.stop()

    def test_check_folder(self):
        self.mock_connection.select.return_value = ('OK', [b'10'])
        url = reverse('imap:email-check')
        response = self.client.get(url, {'folder': 'INBOX'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_latest_emails(self):
        self.mock_connection.select.return_value = ('OK', [b'10'])
        url = reverse('imap:email-latest')
        response = self.client.get(url, {'folder': 'INBOX', 'limit': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('emails', response.data)

    def test_latest_emails_invalid_limit(self):
        url = reverse('imap:email-latest')
        response = self.client.get(url, {'folder': 'INBOX', 'limit': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('django.core.cache.cache.get')
    @patch('django.core.cache.cache.set')
    def test_folder_stats(self, mock_cache_set, mock_cache_get):
        mock_cache_get.return_value = None
        self.mock_connection.select.return_value = ('OK', [b'10'])
        self.mock_connection.search.return_value = ('OK', [b'1 2 3'])
        
        url = reverse('imap:email-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('inbox', response.data)
        self.assertIn('total', response.data['inbox'])
