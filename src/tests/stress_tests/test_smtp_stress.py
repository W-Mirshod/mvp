import unittest
import smtplib
from concurrent.futures import ThreadPoolExecutor


def connect_smtp(server, port, username, password):
    try:
        with smtplib.SMTP(server, port) as smtp:
            smtp.login(username, password)
            smtp.quit()
    except Exception as e:
        raise AssertionError(f"SMTP connection failed: {e}")


class SMTPStressTest(unittest.TestCase):
    def test_smtp_stress(self):
        server = "smtp.example.com"
        port = 587
        username = "user@example.com"
        password = "password"
        num_connections = 100

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(connect_smtp, server, port, username, password)
                for _ in range(num_connections)
            ]
            for future in futures:
                future.result()


if __name__ == "__main__":
    unittest.main()
