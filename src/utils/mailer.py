from django.conf import settings
from django.core.mail import send_mail
from rest_framework.reverse import reverse_lazy


class Mailer:
    def __init__(self, from_email=settings.DEFAULT_FROM_EMAIL):
        self.from_email = from_email

    def send_verification_email(self, user_email, token):
        subject = "Email verification"
        message = "Thank you for registering on our website. Please verify your email:\n"
        link = "http://localhost:8000" + reverse_lazy("users_api:email_verify") + "?token=" + token
        recipient_list = (user_email,)

        send_mail(subject, message + link, self.from_email, recipient_list)
