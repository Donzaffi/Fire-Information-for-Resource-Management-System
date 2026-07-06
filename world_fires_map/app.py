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

app = Flask(__name__, static_folder='web')
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)

fire_data = {"data": []}

def fetch_firms_data():
    """Fetches data using the reliable map_data endpoint."""
    global fire_data
    api_key = os.getenv('NASA_API_KEY')
    
    if not api_key:
        logger.error("NASA_API_KEY is missing!")
        return

    # Use the map_data endpoint which is standard for FIRMS integrations
    # source: MODIS_NRT, area_coords: Spain roughly (lat/lon bounds)
    # The structure: /map_data/country/csv/{api_key}/{source}/{country_code}/{day_range}
    # Or more reliably, the global map data structure:
    url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{api_key}/MODIS_NRT/ESP/1"
    
    # HINWEIS: Wenn der Länder-Endpunkt weiterhin 400 liefert, 
    # nutzt die Integration von janfajessen meist den globalen Datensatz 
    # und filtert im Python-Code nach Koordinaten. 
    # Versuche diese URL, falls ESP/1 immer noch fehlschlägt:
    # url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{api_key}/MODIS_NRT/world/1"

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
