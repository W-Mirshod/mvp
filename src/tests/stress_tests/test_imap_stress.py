import unittest
from imaplib import IMAP4_SSL
from concurrent.futures import ThreadPoolExecutor

def connect_imap(server, username, password):
    try:
        with IMAP4_SSL(server) as imap:
            imap.login(username, password)
            imap.select('inbox')
            imap.logout()
    except Exception as e:
        raise AssertionError(f"IMAP connection failed: {e}")

class IMAPStressTest(unittest.TestCase):
    def test_imap_stress(self):
        server = 'imap.example.com'
        username = 'user@example.com'
        password = 'password'
        num_connections = 100

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(connect_imap, server, username, password) for _ in range(num_connections)]
            for future in futures:
                future.result()
