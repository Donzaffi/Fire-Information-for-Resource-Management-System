ARG BUILD_FROM=ghcr.io/home-assistant/{arch}-base-python:3.13

FROM ${BUILD_FROM}

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
