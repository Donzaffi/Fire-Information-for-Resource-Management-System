#!/usr/bin/with-contenv bashio

export NASA_API_KEY=$(bashio::config 'nasa_api_key')
export LATITUDE=$(bashio::config 'latitude')
export LONGITUDE=$(bashio::config 'longitude')
export RADIUS=$(bashio::config 'radius')


echo "Starting World Fires Map application..."

exec python3 /app/app.py
