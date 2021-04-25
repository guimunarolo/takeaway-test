FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
ADD . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080
