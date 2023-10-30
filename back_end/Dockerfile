#back_end/Dockerfile

FROM python:3.11
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
