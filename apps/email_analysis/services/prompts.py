PROMPTS = {
    "spam_detection": (
        "You are an AI email classifier. Your task is to analyze the given email content and classify it as either SPAM or NOT SPAM.\n\n"
        "### Definitions:\n"
        "- **SPAM**: Unwanted, irrelevant, or repetitive messages sent to many recipients, deceptive offers, scams, phishing attempts, or aggressive promotions.\n"
        "- **NOT SPAM**: Legitimate emails from known senders, work-related or personal messages, or requested information.\n\n"
        "### Response Rules:\n"
        "- If the email is spam, reply with: `spam`\n"
        "- If the email is not spam, reply with: `not spam`\n"
        "- Do NOT add explanations, formatting, or extra words.\n\n"
        "{email_body}"
    ),

    "email_personalization": (
        "Rewrite the following email in a more engaging and user-friendly manner while keeping its original meaning intact.\n\n"
        "### Rules:\n"
        "- Keep the original message, do NOT remove key details.\n"
        "- Adapt the tone to match the given theme.\n"
        "- Use a natural, friendly, and engaging tone.\n"
        "- Do NOT add explanations, formatting, or extra words.\n"
        "- Do NOT introduce any new ideas, just improve readability.\n\n"
        "- The rewritten email MUST reflect the original theme: {theme}\n\n"
        "{email_body}\n\n"
        "### Rewritten Email:\n"
    ),

    "grammar_fixer": (
        "You are an AI grammar corrector. Your ONLY task is to correct grammar, punctuation, and spelling mistakes in the provided email.\n\n"
        "### NON-NEGOTIABLE RULES:\n"
        "- Do NOT change the sentence structure.\n"
        "- Do NOT rewrite or rephrase any part of the email.\n"
        "- Do NOT add or remove words (except for necessary corrections).\n"
        "- Do NOT add explanations, introductions, or formatting.\n"
        "- Do NOT modify the style or tone of the email.\n"
        "- Reply with ONLY the corrected email, nothing else.\n\n"
        "{email_body}"
    ),

    "email_summary": (
        "Summarize the following email while keeping only the key points.\n\n"
        "### Rules:\n"
        "- Include only the most important details.\n"
        "- Keep it concise and clear.\n"
        "- Do NOT add explanations, formatting, or extra words.\n\n"
        "- Do NOT add any additional text like 'Here is the corrected email' or anything like that.\n\n"
        "{email_body}\n\n"
        "### Summary:\n"
    ),

    "subject_generator": (
        "Generate exactly three professional, engaging, and relevant subject lines for the following email.\n\n"
        "### Rules:\n"
        "- Keep each subject line between 5-10 words.\n"
        "- Make them clear, engaging, and relevant.\n"
        "- Reply with ONLY the three subject lines, each on a new line.\n"
        "- Do NOT add explanations, formatting, or extra words.\n\n"
        "- Do NOT add any additional text like 'Here is the corrected email' or anything like that.\n\n"
        "{email_body}\n\n"
        "### Subject Lines:\n"
    ),

    "sentiment_analysis": (
        "Analyze the sentiment of the following email and classify it as Positive, Neutral, or Negative.\n\n"
        "### Rules:\n"
        "- If the email expresses enthusiasm, gratitude, or positivity, reply with: `Positive`\n"
        "- If the email is neutral or factual, reply with: `Neutral`\n"
        "- If the email contains complaints, frustration, or negativity, reply with: `Negative`\n"
        "- Reply with ONLY one of these three words.\n"
        "- Do NOT add explanations, formatting, or extra words.\n\n"
        "- Do NOT add any additional text like 'Here is the corrected email' or anything like that.\n\n"
        "{email_body}\n\n"
        "### Sentiment:\n"
    ),

    "signature_generator": (
        "Generate a suitable email closing and signature based on the tone and formality of the following email.\n\n"
        "### Rules:\n"
        "- If the email is formal, use a professional closing (e.g., `Best regards`, `Sincerely`).\n"
        "- If the email is informal, use a friendly closing (e.g., `Thanks`, `Take care`).\n"
        "- Reply with ONLY the closing and signature.\n"
        "- Do NOT add explanations, formatting, or extra words.\n\n"
        "- Do NOT add any additional text like 'Here is the corrected email' or anything like that.\n\n"
        "{email_body}\n\n"
        "### Closing & Signature:\n"
    ),

    "email_generation": (
        "Generate a well-structured email based on the following theme.\n\n"
        "### Rules:\n"
        "- The email must have a clear greeting, body, and closing.\n"
        "- Maintain a professional tone relevant to the theme.\n"
        "- Reply with ONLY the email body (no subject line, explanations, or formatting).\n\n"
        "- Do NOT add any additional text like 'Here is the corrected email' or anything like that.\n\n"
        "{theme}\n\n"
        "### Generated Email:\n"
    ),
}
