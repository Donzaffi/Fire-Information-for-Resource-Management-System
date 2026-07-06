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

# Set execution permissions
RUN chmod a+x /app/run.sh

# The standard way to integrate with s6 in the HA base image:
# Use ENTRYPOINT so the script IS PID 1, preventing suexec errors.
ENTRYPOINT ["/app/run.sh"]
