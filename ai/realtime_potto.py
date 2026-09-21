import time
import math
import random
import joblib
import pandas as pd
# 1. Load the trained AI model
model = joblib.load("ai/potto_model.pkl")
print("        POTTO REAL-TIME SYSTEM")
print("AI model loaded successfully!")
print("Starting simulated sensor...\n")
# 2. Generate simulated sensor reading
def generate_sensor_reading(event):
    """
    Simulates an accelerometer reading.
    """
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
# 3. Calculate acceleration magnitude
def calculate_magnitude(x, y, z):
    return math.sqrt(
        x**2 +
        y**2 +
        z**2
    )
# 4. Create a list of possible road events
events = [
    "normal_road",
    "rough_road",
    "speed_bump",
    "small_pothole",
    "severe_pothole",
    "braking",
    "acceleration"
]
# 5. Number of readings per window
WINDOW_SIZE = 20
# 6. Start the real-time simulation
try:
    while True:
        # Randomly select a road event
        current_event = random.choice(events)
        print("Road event:", current_event)
        magnitudes = []
        # Generate 20 sensor readings
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
            print(
                f"Reading {i + 1:02d}: "
                f"X={x:.2f}, "
                f"Y={y:.2f}, "
                f"Z={z:.2f}, "
                f"Magnitude={magnitude:.2f}"
            )
            # Simulate sensor sampling delay
            time.sleep(0.1)
        # 7. Feature engineering
        mean_magnitude = sum(magnitudes) / len(magnitudes)
        max_magnitude = max(magnitudes)
        min_magnitude = min(magnitudes)
        range_magnitude = (
            max_magnitude -
            min_magnitude
        )
        # Calculate standard deviation
        mean = mean_magnitude
        variance = sum(
            (x - mean) ** 2
            for x in magnitudes
        ) / len(magnitudes)
        std_magnitude = math.sqrt(variance)
        # 8. Create feature DataFrame
        features = pd.DataFrame([{
            "mean_magnitude": mean_magnitude,
            "max_magnitude": max_magnitude,
            "min_magnitude": min_magnitude,
            "std_magnitude": std_magnitude,
            "range_magnitude": range_magnitude
        }])
        # 9. Ask AI for prediction
        prediction = model.predict(features)
        probabilities = model.predict_proba(
            features
        )
        confidence = probabilities.max()
        # 10. Display AI results
        print("\nPOTTO AI RESULT")
        print(
            "AI Prediction:",
            prediction[0]
        )
        print(
            f"Confidence: "
            f"{confidence * 100:.2f}%"
        )
except KeyboardInterrupt:
    print("\n\nPotto sensor simulation stopped.")
    print("Goodbye!")