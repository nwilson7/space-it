#!/bin/sh

# Wait for MySQL to be ready
while ! nc -z db 3306; do
  echo "Waiting for MySQL..."
  sleep 2
done

# Run migrations
python manage.py migrate --noinput

# Start Django
exec "$@"
