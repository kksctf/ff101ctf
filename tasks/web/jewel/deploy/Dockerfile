FROM ruby:3-alpine

WORKDIR /app

COPY ./http_server.rb .
COPY ./index.html .
COPY ./flag.txt /

CMD ruby ./http_server.rb