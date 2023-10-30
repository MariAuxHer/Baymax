#!/bin/bash

# Install dependencies
echo "Installing python dependencies"
pip install -r requirements.txt

# Apply database migrations
echo "Apply database migrations"
python3.11 manage.py makemigrations back_end
python3.11 manage.py migrate

# Start server
echo "Starting server"
python3.11 manage.py runserver 0.0.0.0:8000