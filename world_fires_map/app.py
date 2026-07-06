import os
import requests
import csv
import io
import math
import logging
from flask import Flask, jsonify, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='web')

# Apply ProxyFix to support Home Assistant Ingress
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)

# Cache for storing fire data
fire_data = {"data": []}

def get_bounding_box(lat, lon, radius_km):
    """Calculates the bounding box (west, south, east, north) for a given radius."""
    # 1 degree of latitude is approximately 111 km
    deg_lat = float(radius_km) / 111.0
    # 1 degree of longitude depends on the latitude
    deg_lon = float(radius_km) / (111.0 * math.cos(math.radians(float(lat))))
    
    west = float(lon) - deg_lon
    south = float(lat) - deg_lat
    east = float(lon) + deg_lon
    north = float(lat) + deg_lat
    
    # Return comma-separated string required by FIRMS area API: min_lon,min_lat,max_lon,max_lat
    return f"{west:.4f},{south:.4f},{east:.4f},{north:.4f}"

def fetch_firms_data():
    """Fetches and parses CSV data from NASA FIRMS API."""
    global fire_data
    
    # Retrieve configuration from environment variables
    api_key = os.getenv('NASA_API_KEY')
    lat = os.getenv('LATITUDE')
    lon = os.getenv('LONGITUDE')
    radius = os.getenv('RADIUS_KM')

    if not api_key or not lat or not lon or not radius:
        logger.error("Configuration incomplete. Please check NASA_API_KEY, LATITUDE, LONGITUDE, and RADIUS_KM.")
        return

    # Calculate Bounding Box for the area endpoint
    bbox = get_bounding_box(lat, lon, radius)
    
    # URL for area search, last 24 hours
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{api_key}/MODIS_NRT/{bbox}/1"
    
    logger.info(f"Fetching data from URL: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        logger.info(f"API response status: {response.status_code}")
        
        if response.status_code == 200:
            # Parse CSV without pandas
            reader = csv.DictReader(io.StringIO(response.text))
            fire_data = {"data": [row for row in reader]}
            logger.info(f"Data updated successfully. Found {len(fire_data['data'])} fires.")
        else:
            logger.error(f"NASA API error: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Error while fetching NASA data: {e}")

# Scheduler to trigger data update every 30 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_firms_data, trigger="interval", minutes=30)
scheduler.start()

@app.route('/')
def index():
    """Serve the frontend static file."""
    return send_from_directory('web', 'index.html')

@app.route('/api/data')
def get_data():
    """Endpoint for the frontend to retrieve cached fire data."""
    return jsonify(fire_data)

@app.route('/api/config')
def get_config():
    """Returns the configured location settings to the frontend."""
    return jsonify({
        "lat": float(os.getenv('LATITUDE', 0)),
        "lon": float(os.getenv('LONGITUDE', 0)),
        "radius": float(os.getenv('RADIUS_KM', 100))
    })

if __name__ == '__main__':
    # Initial fetch when the application starts
    fetch_firms_data()
    # Run the web server on all interfaces
    app.run(host='0.0.0.0', port=8080)
