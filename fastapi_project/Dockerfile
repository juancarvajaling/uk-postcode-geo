FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

LABEL maintainer="juancarvajaling@gmail.com"

COPY requirements.txt ./

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY file_loader /app/file_loader
