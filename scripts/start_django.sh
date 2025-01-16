#!/bin/bash

echo "--- Clean logs and db_backup files ---"
rm ./logs/main_worker_*.log
rm ./logs/general_worker_*.log
rm ./logs/data_processing_*.log
rm ./logs/gunicorn.log
touch ./logs/gunicorn.log
touch ./logs/data_processing.log
touch ./logs/general_worker.log
touch ./logs/main_worker.log
sleep 0.1

echo "--- Do migration ---"
python manage.py migrate
sleep 0.1

echo "--- Collect static files ---"
python manage.py collectstatic --no-input
sleep 0.1

echo "--- Restart celery workers ---"
python manage.py runscript celery_scripts.restart_workers
sleep 0.1

echo "--- Start django server ---"
gunicorn -c ./server_config/gunicorn/gunicorn_config.py
