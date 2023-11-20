FROM python:3.8-alpine as builder

WORKDIR /
COPY . .
RUN pip install -r requirements.txt

EXPOSE 2802
ENTRYPOINT ["python", "server.py"]
