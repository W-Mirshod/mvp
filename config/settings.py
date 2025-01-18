import os
from pathlib import Path
from datetime import timedelta
from celery.schedules import crontab
from dotenv import dotenv_values


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ_values = dotenv_values(BASE_DIR / ".env")


DEBUG = environ_values.get("DEBUG")


SECRET_KEY = environ_values.get("SECRET_KEY")

ALLOWED_HOSTS = environ_values.get("ALLOWED_HOSTS").split(",")
CORS_ORIGIN_WHITELIST = environ_values.get("CORS_ORIGIN_WHITELIST").split(",")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
   # "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "django_celery_results",
    "django_celery_beat",
    "apps.users",
    "apps.changelog",
    "apps.mail_servers",
    "apps.mailers",
    "apps.products",
    "apps.companies",
    "drf_yasg",
    "admin_extra_buttons",
    "constance",
    "constance.backends.database",
]

MIDDLEWARE = [
  #  "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.changelog.middleware.LoggedInUserMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# region REST
REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": [
        "utils.authentication.CustomJWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
}
# endregion

# region JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(environ_values.get("ACCESS_TOKEN_LIFETIME", 15))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(environ_values.get("REFRESH_TOKEN_LIFETIME_DAYS", 1))),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
}
# endregion

AUTH_USER_MODEL = "users.User"
LOGIN_URL = "rest_framework:login"
LOGOUT_URL = "rest_framework:logout"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

MIN_PASSWORD_LENGTH = 8

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": MIN_PASSWORD_LENGTH,
        },
    },
    {
        "NAME": "utils.validators.NumberValidator",
        "OPTIONS": {
            "min_digits": 1,
        },
    },
    {
        "NAME": "utils.validators.UppercaseValidator",
    },
    {
        "NAME": "utils.validators.LowercaseValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = str(BASE_DIR / "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# region Redis
REDIS_PASS = environ_values.get("REDIS_PASS")
REDIS_HOST = environ_values.get("REDIS_HOST")
REDIS_PORT = environ_values.get("REDIS_PORT")

REDIS_URL = f"redis://:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}"

REDIS_DB = "0"
# endregion

# celery config
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_BEAT_SCHEDULE = {
    "test-periodic-task": {
        "task": "apps.mail_servers.tasks.test_periodic_task",
        "schedule": crontab(minute="*/1"),
    },
    'process-new-mail-queue-every-3-seconds': {
        'task': 'apps.mail_servers.tasks.process_new_mail_queue',
        'schedule': 3.0,
    },
    'process-in-process-mail-queue-every-3-seconds': {
        'task': 'apps.mail_servers.tasks.process_in_process_mail_queue',
        'schedule': 3.0,
    },
}

# endregion

# region CONSTANCE
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_CONFIG = {
    "ENABLE_SMTP_SENDING": (False, "Enable or disable SMTP sending"),
    "ENABLE_IMAP_SENDING": (False, "Enable or disable IMAP sending"),
    "ENABLE_PROXY_SENDING": (False, "Enable or disable proxy sending"),
}
# endregion

# region CORS
CORS_ALLOWED_ORIGINS = environ_values.get("CORS_ALLOWED_ORIGINS").split(",")
# endregion

MAIN_HOST = environ_values.get("MAIN_HOST","http://localhost:8000/" )

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



# SECURITY WARNING: don't run with debug turned on in production!

SQL_DEBUG = environ_values.get("SQL_DEBUG")

if SQL_DEBUG:
    MIDDLEWARE += ["utils.middleware.DebugQuerysetsWare"]
if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]


SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CSRF_TRUSTED_ORIGINS = environ_values.get("CSRF_TRUSTED_ORIGINS").split(",")
#CSRF_COOKIE_SECURE = environ_values.get("CSRF_COOKIE_SECURE")
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = environ_values.get("CSRF_COOKIE_HTTPONLY")

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


"""Email config ->"""
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587  # 587 for TLS, 465 for SSL
EMAIL_HOST_USER = environ_values.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = environ_values.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = environ_values.get("DEFAULT_FROM_EMAIL", "")
"""<- Email config"""

"""Django channels ->"""
ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}
"""<- Django channels"""