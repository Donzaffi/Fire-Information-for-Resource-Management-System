#!/usr/bin/with-contenv bashio

# Retrieve configuration using the bashio helper
export NASA_API_KEY=$(bashio::config 'nasa_api_key')

echo "Starting World Fires Map application..."

# Exec ensures python becomes PID 1, satisfying s6-overlay's requirements
exec python3 /app/app.py
