import time
import math
import random
import joblib
import pandas as pd
from datetime import datetime
# 1. Load AI model
model = joblib.load("ai/potto_model.pkl")
print("       POTTO AI + GPS SYSTEM")
print("AI model loaded!")
print("GPS simulator started!")
print()
# 2. Starting GPS location
latitude = -18.1234
longitude = 31.0567
# 3. Generate GPS location
def generate_gps_location():
    global latitude
    global longitude
    # Simulate vehicle movement
    latitude += random.uniform(
        -0.0001,
        0.0001
    )
    longitude += random.uniform(
        -0.0001,
        0.0001
    )
    return latitude, longitude
# 4. Generate sensor reading
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
    elif event == "small_pothole":
        x = random.gauss(1.5, 1.0)
        y = random.gauss(-1.2, 1.0)
        z = random.gauss(13.0, 2.0)
    elif event == "severe_pothole":
        x = random.gauss(3.0, 1.2)
        y = random.gauss(-2.0, 1.2)
        z = random.gauss(17.0, 2.5)
    elif event == "braking":
        x = random.gauss(2.5, 1.0)
        y = random.gauss(0, 0.5)
        z = random.gauss(10.5, 0.8)
    elif event == "acceleration":
        x = random.gauss(-2.0, 0.8)
        y = random.gauss(0, 0.5)
        z = random.gauss(10.3, 0.8)
    else:
        x = random.gauss(0, 0.3)
        y = random.gauss(0, 0.3)
        z = random.gauss(9.8, 0.25)
    return x, y, z
# 5. Calculate magnitude
def calculate_magnitude(x, y, z):
    return math.sqrt(
        x**2 +
        y**2 +
        z**2
    )
# 6. Road events
events = [
    "normal_road",
    "rough_road",
    "speed_bump",
    "small_pothole",
    "severe_pothole",
    "braking",
    "acceleration"
]
# 7. Window size
WINDOW_SIZE = 20
# 8. Start Potto
try:
    while True:
        current_event = random.choice(events)
        magnitudes = []
        print("\n")
        print("NEW ROAD WINDOW")
        print("Actual simulated event:", current_event)
        # Collect sensor readings
        for i in range(WINDOW_SIZE):
            x, y, z = generate_sensor_reading(
                current_event
            )
            magnitude = calculate_magnitude(
                x,
                y,
                z
            )
            magnitudes.append(magnitude)
            time.sleep(0.05)
        # Feature engineering
        mean_magnitude = (
            sum(magnitudes) /
            len(magnitudes)
        )
        max_magnitude = max(magnitudes)
        min_magnitude = min(magnitudes)
        range_magnitude = (
            max_magnitude -
            min_magnitude
        )
        mean = mean_magnitude
        variance = sum(
            (value - mean) ** 2
            for value in magnitudes
        ) / len(magnitudes)
        std_magnitude = math.sqrt(
            variance
        )
        # Create feature DataFrame
        features = pd.DataFrame([{
            "mean_magnitude": mean_magnitude,
            "max_magnitude": max_magnitude,
            "min_magnitude": min_magnitude,
            "std_magnitude": std_magnitude,
            "range_magnitude": range_magnitude
        }])
        # AI prediction
        prediction = model.predict(
            features
        )
        probabilities = model.predict_proba(
            features
        )
        confidence = probabilities.max()
        # GPS
        lat, lon = generate_gps_location()
        # Timestamp
        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        # Display detection
        print("\nPOTTO DETECTION")
        print(
            "Road condition:",
            prediction[0]
        )
        print(
            f"Confidence: "
            f"{confidence * 100:.2f}%"
        )
        print(
            f"Latitude: {lat:.6f}"
        )
        print(
            f"Longitude: {lon:.6f}"
        )
        print(
            "Timestamp:",
            timestamp
        )
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\nPotto system stopped.")
    