import os
import requests
import csv
import io
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

def fetch_firms_data():
    """Fetches and parses CSV data from NASA FIRMS API."""
    global fire_data
    
    # Retrieve configuration from environment variables
    api_key = os.getenv('NASA_API_KEY')
    lat = os.getenv('LATITUDE')
    lon = os.getenv('LONGITUDE')
    radius = os.getenv('RADIUS_KM')

    if not api_key:
        logger.error("NASA_API_KEY is not set! Please configure it in the Add-on settings.")
        return

    logger.info(f"Fetching data for location {lat}, {lon} with radius {radius}km")

# URL for radius search using the area endpoint
    # Format: {api_key}/MODIS_NRT/{latitude},{longitude},{radius_km}/1
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{api_key}/MODIS_NRT/{lat},{lon},{radius}/1"
    
    try:
        response = requests.get(url, timeout=30)
        logger.info(f"API response status: {response.status_code}")
        
        if response.status_code == 200:
            # Parse CSV without pandas
            reader = csv.DictReader(io.StringIO(response.text))
            fire_data = {"data": [row for row in reader]}
            logger.info(f"Data successfully updated. Found {len(fire_data['data'])} fires.")
        else:
            logger.error(f"NASA API error: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Error fetching NASA data: {e}")

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

if __name__ == '__main__':
    # Initial fetch when the application starts
    fetch_firms_data()
    # Run the web server on all interfaces
    app.run(host='0.0.0.0', port=8080)
