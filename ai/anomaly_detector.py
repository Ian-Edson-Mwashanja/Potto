import pandas as pd
# LOAD POTTO DATASET
df = pd.read_csv("data/road_vibration_data.csv")
print("POTTO ANOMALY DETECTOR")
print(f"Total readings: {len(df)}")
# ANOMALY DETECTION
def detect_anomaly(magnitude):
    if magnitude >= 14:
        return "severe_anomaly"
    elif magnitude >= 12:
        return "moderate_anomaly"
    elif magnitude >= 10.5:
        return "minor_anomaly"
    else:
        return "normal"
# TEST THE DETECTOR
test_values = [
    9.8,
    10.2,
    11.5,
    13.4,
    16.8,
    19.2
]
print("\nTest results:")
for value in test_values:
    result = detect_anomaly(value)
    print(
        f"Magnitude: {value:.2f} -> {result}"
    )
# APPLY DETECTOR TO DATASET
df["prediction"] = df["magnitude"].apply(
    detect_anomaly
)
print("\nPredicted conditions:")
print(
    df["prediction"].value_counts()
)
def detect_anomaly(magnitude):
    if magnitude >= 14:
        return "severe"
    elif magnitude >= 12:
        return "moderate"
    elif magnitude >= 10.5:
        return "minor"
    else:
        return "normal"
def describe_result(magnitude):
    severity = detect_anomaly(magnitude)
    if severity == "normal":
        return "Normal road condition"
    elif severity == "minor":
        return "Minor road anomaly detected"
    elif severity == "moderate":
        return "Moderate road anomaly detected"
    else:
        return "Severe road anomaly detected"
print("\nPOTTO LIVE TEST")
test_values = [
    9.8,
    11.2,
    13.5,
    17.8
]
for value in test_values:
    message = describe_result(value)
    print(
        f"{value:.2f} -> {message}"
    )
# BASIC DATA STATISTICS
print("\nDataset statistics:")
print(
    df["magnitude"].describe()
)
# SAVE DETECTION RESULTS
df.to_csv(
    "data/detection_results.csv",
    index=False
)
print(
    "\nDetection results saved to:"
)
print(
    "data/detection_results.csv"
)