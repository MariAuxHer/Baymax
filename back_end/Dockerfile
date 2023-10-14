#back_end/Dockerfile

FROM python:3.11
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN python3.11 manage.py migrate 

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
