#!/bin/sh

# Wait for MySQL to be ready
while ! nc -z db 3306; do
  echo "Waiting for MySQL..."
  sleep 2
done

while ! nc -z redis 6379; do
  echo "Waiting for Redis..."
  sleep 2
done

# Run migrations
python manage.py migrate --noinput

# Start Celery worker in the background
echo "Starting Celery worker..."
celery -A myproject worker --loglevel=info &

# Start Celery Beat in the background
echo "Starting Celery Beat..."
celery -A myproject beat --loglevel=info &

# Start Django development server
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000

# This will ensure the script doesn't exit immediately, keeping the process running
wait
