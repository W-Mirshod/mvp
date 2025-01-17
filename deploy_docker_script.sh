#!/bin/bash

echo "--- Update Python image ---"
docker pull python:3.12
sleep 0.1

echo "--- Update Redis image ---"
docker pull redis:latest
sleep 0.1

echo "--- Update Postgres image ---"
docker pull postgres:latest
sleep 0.1

echo "--- Build docker compose ---"
docker compose -f docker-compose.yml
sleep 0.1

echo "--- Check docker images ---"
docker images
sleep 0.1

echo "--- Start docker compose ---"
docker compose -f docker-compose.yml  up -d
sleep 0.1
