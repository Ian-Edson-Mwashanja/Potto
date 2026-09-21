import pandas as pd
import matplotlib.pyplot as plt
# LOAD POTTO DATASET
file_path = "data/road_vibration_data.csv"
df = pd.read_csv(file_path)
# DISPLAY BASIC INFORMATION
print("POTTO DATA ANALYSIS")
print("\nFirst 10 readings:")
print(df.head(10))
print("\nNumber of readings:")
print(len(df))
print("\nColumns:")
print(df.columns)
print("\nRoad condition distribution:")
print(df["label"].value_counts())
# AVERAGE MAGNITUDE BY ROAD CONDITION
average_magnitude = df.groupby("label")["magnitude"].mean()
print("\nAverage acceleration magnitude:")
print(average_magnitude)
# PLOT AVERAGE MAGNITUDE
average_magnitude.plot(
    kind="bar",
    title="Average Vibration by Road Condition",
    xlabel="Road Condition",
    ylabel="Acceleration Magnitude"
)
plt.tight_layout()
plt.show()
# PLOT ALL SENSOR READINGS
plt.figure(figsize=(12, 6))
plt.plot(
    df["magnitude"],
    linewidth=1
)
plt.title("Potto Simulated Road Vibration")
plt.xlabel("Reading Number")
plt.ylabel("Acceleration Magnitude")
plt.tight_layout()
plt.show()
# COMPARE ROAD CONDITIONS
plt.figure(figsize=(10, 6))
conditions = [
    "normal",
    "rough",
    "small_pothole",
    "severe_pothole"
]
for condition in conditions:
    values = df[df["label"] == condition]["magnitude"]
    plt.plot(
        values.values,
        label=condition
    )
plt.title("Vibration Patterns by Road Condition")
plt.xlabel("Reading")
plt.ylabel("Acceleration Magnitude")
plt.legend()
plt.tight_layout()
plt.show()

