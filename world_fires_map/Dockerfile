ARG BUILD_FROM
FROM ${BUILD_FROM}

RUN apk add --no-cache \
    python3 \
    py3-pip

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install \
    --break-system-packages \
    --no-cache-dir \
    -r requirements.txt

COPY . .

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
