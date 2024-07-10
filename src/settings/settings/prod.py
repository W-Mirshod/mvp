from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)
SQL_DEBUG = env.bool("SQL_DEBUG", False)

if SQL_DEBUG:
    MIDDLEWARE += ["utils.middleware.DebugQuerysetsWare"]
if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]


RUN_IN_DOCKER = env.bool("RUN_IN_DOCKER", False)
print(f"RUN_IN_DOCKER: {RUN_IN_DOCKER}")
if not RUN_IN_DOCKER:
    REDIS_HOST = env.str("REDIS_HOST_LOCAL", "redis")
    REDIS_PORT = env.str("REDIS_PORT_LOCAL", "6379")

# region Celery
BROKER_URL = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"
CELERY_BROKER_URL = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"

print(f"BROKER_URL: {BROKER_URL}")
print(f"CELERY_BROKER_URL: {CELERY_BROKER_URL}")

CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3600}
CELERY_CACHE_BACKEND = "default"
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = env.list("CELERY_ACCEPT_CONTENT")
CELERY_TASK_SERIALIZER = env.str("CELERY_TASK_SERIALIZER", "")
CELERY_RESULT_SERIALIZER = env.str("CELERY_RESULT_SERIALIZER", "")
CELERY_TIMEZONE = env.str("CELERY_TIMEZONE", "")
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# endregion


# region Database
if RUN_IN_DOCKER:
    DATABASES = {
        "default": {
            "ENGINE": env.str("SQL_ENGINE"),
            "NAME": env.str("SQL_DATABASE"),
            "USER": env.str("SQL_USER"),
            "PASSWORD": env.str("SQL_PASSWORD"),
            "HOST": env.str("SQL_HOST"),
            "PORT": env.str("SQL_PORT"),
        }
    }
else:
    DATABASES = {"default": env.db(var="DATABASE_URL")}
# endregion

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=[
        "http://localhost",
        "http://127.0.0.1",
    ],
)

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
