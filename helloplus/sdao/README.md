# Django and Docker
This is a sample django project that will be used as the backend application server.
When it is accessed it just sends back an HTTP response of Hello World.

This also uses docker to maintain a consistant development environment.

# To run the test server using docker:

docker build -t django-serve . && docker compose up -d

# To run the test server from here:
python version: 3.11

python manage.py runserver --bind 0.0.0.0:8000
