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

# region Database
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
