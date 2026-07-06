import os
import requests
import csv
import io
from flask import Flask, jsonify, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.middleware.proxy_fix import ProxyFix

# Initialize Flask app
app = Flask(__name__, static_folder='web')

# Apply ProxyFix to support Home Assistant Ingress
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)

# Cache for storing fire data
fire_data = {"data": []}

def fetch_firms_data():
    """Fetches and parses CSV data from NASA FIRMS API."""
    global fire_data
    api_key = os.getenv('NASA_API_KEY')
    # URL for ESP (Spain) region, last 24 hours
    url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{api_key}/MODIS_NRT/ESP/1"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Parse CSV without pandas
            reader = csv.DictReader(io.StringIO(response.text))
            fire_data = {"data": [row for row in reader]}
            print("Data updated successfully.")
    except Exception as e:
        print(f"Error while fetching NASA data: {e}")

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
