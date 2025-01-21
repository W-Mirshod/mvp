#!/bin/sh

[ ! -d "logs" ] && mkdir logs/
[ ! -f "logs/django.log" ] && touch logs/django.log
[ ! -f "logs/apps_logging.log" ] && touch logs/apps_logging.log

# run a flower
celery -A celery_scripts.celery_app flower