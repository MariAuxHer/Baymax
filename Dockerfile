# nginx/Dockerfile

FROM nginx:latest
WORKDIR /app
COPY nginx/nginx.conf /etc/nginx/nginx.conf
