#!/usr/bin/with-contenv bashio
# Liest die Werte direkt aus der HA-Konfiguration
export NASA_API_KEY=$(bashio::config 'nasa_api_key')
export LAT=$(bashio::config 'latitude')
export LON=$(bashio::config 'longitude')
export RAD=$(bashio::config 'radius')

exec python3 /app/app.py
