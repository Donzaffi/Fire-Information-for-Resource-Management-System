import os
import requests
import pandas as pd
import io
from flask import Flask, jsonify, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__, static_folder='web')
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)

fire_data = {"data": []}

def fetch_firms_data():
    global fire_data
    api_key = os.getenv('NASA_API_KEY')
    url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{api_key}/MODIS_NRT/ESP/1"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            fire_data = {"data": df.to_dict(orient='records')}
    except Exception as e:
        print(f"Error: {e}")

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
