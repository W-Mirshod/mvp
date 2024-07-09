# users/tasks.py

from celery import Celery, shared_task
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.reverse import reverse_lazy


@shared_task
def send_verification_email_task(from_email, user_email, token):
    """
    Задача Celery для отправки верификационного email.

    Аргументы:
    - subject: Тема письма
    - message: Сообщение письма
    - from_email: Адрес отправителя
    - recipient_list: Список получателей
    """
    subject = "Email verification"
    message = "Thank you for registering on our website. Please verify your email:\n"
    link = "http://localhost:8000" + reverse_lazy("users_api:email_verify") + "?token=" + token
    recipient_list = (user_email,)
    send_mail(subject, message + link, from_email, recipient_list)
