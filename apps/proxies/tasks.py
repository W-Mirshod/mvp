from celery import app

from apps.proxies.models.proxies import Proxy
from apps.proxies.utils import check_single_proxy

from concurrent.futures import ThreadPoolExecutor, as_completed
import logging


logger = logging.getLogger(__name__)


@app.shared_task
def check_proxy_health():
    proxies = Proxy.objects.all()

    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_proxy = {executor.submit(check_single_proxy, proxy): proxy for proxy in proxies}
        for future in as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            try:
                future.result()
            except Exception as e:
                logger.error(f'Error checking proxy {proxy.host}:{proxy.port} - {e}')
