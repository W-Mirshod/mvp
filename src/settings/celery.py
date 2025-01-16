import os
from celery import Celery
from dotenv import dotenv_values

environ_values = dotenv_values(".env")


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src')

app = Celery('mm_backend')
CELERY_BROKER_URL = environ_values.get("CELERY_BROKER_URL")
app.conf.broker_url = CELERY_BROKER_URL

app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач
app.autodiscover_tasks()

