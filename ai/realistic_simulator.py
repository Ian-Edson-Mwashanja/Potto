import random
import math
import os
import pandas as pd
def normal_road():
    """
    Simulate a vehicle traveling on a relatively
    smooth road.
    """
    x = random.gauss(0, 0.3)
    y = random.gauss(0, 0.3)
    z = random.gauss(9.8, 0.25)
    return x, y, z
def rough_road():
    """
    Simulate continuous vibration caused by
    an uneven or rough road.
    """
    x = random.gauss(0, 0.8)
    y = random.gauss(0, 0.8)
    z = random.gauss(10.5, 1.0)
    return x, y, z
def speed_bump():
    """
    Simulate the vehicle traveling over a speed bump.
    """
    x = random.gauss(0, 1.2)
    y = random.gauss(0, 1.2)
    z = random.gauss(13.5, 2.0)
    return x, y, z
def braking():
    """
    Simulate vehicle braking.
    """
    x = random.gauss(2.5, 1.0)
    y = random.gauss(0, 0.5)
    z = random.gauss(10.5, 0.8)
    return x, y, z
def acceleration():
    """
    Simulate the vehicle accelerating.
    """
    x = random.gauss(-2.0, 0.8)
    y = random.gauss(0, 0.5)
    z = random.gauss(10.3, 0.8)
    return x, y, z
def small_pothole():
    """
    Simulate a small pothole impact.
    """
    x = random.gauss(1.5, 1.0)
    y = random.gauss(-1.2, 1.0)
    z = random.gauss(13.0, 2.0)
    return x, y, z
def severe_pothole():
    """
    Simulate a severe pothole impact.
    """
    x = random.gauss(3.0, 1.2)
    y = random.gauss(-2.0, 1.2)
    z = random.gauss(17.0, 2.5)
    return x, y, z
def calculate_magnitude(x, y, z):
    return math.sqrt(
        x**2 + y**2 + z**2
    )
data = []
events = {
    "normal": normal_road,
    "rough": rough_road,
    "speed_bump": speed_bump,
    "braking": braking,
    "acceleration": acceleration,
    "small_pothole": small_pothole,
    "severe_pothole": severe_pothole
}
for label, generator in events.items():
    for i in range(500):
        x, y, z = generator()
        magnitude = calculate_magnitude(
            x,
            y,
            z
        )
        data.append([
            x,
            y,
            z,
            magnitude,
            label
        ])
columns = [
    "x",
    "y",
    "z",
    "magnitude",
    "label"
]
df = pd.DataFrame(
    data,
    columns=columns
)
os.makedirs(
    "data",
    exist_ok=True
)
df.to_csv(
    "data/realistic_road_data.csv",
    index=False
)
print("      POTTO REALISTIC SENSOR SIMULATOR")
print(
    f"\nGenerated {len(df)} readings."
)
print("\nRoad event distribution:")
print(
    df["label"].value_counts()
)
print("\nSample data:")
print(
    df.head(10)
)
print(
    "\nDataset saved to:"
)
print(
    "data/realistic_road_data.csv"
)
