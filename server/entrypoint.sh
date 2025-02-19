#!/bin/sh

echo "Waiting for PostgreSQL database to be ready..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "Database is ready!"

# Apply migrations
echo "Make database migrations..."
python manage.py makemigrations --noinput

# Apply migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Check Django is ready before starting Daphne
echo "Checking if Django is ready..."
python -c "
import sys
import time
import django
from django.db import connections
from django.core.exceptions import ImproperlyConfigured

for _ in range(10):
    try:
        django.setup()
        connections['default'].cursor()
        print('Django is ready!')
        sys.exit(0)
    except (ImproperlyConfigured, Exception):
        print('Django is not ready yet. Retrying...')
        time.sleep(1)

print('Django did not start properly. Exiting.')
sys.exit(1)
"

# Start Daphne server
echo "Starting Daphne server..."
exec daphne -b 0.0.0.0 -p 8000 countdown_project.asgi:application
