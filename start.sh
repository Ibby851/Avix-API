#!/usr/bin/env bash
set -e
echo "Applying database migrations"
uv run python manage.py migrate --noinput
echo "Starting Gunicorn"
exec uv run gunicorn avix_api.wsgi:application --bind 0.0.0.0:${PORT:-1000}