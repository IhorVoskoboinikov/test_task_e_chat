FROM python:3.10.8-slim
LABEL maintainer="voskoboinikov777@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
