# Use the official HA base image that does not enforce s6-overlay complexity
ARG BUILD_FROM=homeassistant/aarch64-base:latest
FROM $BUILD_FROM

# Install dependencies
RUN apk add --no-cache python3 py3-pip

# Set working directory
WORKDIR /app

# Install Python packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy files
COPY . /app/

# Set execution permission
RUN chmod a+x /app/run.sh

# This is the standard, simple way to start an add-on
CMD ["/app/run.sh"]
