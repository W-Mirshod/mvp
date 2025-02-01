from apps.email_analysis.services.ollama_service import call_ollama

def classify_email(email_body: str) -> bool:
    """Classifies an email as spam or not spam."""
    result = call_ollama(model="gemma", prompt_key="spam_detection", email_body=email_body)
    return result == "spam"

def personalize_email(email_body: str, theme: str) -> str:
    """Rewrites the email while maintaining the given theme."""
    return call_ollama(model="llama3", prompt_key="email_personalization", email_body=email_body, theme=theme)

def fix_grammar(email_body: str) -> str:
    """Corrects grammar, spelling, and style issues in the email."""
    return call_ollama(model="mistral", prompt_key="grammar_fixer", email_body=email_body)

def summarize_email(email_body: str) -> str:
    """Summarizes the email, keeping the main points."""
    return call_ollama(model="llama3", prompt_key="email_summary", email_body=email_body)

def generate_subject(email_body: str) -> str:
    """Generates subject line suggestions for an email."""
    return call_ollama(model="llama3", prompt_key="subject_generator", email_body=email_body)

def analyze_sentiment(email_body: str) -> str:
    """Analyzes the sentiment of an email (Positive, Neutral, or Negative)."""
    return call_ollama(model="gemma", prompt_key="sentiment_analysis", email_body=email_body)

def generate_signature(email_body: str) -> str:
    """Generates a suitable email closing and signature."""
    return call_ollama(model="gemma", prompt_key="signature_generator", email_body=email_body)

def generate_email(theme: str) -> str:
    """Generates a full email based on a given theme or prompt."""
    return call_ollama(model="llama3", prompt_key="email_generation", theme=theme)
