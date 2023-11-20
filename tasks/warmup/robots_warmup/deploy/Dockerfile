FROM python:3.8-slim-buster

WORKDIR /python-docker

RUN pip3 install flask

COPY . .

CMD [ "python3", "main.py"]