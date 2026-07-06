# BUILD_FROM is provided automatically by the Home Assistant supervisor based on architecture
ARG BUILD_FROM
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

# Start the application
CMD ["/app/run.sh"]
