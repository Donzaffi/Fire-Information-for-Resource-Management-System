#!/bin/bash
# Note: NASA_API_KEY is automatically injected by Home Assistant
# as an environment variable based on config.json

echo "Starting World Fires Map..."
python3 /app/app.py
