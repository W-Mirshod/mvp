import os
from pathlib import Path
from datetime import timedelta

import sentry_sdk
from celery.schedules import crontab
from dotenv import dotenv_values

from celery_scripts.constants import CeleryConstants

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ_values = dotenv_values(BASE_DIR / ".env")


DEBUG = environ_values.get("DEBUG")


SECRET_KEY = environ_values.get("SECRET_KEY")
FERNET_SECRET_KEY = environ_values.get("FERNET_SECRET_KEY")

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
    #
    "django_extensions",
    "django_prometheus",
    "django_celery_results",
    "django_celery_beat",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
    "admin_extra_buttons",
    "constance",
    "constance.backends.database",
    #
    "silk",
    #
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    "health_check.contrib.celery",
    "health_check.contrib.celery_ping",
    "health_check.contrib.redis",
    #
    "anymail",
    #
    "apps.users",
    "apps.changelog",
    "apps.mail_servers",
    "apps.mailers",
    "apps.products",
    "apps.companies",
    "apps.proxies",
    "apps.campaign",
    "apps.backend_mailer",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "silk.middleware.SilkyMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.changelog.middleware.LoggedInUserMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
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


"""SIMPLE_JWT ->"""
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        hours=int(environ_values.get("ACCESS_TOKEN_LIFETIME", 15))
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=int(environ_values.get("REFRESH_TOKEN_LIFETIME", 1))
    ),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS512",
    "SIGNING_KEY": environ_values.get("JWT_SECRET"),
    "VERIFYING_KEY": environ_values.get("JWT_SECRET"),
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}
"""<- SIMPLE_JWT"""
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
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
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

# REDIS_URL = f"redis://:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}"
REDIS_URL = "redis://localhost:6379/0"

REDIS_DB = "0"
# endregion


"""Celery settings ->"""
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_CONNECTION_RETRY = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_IMPORTS = (
    "apps.mail_servers.tasks",
    "apps.users.tasks",
)

CELERY_DEFAULT_QUEUE = CeleryConstants.DEFAULT_QUEUE
CELERY_DEFAULT_EXCHANGE = CeleryConstants.DEFAULT_QUEUE
CELERY_DEFAULT_ROUTING_KEY = CeleryConstants.DEFAULT_QUEUE

CELERY_BEAT_SCHEDULE = {
    # "test-periodic-task": {
    #     "task": "apps.mail_servers.tasks.test_periodic_task",
    #     "schedule": crontab(minute="*/1"),
    # },
    "process-new-mail-queue-every-3-seconds": {
        "task": "apps.mail_servers.tasks.process_new_mail_queue",
        "schedule": 3.0,
    },
    "process-in-process-mail-queue-every-3-seconds": {
        "task": "apps.mail_servers.tasks.process_in_process_mail_queue",
        "schedule": 3.0,
    },
}
"""<- Celery settings"""
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

MAIN_HOST = environ_values.get("MAIN_HOST", "http://localhost:8000/")

DATABASES = {
    "default": {
        "ENGINE": "django_prometheus.db.backends.postgresql",
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

"""Security->"""
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = environ_values.get("CSRF_TRUSTED_ORIGINS").split(",")
SESSION_COOKIE_DOMAIN = environ_values.get("DOMAIN", None)
SECURE_HSTS_SECONDS = 3600  # 1h
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

"""<-Security"""
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

"""CASH ->"""
CACHES = {
    "default": {
        "BACKEND": "django_prometheus.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
        "KEY_PREFIX": "mm-back-main",
    }
}

""" <- CASH"""


if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]

# region SWAGGER
SWAGGER_SETTINGS = {
    "DEFAULT_API_URL": MAIN_HOST,
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

"""sentry.io settings ->"""
USE_SENTRY = environ_values.get("USE_SENTRY", "true") == "true"
SENTRY_ENVIRONMENT_NAME = environ_values.get("SENTRY_ENVIRONMENT_NAME", "unknown")
if USE_SENTRY:

    def traces_sampler(sampling_context: dict) -> float:
        if "celery_job" in sampling_context.keys():
            return 0
        return 0.1

    sentry_sdk.init(
        dsn=environ_values.get("SENTRY_DSN", ""),
        traces_sampler=traces_sampler,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1,
        send_default_pii=True,
        environment=SENTRY_ENVIRONMENT_NAME,
    )
"""<- sentry.io settings"""


"""Logging settings ->"""
DJANGO_LOG_LEVEL = "WARNING"
APP_LOG_LVL = environ_values.get("APP_LOG_LVL", "INFO")
LOGS_DIR = "logs"

FILE_DJANGO = BASE_DIR / LOGS_DIR / "django.log"
FILE_APPS_LOGS = BASE_DIR / LOGS_DIR / "apps_logging.log"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} | {asctime} | {filename} ({lineno}) | {funcName} | {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} | {funcName} ({lineno}) | {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file_django": {
            "level": DJANGO_LOG_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "interval": 1,
            "backupCount": 10,
            "filename": FILE_DJANGO,
            "formatter": "verbose",
        },
        "file": {
            "level": APP_LOG_LVL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "interval": 1,
            "backupCount": 10,
            "filename": FILE_APPS_LOGS,
            "formatter": "verbose",
        },
        "console": {
            "level": APP_LOG_LVL,
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ("file_django", "console"),
            "level": DJANGO_LOG_LEVEL,
            "propagate": True,
        },
        "app": {
            "handlers": ("file", "console"),
            "level": APP_LOG_LVL,
            "propagate": True,
        },
        "celery_scripts": {
            "handlers": ("file", "console"),
            "level": APP_LOG_LVL,
            "propagate": True,
        },
        "dj_config": {
            "handlers": ("file", "console"),
            "level": APP_LOG_LVL,
            "propagate": True,
        },
        "help_scripts": {
            "handlers": ("file", "console"),
            "level": APP_LOG_LVL,
            "propagate": True,
        },
        "locust_testing": {
            "handlers": ("file", "console"),
            "level": APP_LOG_LVL,
            "propagate": True,
        },
    },
}
"""<- Logging settings"""

"""DEBUG_TOOLBAR ->"""
if DEBUG:
    INTERNAL_IPS = ("127.0.0.1",)
    DEBUG_TOOLBAR_CONFIG = {
        "IS_RUNNING_TESTS": False,
    }
    DEBUG_TOOLBAR_PANELS = (
        "debug_toolbar.panels.history.HistoryPanel",
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        # "debug_toolbar.panels.sql.SQLPanel",  # ! uncomment if 'sql_debug/'
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    )

    INSTALLED_APPS = ("debug_toolbar", *INSTALLED_APPS)
    MIDDLEWARE = (*MIDDLEWARE, "debug_toolbar.middleware.DebugToolbarMiddleware")
"""<- DEBUG_TOOLBAR"""

""" HEALTH CHECK ->"""

HEALTH_CHECK = {
    "SUBSETS": {
        "startup-probe": ["MigrationsHealthCheck", "DatabaseBackend"],
        "liveness-probe": ["DatabaseBackend", "CacheBackend"],
        "readiness-probe": ["DatabaseBackend", "CacheBackend", "CeleryHealthCheck"],
        "custom-checks": ["StorageHealthCheck", "RedisHealthCheck"],
        # "COMPANIES_CHECKS": ("apps.companies.health_check.v1.health_check_companies.CompaniesHealthCheck",)
    }
}
""" <- HEALTH CHECK """

""" SILK CONFIG ->"""

SILKY_MAX_RECORDED_REQUESTS = 10**8
SILKY_MAX_RECORDED_REQUESTS_CHECK_PERCENT = 10
SILKY_MAX_REQUEST_BODY_SIZE = -1
SILKY_MAX_RESPONSE_BODY_SIZE = 1024
SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True
SILKY_META = True
SILKY_ANALYZE_QUERIES = True
SILKY_INTERCEPT_PERCENT = 50
SILKY_SENSITIVE_KEYS = {
    "username",
    "api",
    "token",
    "key",
    "secret",
    "password",
    "signature",
}
SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_RESULT_PATH = "/silk_storage/"

SILKY_DYNAMIC_PROFILING = [
    {
        "module": "apps.mail_servers.views.v1.views_mail_servers",
        "function": "SMTPServerView.retrieve",
    }
]
"""<-  SILK CONFIG """

""" POST OFFICE ->"""

POST_OFFICE = {
    "BATCH_SIZE": 100,
    "QUEUE_NAME": "email-queue",
    "DEFAULT_PRIORITY": "high",
    "CELERY_ENABLED": True,
}

""" <-POST OFFICE"""
