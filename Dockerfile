FROM python:3.12-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        libpython3-dev \
        libpq-dev \
        gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

ENV APP__HOME_DIR=/mm
ENV PYTHONPATH=/mm/src

# set work directory
WORKDIR $APP__HOME_DIR

# set work directory
RUN mkdir -p $APP__HOME_DIR
RUN mkdir -p $APP__HOME_DIR/logs
RUN mkdir -p $APP__HOME_DIR/src
# RUN mkdir -p $APP__HOME_DIR/docker/backend
RUN mkdir -p $APP__HOME_DIR/src/media/attachments/

# install dependences
COPY ./requirements.txt /mm/requirements.txt
RUN pip install -r /mm/requirements.txt

RUN apt-get -y update
RUN apt-get install gettext -y

# set display port to avoid crash
ENV DISPLAY=:99

# set open port
EXPOSE 8000
