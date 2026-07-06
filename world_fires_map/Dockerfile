# Nutze das offizielle Home Assistant Basis-Image
ARG BUILD_FROM=homeassistant/amd64-base:latest
FROM $BUILD_FROM

# Install Python3
RUN apk add --no-cache python3 py3-pip

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set execution permissions
RUN chmod a+x /app/run.sh

# Start the application
CMD ["/app/run.sh"]
