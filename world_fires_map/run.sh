#!/usr/bin/with-contenv bashio

# Use bashio to read the configuration. 
# This command is required by the supervisor to properly map the config.
export NASA_API_KEY=$(bashio::config 'nasa_api_key')

echo "Starting World Fires Map application..."

# 'exec' is the magic word here. It replaces the bash process with the python process.
# This makes Python PID 1 and satisfies s6-overlay.
exec python3 /app/app.py
