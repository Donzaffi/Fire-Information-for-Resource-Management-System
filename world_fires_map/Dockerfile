ARG BUILD_FROM=ghcr.io/hassio-addons/base:21.0.0
FROM $BUILD_FROM

RUN apk add --no-cache python3 py3-pip

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Create the s6-service directory
RUN mkdir -p /etc/services.d/world_fires_map
# Move the run script into the service directory
RUN cp /app/run.sh /etc/services.d/world_fires_map/run
RUN chmod a+x /etc/services.d/world_fires_map/run

# NO CMD or ENTRYPOINT here! 
# The s6-overlay will automatically pick up the service from /etc/services.d/
