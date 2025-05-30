#!/bin/bash
set -e

echo "Applying migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput
cp -r /app/collected_static/. /backend_static/static/

echo "Creating superuser..."
python manage.py create_su || true

echo "Creating test categories..."
python manage.py create_category || true

echo "Starting Gunicorn..."
exec "$@"
