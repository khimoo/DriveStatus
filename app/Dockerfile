FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_NO_CACHE_DIR=on

RUN apt-get update && apt-get install -y \
  postgresql \
  libpq-dev \
  gcc \
  git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

WORKDIR /code
COPY requirements/ /code/
RUN pip install -r prod.txt
