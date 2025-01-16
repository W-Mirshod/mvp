from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.reverse import reverse_lazy, reverse


@shared_task
def send_verification_email_task(from_email: str, user_email: str, token: str) -> None:
    subject = "Email verification"
    message = "Thank you for registering on our website. Please verify your email:\n"

    verification_url = str(reverse_lazy("users_api:email_verify"))
    link = settings.MAIN_HOST + verification_url + "?token=" + token

    recipient_list = (user_email,)
    send_mail(subject, message + link, from_email, recipient_list)


@shared_task
def send_one_time_jwt_task(from_email: str, user_email: str, token: str) -> None:
    subject = "Reset password"
    message = "The link for reset password:\n"
    link = (
        settings.MAIN_HOST
        + reverse_lazy("users_api:restore_password")
        + "?token="
        + token
    )
    recipient_list = (user_email,)
    send_mail(subject, message + link, from_email, recipient_list)
