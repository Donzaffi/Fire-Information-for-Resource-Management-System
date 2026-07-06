#!/usr/bin/with-contenv bashio

# Retrieve configuration using the official Home Assistant helper
export NASA_API_KEY=$(bashio::config 'nasa_api_key')

echo "Starting World Fires Map application..."

# Exec ensures the process runs correctly under the s6 manager
exec python3 /app/app.py
