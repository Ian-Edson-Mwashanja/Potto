import pandas as pd
# Load dataset
df = pd.read_csv(
    "data/realistic_road_data.csv"
)
print("POTTO REALISTIC DATA ANALYSIS")
# Number of records
print(
    "\nTotal records:",
    len(df)
)
# Classes
print("\nRoad conditions:")
print(
    df["label"].value_counts()
)
# Average magnitude
print("\nAverage magnitude:")
print(
    df.groupby("label")["magnitude"].mean()
)
# Maximum magnitude
print("\nMaximum magnitude:")
print(
    df.groupby("label")["magnitude"].max()
)
