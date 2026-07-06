#!/usr/bin/with-contenv bashio

export NASA_API_KEY=$(bashio::config 'nasa_api_key')
export WEST=$(bashio::config 'west')
export SOUTH=$(bashio::config 'south')
export EAST=$(bashio::config 'east')
export NORTH=$(bashio::config 'north')

echo "Starting World Fires Map application..."
exec python3 /app/app.py
