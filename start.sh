#!/usr/bin/env bash
set -e

echo "Starting the mqtt_listener"
uv run python manage.py mqtt_listener &

echo "Starting the Django q2 tasks queue system"
uv run python manage.py q_cluster &

echo "Starting Gunicorn"
exec uv run gunicorn avix_api.wsgi:application --bind 0.0.0.0:${PORT:-1000}