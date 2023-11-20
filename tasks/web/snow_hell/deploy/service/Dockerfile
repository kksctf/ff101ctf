FROM python:3.9-buster

WORKDIR /usr/src

# RUN apt-get update && apt-get install -y gnupg2 build-essential && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./main.py .
COPY ./front ./front

# /usr/local/bin/uvicorn
ENTRYPOINT [ "python3", "-m", "uvicorn", "main:app"]
CMD ["--log-level=warning", "--host", "0.0.0.0", "--port", "80", "--proxy-headers", "--forwarded-allow-ips", "*"]
