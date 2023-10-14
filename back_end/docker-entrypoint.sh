#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python3.11 manage.py migrate

# create test user
echo "Creating sample user!"
echo "username: 'test'"
echo "password: 'test'"
printf 'test\n \n test\n test\n y\n' | python3.11 manage.py createsuperuser

# Start server
echo "Starting server"
python3.11 manage.py runserver 0.0.0.0:8000