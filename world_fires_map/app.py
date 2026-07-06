import os
import requests
import csv
import io
import logging
from flask import Flask, jsonify, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging for Home Assistant
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='web')
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)

fire_data = {"data": []}

def fetch_firms_data():
    """Fetches and parses CSV data from NASA FIRMS API."""
    global fire_data
    api_key = os.getenv('NASA_API_KEY')
    
    # Log the status of the API key (obscured for security)
    if not api_key:
        logger.error("NASA_API_KEY is missing! Check your Add-on configuration.")
        return
    else:
        logger.info(f"Fetching data with API Key starting with: {api_key[:4]}...")

    url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{api_key}/MODIS_NRT/ESP/1"
    
    try:
        response = requests.get(url, timeout=30)
        logger.info(f"NASA API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            # Parse CSV
            reader = csv.DictReader(io.StringIO(response.text))
            data = [row for row in reader]
            fire_data = {"data": data}
            logger.info(f"Successfully updated data. Found {len(data)} fire records.")
        else:
            logger.error(f"NASA API returned error: {response.text}")
            
    except Exception as e:
        logger.error(f"Error while fetching NASA data: {str(e)}")

# Scheduler to trigger data update every 30 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_firms_data, trigger="interval", minutes=30)
scheduler.start()

@app.route('/')
def index():
    return send_from_directory('web', 'index.html')

@app.route('/api/data')
def get_data():
    return jsonify(fire_data)

if __name__ == '__main__':
    fetch_firms_data()
    app.run(host='0.0.0.0', port=8080)
