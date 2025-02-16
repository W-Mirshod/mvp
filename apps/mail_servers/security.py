import bleach
import re
import logging

from typing import Any, Dict
from django.core.exceptions import ValidationError
from django.utils.html import escape

logger = logging.getLogger(__name__)


class SecurityUtils:
    ALLOWED_TAGS = [
        "p",
        "br",
        "strong",
        "em",
        "u",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "div",
        "span",
        "a",
        "img",
        "table",
        "tr",
        "td",
        "th",
        "tbody",
        "thead",
    ]

    ALLOWED_ATTRIBUTES = {
        "a": ["href", "title", "target"],
        "img": ["src", "alt", "title", "width", "height"],
        "*": ["class", "style"],
    }

    ALLOWED_STYLES = [
        "color",
        "font-family",
        "font-size",
        "font-weight",
        "text-align",
        "margin",
        "padding",
        "border",
        "background-color",
    ]

    @staticmethod
    def sanitize_html(content: str) -> str:
        """Sanitizes HTML content"""
        try:
            clean_html = bleach.clean(
                content,
                tags=SecurityUtils.ALLOWED_TAGS,
                attributes=SecurityUtils.ALLOWED_ATTRIBUTES,
                styles=SecurityUtils.ALLOWED_STYLES,
                strip=True,
            )
            return clean_html
        except Exception as e:
            logger.error(f"HTML sanitization failed: {str(e)}")
            return escape(content)

    @staticmethod
    def validate_email_template(template: Dict) -> Dict:
        """Validates email template"""
        required_fields = ["subject", "body"]
        for field in required_fields:
            if field not in template:
                raise ValidationError(f"Missing required field: {field}")

        # Sanitize HTML in the email body
        template["body"] = SecurityUtils.sanitize_html(template["body"])

        # Check for malicious content
        SecurityUtils.check_malicious_content(template["body"])

        return template

    @staticmethod
    def check_malicious_content(content: str) -> None:
        """Checks for malicious content"""
        patterns = [
            r"<script.*?>.*?</script>",
            r"javascript:",
            r"onerror=",
            r"onload=",
            r"eval\(",
            r"document\.cookie",
            r"alert\(",
        ]

        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                raise ValidationError(
                    f"Detected potentially malicious content: {pattern}"
                )

    @staticmethod
    def validate_file_upload(file_obj: Any) -> None:
        """Validates uploaded files"""
        # Check file size
        if file_obj.size > 10 * 1024 * 1024:  # 10MB
            raise ValidationError("File size exceeds limit")

        # Check extension
        allowed_extensions = [".txt", ".csv", ".json"]
        ext = file_obj.name.lower().split(".")[-1]
        if f".{ext}" not in allowed_extensions:
            raise ValidationError(f"File type not allowed: {ext}")

        # Check the content of the first bytes
        content_start = file_obj.read(512).decode("utf-8", errors="ignore")
        file_obj.seek(0)

        # Check for executable code
        if re.search(r"<\?php|#!/|import os|system\(", content_start):
            raise ValidationError("File contains potentially dangerous content")

    @staticmethod
    def validate_headers(headers: Dict) -> Dict:
        """Validates HTTP headers"""
        sanitized = {}
        for key, value in headers.items():
            # Remove potentially dangerous headers
            if key.lower() in ["cookie", "authorization"]:
                continue

            # Sanitize values
            if isinstance(value, str):
                sanitized[key] = SecurityUtils.sanitize_header_value(value)

        return sanitized

    @staticmethod
    def sanitize_header_value(value: str) -> str:
        """Sanitizes header values"""
        # Remove control characters and line breaks
        return re.sub(r"[\x00-\x1f\x7f]", "", value)
