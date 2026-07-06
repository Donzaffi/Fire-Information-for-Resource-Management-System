import os
import requests
import pandas as pd
import io
from flask import Flask, jsonify, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__, static_folder='web')

# Global variable to store processed fire data
fire_data = {"data": []}

def fetch_firms_data():
    """Fetches and parses NASA FIRMS CSV data."""
    global fire_data
    api_key = os.getenv('NASA_API_KEY')
    # URL for ESP (Spain) region, last 24 hours
    url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{api_key}/MODIS_NRT/ESP/1"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Parse CSV content
            df = pd.read_csv(io.StringIO(response.text))
            # Convert to dictionary/list for JSON output
            fire_data = {"data": df.to_dict(orient='records'), "last_update": pd.Timestamp.now().isoformat()}
            print(f"Successfully fetched {len(df)} fire records.")
    except Exception as e:
        print(f"Error fetching data: {e}")

# Scheduler: Run every 30 minutes
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
