#!/usr/bin/with-contenv bashio

# Use bashio to get the configuration and set it as an environment variable
# This ensures it is available to the python script
export NASA_API_KEY=$(bashio::config 'nasa_api_key')

echo "Starting World Fires Map application..."

# Run python directly. We do not need sudo or suexec here, 
# as the container runs as root by default.
python3 /app/app.py
