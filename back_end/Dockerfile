#back_end/Dockerfile

FROM python:3.11
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app

# CMD START 
# Install dependencies

CMD ["bash", "/app/docker-entrypoint.sh"]

# CMD END
# ENTRYPOINT [ "./app/docker-entrypoint.sh" ]
