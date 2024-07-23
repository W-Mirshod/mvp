import unittest
import requests
from concurrent.futures import ThreadPoolExecutor

def connect_proxy(url, proxy):
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy})
        assert response.status_code == 200
    except Exception as e:
        raise AssertionError(f"Proxy connection failed: {e}")

class ProxyStressTest(unittest.TestCase):
    def test_proxy_stress(self):
        url = 'http://example.com'
        proxy = 'http://proxy.example.com:8080'
        num_connections = 100

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(connect_proxy, url, proxy) for _ in range(num_connections)]
            for future in futures:
                future.result()
