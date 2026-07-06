#!/usr/bin/with-contenv bashio

# Read configuration from the UI
API_KEY=$(bashio::config 'nasa_api_key')
export NASA_API_KEY=$API_KEY

echo "Starting World Fires Map..."
python3 /app/app.py
