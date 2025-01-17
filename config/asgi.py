"""
ASGI config for dj_config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/

install:
    - pip install uvicorn gunicorn
    - !!! DRF DO NOT SUPPORT ASYNC !!!

run:
    gunicorn -w 4 --log-level warning -k uvicorn.workers.UvicornWorker config.asgi:application
or:
    gunicorn -c ./server_config/gunicorn/gunicorn_sockets.py

"""

import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
    }
)
