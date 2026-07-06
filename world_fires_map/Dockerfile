# Use the official base image
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

# Remove s6 service files that might be causing conflicts
RUN rm -rf /etc/services.d/*

# Run directly without relying on s6 service definitions
CMD ["python3", "/app/app.py"]
