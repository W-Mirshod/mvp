#!/bin/sh

# Для БД на хосте
#netstat -nr | grep '^0\.0\.0\.0' | awk '{print $2" host.docker.internal"}' >> /etc/hosts

# На случай если БД бдует долго запускаться
#while ! curl postgres:5432/ 2>&1 | grep '52'; do sleep 1; done

until cd ./src
do
    echo "Waiting for server volume..."
done


# Миграции и статика
until python manage.py migrate --noinput
do
    echo "Waiting for db to be ready..."
    sleep 2
done
python manage.py collectstatic --no-input --clear
django-admin makemessages --all --ignore=venv
django-admin compilemessages --ignore=venv

# User credentials
email=admin@example.com
password=admin123
echo "from apps.users.models import User; (User.objects.create_superuser(email='$email', password='$password', is_verified=True, is_active=True)) if not User.objects.filter(email='$email').exists() else False" | python3 manage.py shell

# Запуск самого проекта
#gunicorn --env DJANGO_SETTINGS_MODULE=settings.settings.local settings.wsgi:application --chdir /mm/src/ --bind 0.0.0.0:8000 --workers 2 --timeout 900 --error-logfile ../logs/gunicorn_web_error.log
#gunicorn settings.wsgi:application --chdir /mm/src/ --bind 0.0.0.0:8026 --workers 2 --timeout 900 --error-logfile ../logs/gunicorn_web_error.log
python manage.py runserver 0.0.0.0:8000 --settings=settings.settings.prod

exec "$@"
