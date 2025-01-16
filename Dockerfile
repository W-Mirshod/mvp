FROM python:3.12-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /mm-back

# Установка зависимостей
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        libpython3-dev \
        libpq-dev \
        gcc \
        gettext && \
    rm -rf /var/lib/apt/lists/*

# Обновление pip
RUN pip install --upgrade pip

COPY requirements.txt .


RUN pip install -r requirements.txt


COPY . .


EXPOSE 8000

# Команда по умолчанию для запуска
RUN chmod +x ./scripts/start_django.sh
