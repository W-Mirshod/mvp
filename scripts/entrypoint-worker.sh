
until cd ./src
do
    echo "Waiting for server volume..."
done

# run a worker
# -A app - searches for celery.py within the directory app
celery --app=settings --broker="${CELERY_BROKER_URL}" --result-backend="${CELERY_RESULT_BACKEND}" worker -B --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler