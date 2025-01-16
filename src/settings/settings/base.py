import os
import environ
from pathlib import Path
from datetime import timedelta
from celery.schedules import crontab
from django.utils.crypto import get_random_string
from dotenv import dotenv_values


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

environ_values = dotenv_values(".env")


env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = environ_values.get("DEBUG")

def get_secret_key():
    if not environ_values.get("SECRET_KEY"):
        print("[agents_portal] No setting found for SECRET_KEY. Generating a random key...")
        return get_random_string(length=50)
    return environ_values.get("SECRET_KEY")


SECRET_KEY = get_secret_key()

ALLOWED_HOSTS = environ_values.get("ALLOWED_HOSTS").split(",")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "django_celery_results",
    "django_celery_beat",
    "src.apps.users",
    "src.apps.changelog",
    "src.apps.mail_servers",
    "src.apps.mailers",
    "src.apps.products",
    "src.apps.companies",
    "drf_yasg",
    "admin_extra_buttons",
    "constance",
    "constance.backends.database",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.changelog.middleware.LoggedInUserMiddleware",
]

ROOT_URLCONF = "settings.urls"

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

WSGI_APPLICATION = "settings.wsgi.application"

# region REST
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "utils.authentication.CustomJWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
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

#REDIS_URL = f"redis://:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}"
REDIS_DB = "0"
# endregion

# celery settings
CELERY_BROKER_URL = environ_values.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = environ_values.get("CELERY_RESULT_BACKEND")
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
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
# endregion

MAIN_HOST = "http://localhost:8000/"

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
