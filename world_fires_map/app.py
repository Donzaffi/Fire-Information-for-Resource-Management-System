import os
import requests
import csv
import io
import logging
from flask import Flask, jsonify, send_from_directory

# ... (Logging & Flask Setup) ...

def fetch_firms_data():
    global fire_data
    api_key = os.getenv('NASA_API_KEY')
    
    # Werte aus den HA-Variablen (ohne Hardcodierung)
    lat = float(os.getenv('LAT'))
    lon = float(os.getenv('LON'))
    radius_km = float(os.getenv('RAD'))
    
    # 1 Grad Längengrad/Breitengrad entsprechen ca. 111 km
    deg_delta = radius_km / 111.0
    
    # BBOX Berechnung: West, South, East, North
    # Wichtig: West = lon - delta, East = lon + delta, etc.
    west = round(lon - deg_delta, 4)
    south = round(lat - deg_delta, 4)
    east = round(lon + deg_delta, 4)
    north = round(lat + deg_delta, 4)
    
    # Die API verlangt explizit West,South,East,North
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{api_key}/MODIS_NRT/{west},{south},{east},{north}/1"
    
    # ... (Rest wie gehabt) ...
