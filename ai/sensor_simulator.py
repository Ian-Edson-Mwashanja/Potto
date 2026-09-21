import random
import os
import math
import pandas as pd
# POTTO ACCELEROMETER SIMULATOR
def generate_normal_road():
    #Simulates normal road vibration.
    x = random.uniform(-0.5, 0.5)
    y = random.uniform(-0.5, 0.5)
    z = random.uniform(9.5, 10.1)
    return x, y, z
def generate_rough_road():
    #Simulates a rough road.
    x = random.uniform(-1.5, 1.5)
    y = random.uniform(-1.5, 1.5)
    z = random.uniform(8.5, 11.5)
    return x, y, z
def generate_small_pothole():
    #Simulates a small pothole.
    x = random.uniform(-2.5, 2.5)
    y = random.uniform(-2.5, 2.5)
    z = random.uniform(11.0, 14.0)
    return x, y, z
def generate_severe_pothole():
    #Simulates a severe pothole.
    x = random.uniform(-4.0, 4.0)
    y = random.uniform(-4.0, 4.0)
    z = random.uniform(14.0, 20.0)
    return x, y, z
# CALCULATE ACCELERATION MAGNITUDE
def calculate_magnitude(x, y, z):
    magnitude = math.sqrt(
        x**2 + y**2 + z**2
    )
    return magnitude
# GENERATE DATASET
data = []
# Generate normal road data
for i in range(250):
    x, y, z = generate_normal_road()
    magnitude = calculate_magnitude(x, y, z)
    data.append([
        x,
        y,
        z,
        magnitude,
        "normal"
    ])
# Generate rough road data
for i in range(250):
    x, y, z = generate_rough_road()
    magnitude = calculate_magnitude(x, y, z)
    data.append([
        x,
        y,
        z,
        magnitude,
        "rough"
    ])
# Generate small pothole data
for i in range(250):
    x, y, z = generate_small_pothole()
    magnitude = calculate_magnitude(x, y, z)
    data.append([
        x,
        y,
        z,
        magnitude,
        "small_pothole"
    ])
# Generate severe pothole data
for i in range(250):
    x, y, z = generate_severe_pothole()
    magnitude = calculate_magnitude(x, y, z)
    data.append([
        x,
        y,
        z,
        magnitude,
        "severe_pothole"
    ])
# CREATE DATAFRAME
columns = [
    "x",
    "y",
    "z",
    "magnitude",
    "label"
]
df = pd.DataFrame(data, columns=columns)
# SAVE DATASET
os.makedirs("data", exist_ok=True)
df.to_csv(
    "data/road_vibration_data.csv",
    index=False
)
print("POTTO SENSOR SIMULATOR")
print(f"Generated {len(df)} sensor readings.")
print("\nRoad condition distribution:")
print(df["label"].value_counts())
print("\nFirst 10 readings:")
print(df.head(10))
print("\nDataset saved to:")
print("data/road_vibration_data.csv")


