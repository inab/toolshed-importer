# syntax=docker/dockerfile:1
FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ca-certificates \
    gcc \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip setuptools wheel
ENV STATIC_DEPS=true
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /toolshed/logs

CMD ["python", "main.py", "-l=DEBUG", "-d=/toolshed/logs/summary.log"]