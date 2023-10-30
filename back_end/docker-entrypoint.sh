#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python3.11 manage.py makemigrations back_end
python3.11 manage.py migrate

# collect static # files will be used by nginx
python3.11 manage.py collectstatic --noinput

# Start server
echo "Starting server"
python3.11 manage.py runserver 0.0.0.0:8000