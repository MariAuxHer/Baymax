#back_end/Dockerfile

FROM python:3.11
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python3.11","manage.py","runserver","0.0.0.0:8000"]
