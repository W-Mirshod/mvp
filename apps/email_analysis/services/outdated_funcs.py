import requests
import logging

from apps.sentry.sentry_constants import SentryConstants
from apps.sentry.sentry_scripts import SendToSentry

from apps.mailers.models.message import SentMessage

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"


def classify_email(email_content):
    """
    Classify whether an email is spam or not using Ollama.
    :param email_content: str, the email content to classify.
    :return: bool, True if spam, False otherwise.
    """
    try:
        payload = {
            "model": "gemma",
            "prompt": (
                "You are an AI email classifier. Your task is to analyze the given email content and classify it as either SPAM or NOT SPAM.\n\n"
                "### Definition of SPAM:\n"
                "- Unwanted, irrelevant, or repetitive messages sent to many recipients.\n"
                "- Messages that include deceptive offers, scams, or phishing attempts.\n"
                "- Emails that promote products/services aggressively without prior consent.\n\n"
                "### Definition of NOT SPAM:\n"
                "- Legitimate emails from known senders.\n"
                "- Work-related or personal messages.\n"
                "- Emails containing relevant information requested by the recipient.\n\n"
                "### Response Rules:\n"
                "- If the email is SPAM, reply ONLY with: 'spam'.\n"
                "- If the email is NOT SPAM, reply ONLY with: 'not spam'.\n"
                "- Do NOT add explanations, extra words, or formatting.\n"
                "- Do NOT use variations like 'true/false' or 'yes/no'.\n\n"
                "Here is the email content:\n\n"
                f"\"{email_content}\""
            ),
            "stream": False,
        }

        response = requests.post(OLLAMA_URL, json=payload)

        if response.status_code != 200:
            logger.error(f"Ollama API error: {response.text}")
            return "Error"

        result = response.json()
        spam_result = result.get("response", "").strip().lower()

        return spam_result

    except Exception as e:
        SendToSentry.send_scope_msg(
            scope_data={
                "message": "classify_email(): Ex",
                "level": SentryConstants.SENTRY_MSG_ERROR,
                "tag": SentryConstants.SENTRY_TAG_GENERAL,
                "detail": "Unexpected error occurred while trying to classify email",
                "extra_detail": str(e),
            }
        )
        logger.error("Unexpected error occurred while trying to classify email: %s", e)
        return "Error"


def personalize_email(user, email_content):
    """
    Generate a personalized email based on the user's past messages.

    :param user: User instance
    :param email_content: str, the email content to personalize
    :return: str, the rewritten email content
    """
    try:
        recent_messages = (
            SentMessage.objects.filter(user=user)
            .order_by("-created_at")[:5]
        )

        conversation_history = "\n".join(
            [f"User: {msg.message}" for msg in recent_messages if msg.message]
        )

        prompt = (
            "You are an AI that helps users write emails in their own style.\n"
            "Below are previous messages written by the user.\n"
            "Use them as reference to rewrite the new email in the same style.\n\n"
            "Give only NEW email body, dont give anything else, only Improved Version\n"
            "### User's Previous Emails:\n"
            f"{conversation_history}\n\n"
            "### Email to Personalize:\n"
            f"{email_content}\n\n"
            "### Improved Version:\n"
        )

        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
        }
        response = requests.post(OLLAMA_URL, json=payload)


        if response.status_code != 200:
            logger.error(f"Ollama API error: {response.text}")
            return email_content

        result = response.json()
        personalized_email = result.get("response", "").strip()

        logger.info("Ollama Personalized Email: %s", personalized_email)
        return personalized_email

    except Exception as e:
        SendToSentry.send_scope_msg(
            scope_data={
                "message": "personalize_email(): Ex",
                "level": SentryConstants.SENTRY_MSG_ERROR,
                "tag": SentryConstants.SENTRY_TAG_GENERAL,
                "detail": "Unexpected error occurred while trying to personalize email",
                "extra_detail": str(e),
            }
        )
        logger.error("Unexpected error occurred while trying to personalize email: %s", e)
        return email_content
