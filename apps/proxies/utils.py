from datetime import datetime

from .checker import ProxyChecker
from .models.proxies import Proxy


def check_single_proxy(proxy):

    checker = ProxyChecker()

    response = checker.check_proxy(
        f'{proxy.host}:{proxy.port}',
        user=proxy.username,
        password=proxy.password
    ) if proxy.username and proxy.password else checker.check_proxy(
        f'{proxy.host}:{proxy.port}')

    if not response:
        proxy.is_active = False

    elif proxy.is_active is None or not proxy.is_active:
        proxy.country = response['country']
        proxy.is_active = True
        proxy.country_code = response['country_code']
        proxy.anonymity = response['anonymity']
        proxy.timeout = response['timeout']

    proxy.last_time_checked = datetime.now()
    proxy.save()

    return proxy


def get_existing_proxies():
    return set(f"{proxy.host}:{proxy.port}" for proxy in Proxy.objects.all())


def validate_and_create_proxy(host, port, username, password, existing_proxies):
    proxy_key = f"{host}:{port}"
    if proxy_key in existing_proxies:
        return None, f"Proxy {proxy_key} already exists."
    else:
        Proxy.objects.create(
            host=host,
            port=int(port),
            username=username,
            password=password
        )
        return proxy_key, None


def process_proxies(proxies, existing_proxies):
    created_proxies = []
    errors = []

    for proxy in proxies:
        host = proxy.get('host')
        port = proxy.get('port')
        username = proxy.get('username', None)
        password = proxy.get('password', None)

        if host is not None and port is not None:
            proxy_key, error = validate_and_create_proxy(host, port, username, password, existing_proxies)
            if proxy_key:
                created_proxies.append(proxy_key)
            if error:
                errors.append(error)

    return created_proxies, errors
