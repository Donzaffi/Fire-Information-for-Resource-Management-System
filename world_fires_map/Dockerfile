# Use the official Home Assistant base image
ARG BUILD_FROM=ghcr.io/hassio-addons/base:21.0.0
FROM $BUILD_FROM

# Install Python3 and pip
RUN apk add --no-cache python3 py3-pip

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Create the s6-service directory and copy the run script
# s6-overlay will automatically pick up any script in /etc/services.d/
RUN mkdir -p /etc/services.d/app
RUN cp /app/run.sh /etc/services.d/app/run
RUN chmod a+x /etc/services.d/app/run
