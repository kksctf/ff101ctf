FROM python:3.8-alpine as builder

WORKDIR /
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "server.py"]
