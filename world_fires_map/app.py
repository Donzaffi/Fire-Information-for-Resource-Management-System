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

# Initialize Flask application
app = Flask(__name__, static_folder='web')
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)

# Global storage for fire data
fire_data = {"data": []}

def fetch_firms_data():
    """
    Fetches fire data from NASA FIRMS using the point-radius API endpoint.
    Format: /api/area/csv/{api_key}/{source}/{longitude},{latitude},{radius}/1
    """
    global fire_data
    
    # Retrieve configuration values from environment variables
    # These are populated by the run.sh script from the Home Assistant config
    api_key = os.getenv('NASA_API_KEY')
    lat = os.getenv('LATITUDE')
    lon = os.getenv('LONGITUDE')
    radius = os.getenv('RADIUS')
    
    # Ensure all required configuration values are present
    if not all([api_key, lat, lon, radius]):
        logger.error("Configuration missing! Ensure NASA_API_KEY, LATITUDE, LONGITUDE, and RADIUS are set.")
        return

    # NASA FIRMS point-radius endpoint
    # Note: Using {lon},{lat},{radius} order as required by the API
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{api_key}/MODIS_NRT/{lon},{lat},{radius}/1"
    
    logger.info(f"Fetching data for location: {lat}, {lon} with radius: {radius}km")
    
    try:
        response = requests.get(url, timeout=30)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse CSV response into a list of dictionaries
            reader = csv.DictReader(io.StringIO(response.text))
            fire_data = {"data": [row for row in reader]}
            logger.info(f"Successfully retrieved {len(fire_data['data'])} records.")
        else:
            # Log specific API errors (e.g., 400 Bad Request)
            logger.error(f"NASA API Error {response.status_code}: {response.text}")
            
    except Exception as e:
        logger.error(f"An error occurred during data fetching: {e}")

# Scheduler to trigger data update every 30 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_firms_data, trigger="interval", minutes=30)
scheduler.start()

# Route to serve the frontend
@app.route('/')
def index():
    return send_from_directory('web', 'index.html')

# API endpoint for the frontend to consume the data
@app.route('/api/data')
def get_data():
    return jsonify(fire_data)

if __name__ == '__main__':
    # Initial fetch to populate data on startup
    fetch_firms_data()
    # Run the application
    app.run(host='0.0.0.0', port=8080)
