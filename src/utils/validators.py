import re

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class NumberValidator(object):
    def __init__(self, min_digits=0):
        self.min_digits = min_digits

    def validate(self, password, user=None):
        if not len(re.findall(r"\d", password)) >= self.min_digits:
            raise ValidationError(
                detail={
                    "error": _(
                        f"The password must contain at least {self.min_digits} digit(s), 0-9."
                    )
                },
                code="password_no_number",
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_digits)d digit(s), 0-9."
            % {"min_digits": self.min_digits}
        )


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall("[A-Z]", password):
            raise ValidationError(
                detail={"error": _("The password must contain at least 1 uppercase letter, A-Z.")},
                code="password_no_upper",
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 uppercase letter, A-Z.")


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall("[a-z]", password):
            raise ValidationError(
                detail={"error": _("The password must contain at least 1 lowercase letter, a-z.")},
                code="password_no_lower",
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 lowercase letter, a-z.")


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r"[()[\]{}|\\`~!@#$%^&*_\-+=;:'\",<>./?]", password):
            raise ValidationError(
                detail={
                    "error": _(
                        "The password must contain at least 1 symbol: "
                        + r"()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
                    )
                },
                code="password_no_symbol",
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 symbol: " + r"()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )
