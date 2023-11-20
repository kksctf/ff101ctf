FROM python:3.11.5

RUN apt update && apt install -y gcc libpq-dev curl && apt clean

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app
CMD ["python", "app.py"]
