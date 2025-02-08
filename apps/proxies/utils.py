from datetime import datetime
from typing import Set, Tuple, Optional, List, Dict

from apps.proxies.checker import ProxyChecker
from apps.proxies.models.proxies import Proxy
from apps.proxies.models.configs import ProxyConfig
from apps.users.models import User


class CheckProxyUtils:
    @staticmethod
    def check_single_proxy(proxy: Proxy, user: User = None) -> Proxy:
        checker = ProxyChecker()

        config = ProxyConfig.objects.filter(author=user).first()
        if config:
            checker.proxy_judges = config.judge
            checker.timeout = config.timeout

        proxy_address = f"{proxy.host}:{proxy.port}"
        auth_params = (
            {"user": proxy.username, "password": proxy.password}
            if proxy.username and proxy.password
            else {}
        )

        response = checker.check_proxy(proxy_address, **auth_params)

        if response:
            if not proxy.is_active:
                proxy.country = response["country"]
                proxy.country_code = response["country_code"]
                proxy.anonymity = response["anonymity"]
                proxy.timeout = response["timeout"]
                proxy.is_active = True
        else:
            proxy.is_active = False

        proxy.last_time_checked = datetime.now()
        proxy.save()

        return proxy


class GetExistingProxies:
    @staticmethod
    def get_existing_proxies() -> Set[str]:
        return set(f"{proxy.host}:{proxy.port}" for proxy in Proxy.objects.all())


class ValidateCreateProxy:
    @staticmethod
    def validate_and_create_proxy(
        host: str,
        port: int,
        username: Optional[str],
        password: Optional[str],
        existing_proxies: Set[str],
    ) -> Tuple[Optional[str], Optional[str]]:
        proxy_key = f"{host}:{port}"
        if proxy_key in existing_proxies:
            return None, f"Proxy {proxy_key} already exists."
        else:
            Proxy.objects.create(
                host=host, port=int(port), username=username, password=password
            )
            return proxy_key, None


class ProcessProxies:
    @staticmethod
    def process_proxies(
        proxies: List[Dict[str, Optional[str]]], existing_proxies: Set[str]
    ) -> Tuple[List[str], List[str]]:
        created_proxies = []
        errors = []

        for proxy in proxies:
            host = proxy.get("host")
            port = proxy.get("port")
            username = proxy.get("username")
            password = proxy.get("password")

            if host and port:
                proxy_key, error = ValidateCreateProxy.validate_and_create_proxy(
                    host, int(port), username, password, existing_proxies
                )
                if proxy_key:
                    created_proxies.append(proxy_key)
                if error:
                    errors.append(error)

        return created_proxies, errors
