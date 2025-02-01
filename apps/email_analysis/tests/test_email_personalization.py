from django.contrib.auth import get_user_model
from django.test import TestCase
from apps.email_analysis.services.ai_functions import personalize_email
from apps.mailers.models.message import SentMessage
from unittest.mock import patch
import json

User = get_user_model()


class EmailPersonalizationTests(TestCase):
    """
    Test suite for the email personalization feature using Ollama.
    """

    def setUp(self):
        """
        Set up a test user and populate the database with past emails.
        """
        self.user = User.objects.create_user(email="test@example.com", password="testpassword")

        # Create past messages for the user to establish writing style
        SentMessage.objects.create(user=self.user, message="Hey team, let's catch up tomorrow.")
        SentMessage.objects.create(user=self.user, message="Reminder: The project deadline is Friday.")
        SentMessage.objects.create(user=self.user, message="Can you review the attached document?")
        SentMessage.objects.create(user=self.user, message="Let's schedule a meeting at 3 PM.")
        SentMessage.objects.create(user=self.user, message="Thanks for the update, sounds great!")

        self.new_email = "We have a new feature launching next week. Let me know if you have questions!"

    @patch("apps.email_analysis.services.spam_detection_service.requests.post")
    def test_personalize_email_with_history(self, mock_post):
        """
        Test if the personalized email incorporates the user's past messages.
        """
        mock_response_data = {"response": "Let's schedule a discussion next week about the new feature launch!"}
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response_data

        personalized_email = personalize_email(self.user, self.new_email)

        print(personalized_email)

        self.assertIsInstance(personalized_email, str)
        self.assertNotEqual(personalized_email, self.new_email)  # Ensure the response is changed
        self.assertIn("schedule a discussion", personalized_email.lower())

    @patch("apps.email_analysis.services.spam_detection_service.requests.post")
    def test_personalize_email_without_history(self, mock_post):
        """
        Test personalization when no previous messages exist.
        """
        # Clear past messages
        SentMessage.objects.filter(user=self.user).delete()

        mock_response_data = {"response": "Excited to share our new feature launching next week!"}
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response_data

        personalized_email = personalize_email(self.user, self.new_email)

        self.assertIsInstance(personalized_email, str)
        self.assertNotEqual(personalized_email, self.new_email)  # Ensure the response is modified
        self.assertIn("excited", personalized_email.lower())

    @patch("apps.email_analysis.services.spam_detection_service.requests.post")
    def test_personalize_email_handles_api_failure(self, mock_post):
        """
        Test how the function handles API failure.
        """
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = "Internal Server Error"

        personalized_email = personalize_email(self.user, self.new_email)

        self.assertEqual(personalized_email, self.new_email)

    # @patch("apps.email_analysis.services.spam_detection_service.requests.post")
    # def test_personalize_email_handles_empty_response(self, mock_post):
    #     """
    #     Test how the function handles an empty response from the API.
    #     """
    #     mock_post.return_value.status_code = 200
    #     mock_post.return_value.json.return_value = {}
    #
    #     personalized_email = personalize_email(self.user, self.new_email)
    #
    #     self.assertEqual(personalized_email, self.new_email)  # It should return the original message

