FROM python:3-alpine3.20

WORKDIR /opt/server

COPY . .
RUN pip install -r requirements.txt
