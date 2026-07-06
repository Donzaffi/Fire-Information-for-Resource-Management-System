#!/usr/bin/with-contenv bashio

# Set the API key using bashio
export NASA_API_KEY=$(bashio::config 'nasa_api_key')

echo "Starting World Fires Map application..."

# Run the application
exec python3 /app/app.py
