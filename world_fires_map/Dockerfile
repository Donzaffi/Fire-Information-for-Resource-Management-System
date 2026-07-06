# Use the current official Home Assistant base image
ARG BUILD_FROM=ghcr.io/hassio-addons/base:21.0.0
FROM $BUILD_FROM

# Install Python3 and pip
RUN apk add --no-cache python3 py3-pip

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code
COPY . /app/

# Set execution permissions for the start script
RUN chmod a+x /app/run.sh

# Use CMD to execute the run script
CMD ["/app/run.sh"]
