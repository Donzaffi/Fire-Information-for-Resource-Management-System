# Use the official Home Assistant base image for aarch64 as a fallback
ARG BUILD_FROM=homeassistant/aarch64-base:latest
FROM $BUILD_FROM

# Install Python3 and pip
RUN apk add --no-cache python3 py3-pip

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Set execution permissions for the start script
RUN chmod a+x /app/run.sh

# Ensure the container starts the run.sh script correctly
ENTRYPOINT ["/app/run.sh"]
