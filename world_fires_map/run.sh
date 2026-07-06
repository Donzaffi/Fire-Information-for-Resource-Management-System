#!/bin/bash
# Get the API Key from Home Assistant configuration
export NASA_API_KEY=$(bashio::config 'nasa_api_key')

echo "Starting World Fires Map..."

# Simple python execution as PID 1
python3 /app/app.py
