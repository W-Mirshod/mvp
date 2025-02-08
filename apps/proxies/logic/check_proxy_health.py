from apps.proxies.models.proxies import Proxy
from apps.proxies.utils import check_single_proxy

from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

from apps.sentry.sentry_constants import SentryConstants
from apps.sentry.sentry_scripts import SendToSentry

logger = logging.getLogger(__name__)


class CheckProxyHealth:
    @staticmethod
    def check_proxy_health():
        proxies = Proxy.objects.all()

        with ThreadPoolExecutor(max_workers=100) as executor:
            future_to_proxy = {
                executor.submit(check_single_proxy, proxy): proxy for proxy in proxies
            }
            for future in as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    future.result()
                except Exception as e:
                    SendToSentry.send_scope_msg(
                        scope_data={
                            "message": f"CheckProxyHealth.check_proxy_health: Exception",
                            "level": SentryConstants.SENTRY_MSG_ERROR,
                            "tag": SentryConstants.SENTRY_TAG_REQUEST,
                            "detail": f"Error checking proxy {proxy.host}:{proxy.port}",
                            "extra_detail": str(e),
                        }
                    )
                    logger.error(
                        f"Error checking proxy {proxy.host}:{proxy.port} - {e}"
                    )
