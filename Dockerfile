# nginx/Dockerfile

FROM nginx:latest
WORKDIR /app

# copy nginx conf 
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

# copy front end static to app static
COPY ./back_end/static/ /app/static/
