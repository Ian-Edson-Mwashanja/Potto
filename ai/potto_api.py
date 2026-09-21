import random
import time
import math
import requests
import joblib
import pandas as pd
from datetime import datetime
# LOAD AI MODEL
model = joblib.load("ai/potto_model.pkl")
# FLASK API ADDRESS
API_URL = "http://127.0.0.1:5000/api/anomalies"
# GPS STARTING LOCATION
latitude = -18.1234
longitude = 31.0567
# SENSOR SIMULATION
def generate_sensor_reading(event):

    if event == "normal_road":
        x = random.gauss(0, 0.3)
        y = random.gauss(0, 0.3)
        z = random.gauss(9.8, 0.25)

    elif event == "rough_road":
        x = random.gauss(0, 0.8)
        y = random.gauss(0, 0.8)
        z = random.gauss(10.5, 1.0)

    elif event == "speed_bump":
        x = random.gauss(0, 1.2)
        y = random.gauss(0, 1.2)
        z = random.gauss(13.5, 2.0)

    elif event == "braking":
        x = random.gauss(2.5, 1.0)
        y = random.gauss(0, 0.5)
        z = random.gauss(10.5, 0.8)

    elif event == "acceleration":
        x = random.gauss(-2.0, 0.8)
        y = random.gauss(0, 0.5)
        z = random.gauss(10.3, 0.8)

    elif event == "small_pothole":
        x = random.gauss(1.5, 1.0)
        y = random.gauss(-1.2, 1.0)
        z = random.gauss(13.0, 2.0)

    elif event == "severe_pothole":
        x = random.gauss(3.0, 1.2)
        y = random.gauss(-2.0, 1.2)
        z = random.gauss(17.0, 2.5)
    else:
        x = 0
        y = 0
        z = 9.8
    return x, y, z
# CALCULATE MAGNITUDE
def calculate_magnitude(x, y, z):

    return math.sqrt(
        x**2 +
        y**2 +
        z**2
    )
# GENERATE GPS LOCATION
def generate_gps_location():
    global latitude
    global longitude
    latitude += random.uniform(-0.0001, 0.0001)
    longitude += random.uniform(-0.0001, 0.0001)
    return latitude, longitude
# DETERMINE SEVERITY
def determine_severity(condition):

    if condition == "severe_pothole":
        return "severe"

    elif condition == "small_pothole":
        return "moderate"

    elif condition == "rough_road":
        return "moderate"

    elif condition == "speed_bump":
        return "low"
    else:
        return "low"
# SEND DETECTION TO API
def send_to_api(condition, confidence, latitude, longitude):
    severity = determine_severity(condition)
    data = {
        "type": condition,
        "severity": severity,
        "confidence": confidence,
        "latitude": latitude,
        "longitude": longitude,
        "device_id": "POTTO-001"
    }
    try:
        response = requests.post(
            API_URL,
            json=data
        )
        if response.status_code == 201:
            print("Successfully sent to Potto API!")
        else:
            print("API error:")
            print(response.status_code)
            print(response.text)
    except requests.exceptions.ConnectionError:
        print("Could not connect to Flask API.")
        print("Make sure backend/app.py is running.")
# MAIN PROGRAM
events = [
    "normal_road",
    "rough_road",
    "speed_bump",
    "small_pothole",
    "severe_pothole",
    "braking",
    "acceleration"
]
try:
    while True:
        print("        POTTO ROAD MONITOR")
        event = random.choice(events)
        print("Simulated event:", event)
        readings = []
        # Collect 20 sensor readings
        for i in range(20):
            x, y, z = generate_sensor_reading(event)
            magnitude = calculate_magnitude(x, y, z)
            readings.append({
                "x": x,
                "y": y,
                "z": z,
                "magnitude": magnitude
            })
            time.sleep(0.05)
        # FEATURE ENGINEERING
        df = pd.DataFrame(readings)
        features = {
            "mean_magnitude": df["magnitude"].mean(),
            "max_magnitude": df["magnitude"].max(),
            "min_magnitude": df["magnitude"].min(),
            "std_magnitude": df["magnitude"].std(),
            "range_magnitude": (
                df["magnitude"].max()
                -
                df["magnitude"].min()
            )
        }
        feature_data = pd.DataFrame([features])
        # AI PREDICTION
        prediction = model.predict(feature_data)[0]
        probabilities = model.predict_proba(feature_data)[0]
        confidence = max(probabilities)
        # GPS
        lat, lon = generate_gps_location()
        # TIMESTAMP
        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:S"
        )
        # DISPLAY RESULT
        print("\nAI DETECTION")
        print("Road condition:", prediction)
        print(
            "Confidence:",
            f"{confidence * 100:.2f}%"
        )
        print("\nLOCATION")
        print("Latitude:", lat)
        print("Longitude:", lon)
        print("\nTimestamp:", timestamp)
        # SEND TO BACKEND
        send_to_api(
            prediction,
            confidence,
            lat,
            lon
        )
        time.sleep(2)
except KeyboardInterrupt:
    print("\nPotto monitoring stopped.")