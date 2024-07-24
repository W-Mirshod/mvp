FROM python:3.12-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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

# Настройка переменных окружения
ENV APP_HOME_DIR=/mm
ENV PYTHONPATH=$APP_HOME_DIR/src

# Создание необходимых директорий
RUN mkdir -p $APP_HOME_DIR/src $APP_HOME_DIR/logs $APP_HOME_DIR/src/media/attachments

# Установка зависимостей Python
COPY ./requirements.txt $APP_HOME_DIR/requirements.txt
RUN pip install -r $APP_HOME_DIR/requirements.txt

# Копирование исходного кода в контейнер
COPY . $APP_HOME_DIR/src

# Установка рабочего каталога
WORKDIR $APP_HOME_DIR/src

# Открытие порта
EXPOSE 8000

# Команда по умолчанию для запуска
CMD ["sh", "./scripts/entrypoint-wsgi-web.sh"]
