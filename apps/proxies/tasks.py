from celery import app
from apps.proxies.logic.check_proxy_health import CheckProxyHealth
import logging


logger = logging.getLogger(__name__)


@app.shared_task
def check_proxy_health():
    CheckProxyHealth.check_proxy_health()
