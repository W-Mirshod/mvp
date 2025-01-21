#!/bin/sh


# run a flower
chmod -R 755 logs/
celery -A celery_scripts.celery_app flower