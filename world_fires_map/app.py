import os
import requests
import csv
import io
import logging
from flask import Flask, jsonify, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.middleware.proxy_fix import ProxyFix

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='web')
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)

fire_data = {"data": []}

def fetch_firms_data():
    global fire_data
    # Reading configuration from environment variables
    api_key = os.getenv('NASA_API_KEY')
    west = os.getenv('WEST', '-9.3')
    south = os.getenv('SOUTH', '36.0')
    east = os.getenv('EAST', '4.0')
    north = os.getenv('NORTH', '43.8')
    
    if not api_key:
        logger.error("NASA_API_KEY is missing!")
        return

    # NASA API format: .../api/area/csv/{api_key}/MODIS_NRT/{west},{south},{east},{north}/1
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{api_key}/MODIS_NRT/{west},{south},{east},{north}/1"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            reader = csv.DictReader(io.StringIO(response.text))
            fire_data = {"data": [row for row in reader]}
            logger.info(f"Successfully fetched {len(fire_data['data'])} records.")
        else:
            logger.error(f"NASA API Error {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Fetch failed: {e}")

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
