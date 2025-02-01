from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework_simplejwt.tokens import RefreshToken

from apps.mail_servers.tests.factories import MessageTemplateFactory
from apps.users.tests.factories import UserFactory


class SpamDetectionViewTests(APITestCase):
    """
    ./manage.py test apps.email_analysis.tests.test_spam_detection.SpamDetectionViewTests
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
        self.url = reverse_lazy("email_analysis_api:spam_detection")  # Update with your actual route name

    def test_missing_email_content(self):
        response = self.client.post(self.url, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)  # Check if 'email_content' is in response
        self.assertEqual(response.data, {"error": "Email content is required."})

    def test_detect_spam(self):
        """Test detection of a spam email"""
        spam_cases = [
            {"email_content": "Congratulations! You have won a free iPhone. Click here to claim now!"},
            {"email_content": "Urgent! Your account has been compromised. Reset your password immediately!"},
            {"email_content": "You've been selected for an exclusive prize. Claim your reward now!"},
            {"email_content": "Dear customer, we noticed unusual activity in your account. Verify now!"},
            {"email_content": "Make $5000 a day from home with this secret method. Limited spots available!"},
            {"email_content": "🚨 ALERT: Your subscription will be canceled unless you update your payment info now!"},
            {"email_content": "Win a free vacation to the Bahamas! Enter your details here."},
            {"email_content": "Get rich fast! Invest just $100 and earn $5000 in a week!"},
            {"email_content": "Limited-time offer! Buy now and get 80% off on our premium service."},
            {"email_content": "Click this link to claim your Amazon gift card - no purchase necessary!"}
        ]

        for spam_email in spam_cases:
            response = self.client.post(self.url, spam_email, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(response.data["is_spam"], ["spam", "not spam"])
            self.assertEqual(response.data["is_spam"], "spam")

    def test_detect_not_spam(self):
        """Test detection of a non-spam email"""
        not_spam_cases = [
            {"email_content": "Hello John, your report is due tomorrow. Please submit it by 10 AM."},
            {"email_content": "Reminder: Your dentist appointment is scheduled for Monday at 2 PM."},
            {"email_content": "Hey Alex, can we meet for lunch at 1 PM today? Let me know!"},
            {"email_content": "Team, please review the attached document before our meeting."},
            {"email_content": "Thank you for your purchase! Your order has been shipped."},
            {"email_content": "Invitation: Join us for a networking event next Thursday at 6 PM."},
            {"email_content": "Your password was successfully updated. If this wasn't you, contact support."},
            {"email_content": "Hi Sarah, I loved your presentation today! Looking forward to your next talk."},
            {"email_content": "Weekly newsletter: Top 10 productivity tips for remote work."},
            {"email_content": "Your bank statement for this month is now available. Log in to view it."}
        ]

        for not_spam_email in not_spam_cases:
            response = self.client.post(self.url, not_spam_email, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(response.data["is_spam"], ["spam", "not spam"])
            self.assertEqual(response.data["is_spam"], "not spam")

