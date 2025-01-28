from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import logging

from apps.sentry.sentry_constants import SentryConstants
from apps.sentry.sentry_scripts import SendToSentry

logger = logging.getLogger(__name__)

MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()


def classify_email(email_content):
    """
    Classify whether an email is spam or not.
    :param email_content: str, the email content to classify.
    :return: bool, True if spam, False otherwise.
    """
    try:
        inputs = tokenizer(email_content, return_tensors="pt", truncation=True, padding=True, max_length=512)

        with torch.no_grad():
            outputs = model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=-1)

        spam_probability = probabilities[0][1].item()
        return spam_probability > 0.5
    except Exception as e:
        SendToSentry.send_scope_msg(
            scope_data={
                "message": f"IMAPDriver.check_connection(): Ex",
                "level": SentryConstants.SENTRY_MSG_ERROR,
                "tag": SentryConstants.SENTRY_TAG_GENERAL,
                "detail": "Unexpected error occurred while trying to classify email",
                "extra_detail": f"{e = }",
            }
        )
        logger.error("Unexpected error occurred while trying to classify email: %s", e)
        return False
