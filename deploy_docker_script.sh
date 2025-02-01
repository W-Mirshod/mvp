#!/bin/bash

echo "--- Update Python image ---"
docker pull python:3.12
sleep 0.1

echo "--- Update Redis image ---"
docker pull redis:latest
sleep 0.1

echo "--- Update Grafana image ---"
docker pull grafana/grafana
sleep 0.1

echo "--- Update Prometheus image ---"
docker pull prom/prometheus
sleep 0.1

echo "--- Update Postgres image ---"
docker pull postgres:latest
sleep 0.1

echo "--- Update Node Exporter image ---"
docker pull prom/node-exporter
sleep 0.1

echo "--- Update Email Engine image ---"
docker pull postalsys/emailengine:latest
sleep 0.1


echo "--- Build docker compose ---"
docker compose -f docker-compose.yml -f docker-compose-monitoring.yml build
sleep 0.1

echo "--- Check docker images ---"
docker images
sleep 0.1

echo "--- Start docker compose ---"
docker compose -f docker-compose.yml -f docker-compose-monitoring.yml up -d
sleep 0.1
