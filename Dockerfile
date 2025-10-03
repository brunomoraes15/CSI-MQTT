FROM python:3.11-slim

WORKDIR /workspace

RUN apt-get update && pip install --no-cache-dir -r requirements.txt
