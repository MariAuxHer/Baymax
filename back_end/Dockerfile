#back_end/Dockerfile

FROM python:3.11
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy files into container
COPY . .

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
