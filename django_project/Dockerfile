FROM python:3.8-slim

LABEL maintainer="juancarvajaling@gmail.com"

WORKDIR /usr/src/app/near_postcode

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt update \
    && apt -y install netcat

COPY entrypoint.sh /
COPY near_postcode ./app/near_postcode
