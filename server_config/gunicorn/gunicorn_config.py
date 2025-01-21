import multiprocessing

wsgi_app = "config.wsgi:application"
command = "./venv/bin/gunicorn"
pythonpath = "."
bind = ":8000"
workers = multiprocessing.cpu_count() * 2 + 1
raw_env = "DJANGO_SETTINGS_MODULE=config.settings"
errorlog = "./logs/gunicorn.log"
max_requests = 1000
max_requests_jitter = 100
timeout = 30
graceful_timeout = 30
