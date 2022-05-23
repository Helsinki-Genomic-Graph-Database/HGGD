#!/bin/sh
gunicorn  --config ./src/gunicorn_config.py src.wsgi:app