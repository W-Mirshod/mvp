
from src.settings.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = environ_values.get("DEBUG")
SQL_DEBUG = environ_values.get("SQL_DEBUG")

if SQL_DEBUG:
    MIDDLEWARE += ["utils.middleware.DebugQuerysetsWare"]
if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]


# RUN_IN_DOCKER = environ_values.get("RUN_IN_DOCKER")
#
# if not RUN_IN_DOCKER:
#     REDIS_HOST = environ_values.get("REDIS_HOST")
#     REDIS_PORT = environ_values.get("REDIS_PORT")
#
# # region Celery
# BROKER_URL = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"
# CELERY_BROKER_URL = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"


CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3600}
CELERY_CACHE_BACKEND = "default"
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = environ_values.get("CELERY_ACCEPT_CONTENT")
CELERY_TASK_SERIALIZER = environ_values.get("CELERY_TASK_SERIALIZER")
CELERY_RESULT_SERIALIZER = environ_values.get("CELERY_RESULT_SERIALIZER")
CELERY_TIMEZONE = environ_values.get("CELERY_TIMEZONE")
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# endregion


# region Database
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": environ_values.get("DB_NAME"),
        "USER": environ_values.get("DB_USER"),
        "PASSWORD": environ_values.get("DB_PASSWORD"),
        "HOST": environ_values.get("DB_HOST"),
        "PORT": environ_values.get("DB_PORT"),
        "CONN_MAX_AGE": 30,
        "CONN_HEALTH_CHECKS": True,
    }
}

# endregion

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CSRF_TRUSTED_ORIGINS = environ_values.get("CSRF_TRUSTED_ORIGINS").split(",")


if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

# region SWAGGER
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {"type": "basic"},
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"},
    },
}
# endregion


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


"""Email settings ->"""
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587  # 587 for TLS, 465 for SSL
EMAIL_HOST_USER = environ_values.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = environ_values.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = environ_values.get("DEFAULT_FROM_EMAIL", "")
"""<- Email settings"""

