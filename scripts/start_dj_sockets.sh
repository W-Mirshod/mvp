#!/bin/bash

touch ./logs/gunicorn_sockets.log
sleep 0.1
gunicorn -c ./server_config/gunicorn/gunicorn_sockets.py
