#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python3.11 manage.py makemigrations back_end
python3.11 manage.py migrate

# collect static # files will be used by nginx
echo "Generating Django's static files" 
python3.11 manage.py collectstatic --noinput

# create super user
# auto create a test user

echo "Creating a test user with username: "test" and password: "test"" 
export DJANGO_SUPERUSER_PASSWORD="test"
python3.11 manage.py createsuperuser --username "test" --email "test@gmail.com" --noinput

# Start server
echo "Starting server"
python3.11 manage.py runserver 0.0.0.0:8000
