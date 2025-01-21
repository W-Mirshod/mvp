# import multiprocessing

wsgi_app = "config.asgi:application"
worker_class = "uvicorn.workers.UvicornWorker"
command = "./venv/bin/gunicorn"
pythonpath = "."
bind = ":8001"
workers = 4
raw_env = "DJANGO_SETTINGS_MODULE=config.settings"
errorlog = "./logs/gunicorn_sockets.log"
max_requests = 1000
max_requests_jitter = 100