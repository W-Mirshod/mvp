import requests
import logging
from apps.email_analysis.services.prompts import PROMPTS
from django.conf import settings

logger = logging.getLogger(__name__)

OLLAMA_URL = settings.OLLAMA_URL

def call_ollama(model: str, prompt_key: str, **kwargs) -> str:
    """
    Calls Ollama API with a predefined prompt.
    :param model: AI model name (e.g., "gemma", "llama3").
    :param prompt_key: The key for the prompt in PROMPTS.
    :param kwargs: Data to fill into the prompt.
    :return: AI-generated response.
    """
    try:
        if prompt_key not in PROMPTS:
            raise ValueError(f"Prompt key '{prompt_key}' not found in PROMPTS.")

        prompt = PROMPTS[prompt_key].format(**kwargs)

        payload = {"model": model, "prompt": prompt, "stream": False}

        response = requests.post(OLLAMA_URL, json=payload, timeout=600)

        if response.status_code != 200:
            logger.error(f"Ollama API error: {response.text}")
            return None

        return response.json().get("response", "").strip()

    except requests.exceptions.Timeout:
        logger.error("Ollama request timed out!")
        return None

    except Exception as e:
        logger.error(f"Unexpected error in call_ollama: {e}")
        return None
